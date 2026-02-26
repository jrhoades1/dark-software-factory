# Zero-Trust Implementation Patterns

Reference for the CITADEL Inventory and Assemble steps. Zero-trust means: verify
every request, assume the network is hostile, enforce least privilege everywhere.

## Core Principle

Never trust:
- The network (even internal)
- The client (even authenticated)
- The request (even from known users)
- The data (even from your own database)

Always verify: identity, authorization, input integrity, output safety.

---

## Authentication Middleware Stack

Every request passes through these layers in order. Each layer can reject the request.

### Express.js (Node.js)

```typescript
// middleware/auth.ts — JWT verification + account status + permission check + audit

import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

interface AuthenticatedRequest extends Request {
    user: { id: string; role: string; orgId: string };
}

// Layer 1: Verify JWT
export function verifyToken(req: Request, res: Response, next: NextFunction) {
    const token = req.cookies?.session_token
        || req.headers.authorization?.replace('Bearer ', '');

    if (!token) {
        return res.status(401).json({ error: 'Authentication required' });
    }

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET!, {
            algorithms: ['HS256'],
            maxAge: '1h',
        });
        (req as AuthenticatedRequest).user = decoded as any;
        next();
    } catch (err) {
        return res.status(401).json({ error: 'Invalid or expired token' });
    }
}

// Layer 2: Verify account is active
export async function verifyAccountStatus(
    req: Request, res: Response, next: NextFunction
) {
    const userId = (req as AuthenticatedRequest).user.id;
    const user = await db.users.findById(userId);

    if (!user || !user.is_active) {
        return res.status(403).json({ error: 'Account deactivated' });
    }

    if (user.locked_until && user.locked_until > new Date()) {
        return res.status(423).json({ error: 'Account locked' });
    }

    next();
}

// Layer 3: Verify permission for this action
export function requirePermission(permission: string) {
    return (req: Request, res: Response, next: NextFunction) => {
        const user = (req as AuthenticatedRequest).user;
        const allowed = checkPermission(user.role, permission);

        if (!allowed) {
            auditLog('AUTHORIZATION_DENIED', {
                userId: user.id,
                permission,
                path: req.path,
            });
            return res.status(403).json({ error: 'Insufficient permissions' });
        }

        next();
    };
}

// Layer 4: Audit log
export function auditRequest(req: Request, res: Response, next: NextFunction) {
    const user = (req as AuthenticatedRequest).user;
    auditLog('REQUEST', {
        userId: user.id,
        method: req.method,
        path: req.path,
        ip: req.ip,
        userAgent: req.headers['user-agent'],
    });
    next();
}

// Compose the stack
app.use('/api/protected/*',
    verifyToken,
    verifyAccountStatus,
    auditRequest
);

// Per-route permissions
app.delete('/api/protected/users/:id',
    requirePermission('users:delete'),
    deleteUserHandler
);
```

### FastAPI (Python)

```python
# middleware/auth.py

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from datetime import datetime

security = HTTPBearer()

async def verify_token(request: Request, token = Depends(security)):
    """Layer 1: Verify JWT signature and expiry."""
    try:
        payload = jwt.decode(
            token.credentials,
            settings.JWT_SECRET,
            algorithms=["HS256"],
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def verify_account_status(
    payload: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    """Layer 2: Verify account is active and not locked."""
    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="Account deactivated")
    if user.locked_until and user.locked_until > datetime.utcnow():
        raise HTTPException(status_code=423, detail="Account locked")
    return user

def require_role(*roles: str):
    """Layer 3: Require specific role."""
    async def check(user: User = Depends(verify_account_status)):
        if user.role not in roles:
            await audit_log("AUTHORIZATION_DENIED", user_id=user.id)
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return check

# Usage
@app.delete("/api/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_role("admin")),
):
    ...
```

---

## Tenant Isolation

Multi-tenant apps MUST prevent cross-tenant data access.

### Database-level isolation (preferred)

```sql
-- Every query is automatically scoped to the user's org
-- Even if application code has a bug, RLS prevents cross-tenant access

CREATE POLICY "tenant_isolation" ON projects
    FOR ALL USING (
        org_id = current_setting('app.current_org_id')::uuid
    );
```

```python
# Set tenant context at the start of every request
@app.middleware("http")
async def set_tenant_context(request: Request, call_next):
    user = request.state.user
    if user:
        await db.execute(
            text("SET app.current_org_id = :org_id"),
            {"org_id": str(user.org_id)}
        )
    return await call_next(request)
```

### Application-level checks (defense in depth)

```python
# Even with RLS, add application-level tenant checks
async def get_project(project_id: str, user: User):
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(404)
    if project.org_id != user.org_id:  # Belt AND suspenders
        await audit_log("CROSS_TENANT_ATTEMPT", user_id=user.id)
        raise HTTPException(404)  # 404, not 403 — don't leak existence
    return project
```

---

## Field-Level Encryption

For high-sensitivity data (SSN, financial data, PHI), encrypt at the application
level in addition to database encryption at rest.

```python
from cryptography.fernet import Fernet

class FieldEncryptor:
    """Encrypt/decrypt individual fields with per-tenant keys."""

    def __init__(self, master_key: bytes):
        self.fernet = Fernet(master_key)

    def encrypt(self, plaintext: str) -> str:
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        return self.fernet.decrypt(ciphertext.encode()).decode()

# Usage in model
class Patient(Base):
    _ssn_encrypted = Column("ssn", String)  # Stored encrypted

    @property
    def ssn(self) -> str:
        return encryptor.decrypt(self._ssn_encrypted)

    @ssn.setter
    def ssn(self, value: str):
        self._ssn_encrypted = encryptor.encrypt(value)
```

---

## mTLS Between Services

For microservice architectures, use mutual TLS — both client and server verify
each other's certificates.

```yaml
# docker-compose.yml — mTLS between services
services:
  api:
    environment:
      - TLS_CERT=/certs/api.crt
      - TLS_KEY=/certs/api.key
      - TLS_CA=/certs/ca.crt
      - REQUIRE_CLIENT_CERT=true
    volumes:
      - ./certs:/certs:ro

  worker:
    environment:
      - TLS_CERT=/certs/worker.crt
      - TLS_KEY=/certs/worker.key
      - TLS_CA=/certs/ca.crt
    volumes:
      - ./certs:/certs:ro
```

```python
# Python client with mTLS
import httpx

client = httpx.Client(
    cert=("/certs/worker.crt", "/certs/worker.key"),
    verify="/certs/ca.crt",
)
response = client.get("https://api:8443/internal/data")
```

---

## Request Signing

For webhook receivers and API-to-API calls, verify request integrity with HMAC.

```python
import hmac
import hashlib

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify HMAC-SHA256 signature on incoming webhook."""
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)

# In route handler
@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    if not verify_webhook_signature(payload, sig, settings.STRIPE_WEBHOOK_SECRET):
        raise HTTPException(400, "Invalid signature")
    ...
```

---

## Session Security

```python
# Secure cookie configuration
SESSION_CONFIG = {
    "httponly": True,      # JavaScript cannot access
    "secure": True,        # HTTPS only
    "samesite": "strict",  # No cross-site requests
    "max_age": 3600,       # 1 hour
    "path": "/",
    "domain": None,        # Current domain only
}
```

### Token rotation

```python
async def refresh_token(refresh_token: str) -> dict:
    """Rotate refresh token on each use (prevents replay attacks)."""
    stored = await db.get_refresh_token(refresh_token)
    if not stored or stored.used or stored.expires_at < datetime.utcnow():
        # Token reuse detected — revoke all tokens for this user
        if stored and stored.used:
            await revoke_all_tokens(stored.user_id)
            await audit_log("TOKEN_REUSE_DETECTED", user_id=stored.user_id)
        raise HTTPException(401, "Invalid refresh token")

    # Mark old token as used
    await db.mark_token_used(refresh_token)

    # Issue new pair
    new_access = create_access_token(stored.user_id)
    new_refresh = create_refresh_token(stored.user_id)
    return {"access_token": new_access, "refresh_token": new_refresh}
```
