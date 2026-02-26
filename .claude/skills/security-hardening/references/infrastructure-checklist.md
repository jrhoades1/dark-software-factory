# Infrastructure Security Checklist

Reference for the security-hardening Enforce step when deploying to cloud infrastructure.

## Cloud Security (AWS / GCP / Azure)

### IAM

```
[ ] No root/owner account used for daily operations
[ ] MFA enabled on all human accounts
[ ] Service accounts use least-privilege roles
[ ] No wildcard permissions (Action: "*", Resource: "*")
[ ] API keys rotated on schedule (90 days max)
[ ] Unused accounts/keys removed
[ ] Cross-account access reviewed and justified
[ ] IAM policies attached to groups/roles, not individual users
```

### Networking

```
[ ] VPC/VNet configured with private subnets for databases
[ ] Security groups/firewall rules follow least-privilege
[ ] No 0.0.0.0/0 ingress on non-public services
[ ] Database not accessible from public internet
[ ] VPN or bastion host for admin access
[ ] Network flow logs enabled
[ ] DNS configured with DNSSEC where possible
```

### Storage

```
[ ] No public S3 buckets / Cloud Storage buckets / Blob containers
[ ] Encryption at rest enabled on all storage
[ ] Versioning enabled for critical buckets
[ ] Lifecycle policies configured (auto-delete old objects)
[ ] Access logging enabled on storage
[ ] Cross-origin access restricted (CORS)
```

### Compute

```
[ ] OS patches applied (automated patching preferred)
[ ] Unnecessary ports closed
[ ] SSH key authentication only (no password auth)
[ ] Instance metadata service (IMDS) restricted to v2 (IMDSv2 on AWS)
[ ] No secrets in user data / startup scripts
[ ] Instances in private subnets where possible
```

### Logging & Audit

```
[ ] CloudTrail / Cloud Audit Logs / Azure Activity Log enabled
[ ] Logs shipped to centralized, immutable storage
[ ] Log retention meets compliance requirements (6 years for HIPAA)
[ ] Alerting configured on suspicious activity
[ ] VPC flow logs enabled
[ ] Database audit logging enabled
```

---

## Container Security

### Image hardening

```
[ ] Minimal base image (alpine, distroless, or slim variants)
[ ] Non-root user in container
[ ] No secrets baked into image
[ ] Multi-stage build (build deps not in final image)
[ ] Image scanning in CI (Trivy, Snyk, etc.)
[ ] Pinned base image version (not :latest)
[ ] Signed images where possible
```

### Secure Dockerfile template

```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY src/ ./src/

# Production stage
FROM python:3.12-slim AS production

# Security: non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy only what's needed
COPY --from=builder /root/.local /home/appuser/.local
COPY --from=builder /build/src /app/src

WORKDIR /app
USER appuser

# Security: read-only filesystem where possible
# Security: no new privileges
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()"

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Runtime security

```
[ ] Read-only root filesystem (mount writable volumes only where needed)
[ ] No privileged containers
[ ] Resource limits set (CPU, memory)
[ ] Network policies restrict pod-to-pod communication
[ ] Secrets mounted as volumes (not environment variables)
[ ] Container runtime security (seccomp, AppArmor)
[ ] No host network mode
[ ] No host PID mode
```

### Docker Compose security

```yaml
services:
  app:
    image: myapp:1.0.0
    read_only: true
    security_opt:
      - no-new-privileges:true
    tmpfs:
      - /tmp:size=100M
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
```

---

## Kubernetes Security (if applicable)

```
[ ] Pod security standards enforced (restricted profile)
[ ] Network policies defined for all namespaces
[ ] RBAC with least-privilege roles
[ ] Secrets encrypted at rest (etcd encryption)
[ ] Image pull from private registry only
[ ] Resource quotas set per namespace
[ ] Admission controllers active (OPA/Gatekeeper)
[ ] Audit logging enabled on API server
```

---

## Database Security

```
[ ] Encryption at rest enabled
[ ] SSL/TLS required for connections (sslmode=require)
[ ] Database user has minimal privileges (no SUPERUSER)
[ ] Separate users for application, migration, and admin
[ ] Connection pooling with limits
[ ] Slow query logging enabled
[ ] Automated backups configured and tested
[ ] Point-in-time recovery tested
[ ] No default passwords
[ ] Database not accessible from public internet
```

### PostgreSQL hardening

```sql
-- Verify SSL is required
SHOW ssl;  -- should be 'on'

-- Check existing roles and privileges
SELECT rolname, rolsuper, rolcreaterole, rolcreatedb FROM pg_roles;

-- Verify RLS is enabled on all user-data tables
SELECT schemaname, tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';

-- Check for overly permissive grants
SELECT grantee, table_name, privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'public';
```

---

## CI/CD Security

```
[ ] Secrets stored in CI/CD vault (not in repo)
[ ] Pipeline runs with least-privilege credentials
[ ] Dependencies pinned in lockfile
[ ] Security scanning in pipeline (SAST, dependency audit, secrets)
[ ] Deployment requires approval for production
[ ] Audit trail on all deployments
[ ] Rollback procedure tested
[ ] Branch protection on main/production branches
[ ] No force push to protected branches
```
