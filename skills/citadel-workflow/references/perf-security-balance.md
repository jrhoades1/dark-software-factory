# Performance vs Security Balance

Reference for the CITADEL Drill step. Security shouldn't tank performance, and
performance shortcuts shouldn't create vulnerabilities.

## When Caching Auth Checks Is Safe

### Safe to cache

| What | TTL | Why safe |
|------|-----|----------|
| User role/permissions | 5 min | Roles change rarely; 5 min staleness is acceptable |
| Session validation | 1 min | Short TTL catches revoked sessions quickly |
| Rate limit counters | Real-time | Must be real-time in Redis/memory |
| Public resource access | 15 min | No auth needed, cache freely |
| API key validation | 5 min | Keys rarely change; revocation propagates at TTL |

### Never cache

| What | Why |
|------|-----|
| Password verification | Must hit DB every time (lockout counters) |
| MFA verification | Must be real-time |
| Authorization for write operations | Stale permission = unauthorized write |
| Token revocation checks | Revoked token must fail immediately |
| Account lockout status | Must be real-time |

### Cache invalidation pattern

```python
class AuthCache:
    """Cache auth decisions with targeted invalidation."""

    def __init__(self, redis_client):
        self.redis = redis_client

    async def get_user_permissions(self, user_id: str) -> list[str] | None:
        cached = await self.redis.get(f"perms:{user_id}")
        return json.loads(cached) if cached else None

    async def set_user_permissions(self, user_id: str, perms: list[str]):
        await self.redis.setex(f"perms:{user_id}", 300, json.dumps(perms))

    async def invalidate_user(self, user_id: str):
        """Call this when user's role/permissions change."""
        await self.redis.delete(f"perms:{user_id}")

    async def invalidate_all(self):
        """Nuclear option — clear all auth caches."""
        keys = await self.redis.keys("perms:*")
        if keys:
            await self.redis.delete(*keys)
```

---

## Rate Limiting Without Degrading UX

### Tiered rate limits

```python
RATE_LIMITS = {
    # Public endpoints (unauthenticated)
    "public": {
        "requests": 30,
        "window": 60,  # seconds
        "burst": 10,   # allow short bursts
    },
    # Authenticated users
    "authenticated": {
        "requests": 120,
        "window": 60,
        "burst": 30,
    },
    # Paid tier
    "premium": {
        "requests": 600,
        "window": 60,
        "burst": 100,
    },
    # Sensitive endpoints (login, password reset)
    "sensitive": {
        "requests": 5,
        "window": 60,
        "burst": 3,
    },
}
```

### UX-friendly rate limit responses

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

async def rate_limit_response(request, limit_info):
    """Return helpful rate limit info instead of bare 429."""
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "retry_after": limit_info["reset_seconds"],
            "limit": limit_info["limit"],
            "remaining": 0,
        },
        headers={
            "Retry-After": str(limit_info["reset_seconds"]),
            "X-RateLimit-Limit": str(limit_info["limit"]),
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": str(limit_info["reset_timestamp"]),
        },
    )
```

---

## Encryption Overhead Management

### Performance impact benchmarks (approximate)

| Operation | Overhead | Mitigation |
|-----------|----------|------------|
| TLS handshake | 1-3ms first request | Connection pooling, keep-alive |
| TLS per request | <0.1ms | Negligible with keep-alive |
| AES-256 field encryption | ~0.1ms per field | Encrypt only sensitive fields |
| Bcrypt password hashing | 100-300ms | Async, never on hot path |
| Database encryption at rest | <5% query overhead | Handled by DB engine, minimal |

### When to use field-level encryption

Only encrypt individual fields when:
- The field contains high-sensitivity data (SSN, financial accounts)
- Database encryption at rest isn't sufficient (compliance requires it)
- You need per-tenant encryption keys

Don't encrypt:
- Every field (massive overhead, breaks queries)
- Fields you need to search/sort/filter on (can't query encrypted data)
- Non-sensitive data (timestamps, status flags)

### Searchable encryption pattern

```python
# For fields that need both encryption AND searching:
# Store a secure hash alongside the encrypted value

class EncryptedSearchable:
    """Store encrypted value + searchable hash."""

    @staticmethod
    def store(plaintext: str) -> tuple[str, str]:
        encrypted = encryptor.encrypt(plaintext)
        # HMAC for searching — consistent hash, not reversible
        search_hash = hmac.new(
            SEARCH_KEY, plaintext.encode(), hashlib.sha256
        ).hexdigest()
        return encrypted, search_hash

    @staticmethod
    def search(plaintext: str) -> str:
        """Generate search hash for WHERE clause."""
        return hmac.new(
            SEARCH_KEY, plaintext.encode(), hashlib.sha256
        ).hexdigest()

# Usage: find patient by SSN without decrypting database
hash_to_find = EncryptedSearchable.search("123-45-6789")
patient = await db.query(Patient).filter(Patient.ssn_hash == hash_to_find).first()
```

---

## CDN Security Considerations

```
[ ] Cache-Control headers set correctly (no caching of authenticated responses)
[ ] Vary: Authorization header on protected endpoints
[ ] CDN configured to pass auth headers to origin
[ ] Static assets cached aggressively (cache-bust via content hash)
[ ] API responses not cached at CDN level (or very short TTL)
[ ] CORS headers set at origin, not CDN
[ ] WAF rules on CDN (rate limiting, bot detection)
```

### Cache header patterns

```python
# Public static assets — cache aggressively
@app.get("/static/{path}")
async def static_file(path: str):
    return FileResponse(path, headers={
        "Cache-Control": "public, max-age=31536000, immutable",
    })

# Authenticated API responses — never cache at CDN
@app.get("/api/me")
async def get_profile(user = Depends(get_current_user)):
    return JSONResponse(content=user.to_dict(), headers={
        "Cache-Control": "private, no-store",
        "Vary": "Authorization",
    })

# Public API responses — short cache
@app.get("/api/public/stats")
async def public_stats():
    return JSONResponse(content=get_stats(), headers={
        "Cache-Control": "public, max-age=60",
    })
```

---

## Database Query Optimization (Security-Safe)

### Pagination (prevents full table scan DoS)

```python
MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 20

@app.get("/api/items")
async def list_items(
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=MAX_PAGE_SIZE, default=DEFAULT_PAGE_SIZE),
):
    offset = (page - 1) * size
    items = await db.query(Item).offset(offset).limit(size).all()
    total = await db.query(func.count(Item.id)).scalar()
    return {"items": items, "total": total, "page": page, "size": size}
```

### Query timeout (prevents long-running query DoS)

```python
# Set statement timeout per query
async def safe_query(query, timeout_ms: int = 5000):
    await db.execute(text(f"SET LOCAL statement_timeout = {timeout_ms}"))
    return await db.execute(query)
```
