# Secure Schema Patterns

Reference for the CITADEL Inventory step. Every data model should include these
security constraints at the database level — don't rely on application code alone.

## PostgreSQL with Row Level Security

### Users table (foundation)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE
        CHECK (email ~* '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        CHECK (length(email) <= 254),
    password_hash TEXT NOT NULL
        CHECK (length(password_hash) >= 60),  -- bcrypt minimum
    role TEXT NOT NULL DEFAULT 'user'
        CHECK (role IN ('user', 'admin', 'manager', 'readonly')),
    display_name TEXT
        CHECK (length(display_name) BETWEEN 1 AND 100),
    is_active BOOLEAN NOT NULL DEFAULT true,
    failed_login_attempts INTEGER NOT NULL DEFAULT 0
        CHECK (failed_login_attempts >= 0),
    locked_until TIMESTAMPTZ,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Index for login lookups
CREATE UNIQUE INDEX idx_users_email_lower ON users (lower(email));

-- RLS: Users see only themselves; admins see all
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users_select_own" ON users
    FOR SELECT USING (
        id = auth.uid() OR
        EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin')
    );

CREATE POLICY "users_update_own" ON users
    FOR UPDATE USING (id = auth.uid())
    WITH CHECK (id = auth.uid());
```

### Multi-tenant data table

```sql
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL CHECK (length(name) BETWEEN 1 AND 200),
    slug TEXT NOT NULL UNIQUE CHECK (slug ~* '^[a-z0-9-]+$'),
    owner_id UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE org_members (
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'member'
        CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
    joined_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (org_id, user_id)
);

-- Tenant-scoped data: every row belongs to an org
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name TEXT NOT NULL CHECK (length(name) BETWEEN 1 AND 200),
    description TEXT CHECK (length(description) <= 5000),
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'archived', 'deleted')),
    created_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- RLS: Users see only projects in their org
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY "projects_tenant_isolation" ON projects
    FOR ALL USING (
        org_id IN (
            SELECT org_id FROM org_members
            WHERE user_id = auth.uid()
        )
    );
```

### Audit log table

```sql
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    event_type TEXT NOT NULL
        CHECK (event_type IN (
            'LOGIN', 'LOGOUT', 'LOGIN_FAILED',
            'CREATE', 'READ', 'UPDATE', 'DELETE',
            'PERMISSION_CHANGE', 'EXPORT', 'ADMIN_ACTION'
        )),
    actor_id UUID REFERENCES users(id),
    actor_ip INET,
    resource_type TEXT NOT NULL,
    resource_id TEXT,
    details JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Audit logs are append-only — no updates or deletes
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "audit_insert_only" ON audit_log
    FOR INSERT WITH CHECK (true);

CREATE POLICY "audit_read_admin" ON audit_log
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'admin')
    );

-- Partition by month for performance
CREATE INDEX idx_audit_created ON audit_log (created_at);
CREATE INDEX idx_audit_actor ON audit_log (actor_id);
CREATE INDEX idx_audit_resource ON audit_log (resource_type, resource_id);
```

## Constraint patterns

### Length limits (prevent DoS via oversized payloads)
```sql
-- Always set maximum lengths on text fields
name TEXT CHECK (length(name) <= 200)
description TEXT CHECK (length(description) <= 10000)
bio TEXT CHECK (length(bio) <= 2000)
url TEXT CHECK (length(url) <= 2048)
```

### Non-negative values
```sql
price NUMERIC(10, 2) CHECK (price >= 0)
quantity INTEGER CHECK (quantity >= 0)
rating NUMERIC(2, 1) CHECK (rating BETWEEN 0 AND 5)
```

### Enum-like constraints
```sql
-- Prefer CHECK over enum types (easier to modify)
status TEXT CHECK (status IN ('draft', 'published', 'archived'))
priority TEXT CHECK (priority IN ('low', 'medium', 'high', 'critical'))
```

### Temporal constraints
```sql
-- End date must be after start date
CHECK (end_date > start_date)

-- Prevent future dates where inappropriate
CHECK (date_of_birth <= CURRENT_DATE)

-- Automatic updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON your_table
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

## Supabase-specific patterns

```sql
-- Use Supabase auth.uid() for RLS
CREATE POLICY "user_data" ON user_profiles
    FOR ALL USING (auth.uid() = user_id);

-- Service role bypasses RLS (use only in trusted server-side code)
-- Never expose service role key to client
```

## SQLAlchemy / Alembic patterns

```python
from sqlalchemy import Column, String, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("length(email) <= 254", name="ck_users_email_length"),
        CheckConstraint("length(display_name) <= 100", name="ck_users_name_length"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(254), unique=True, nullable=False)
    display_name = Column(String(100))
```

## Migration safety

- Always add constraints in a separate migration from data changes
- Test migrations against a copy of production data
- Include both `upgrade()` and `downgrade()` in every migration
- Never modify a migration that's been applied to production — create a new one
