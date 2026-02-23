# API Security Patterns

Reference for the CITADEL Assemble step for API-heavy applications.

## API Versioning

### URL-based versioning (recommended for simplicity)

```
/api/v1/users
/api/v2/users
```

```python
# FastAPI
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

app.include_router(v1_router)
app.include_router(v2_router)
```

### Rules
- Never break v1 consumers when shipping v2
- Deprecate with `Sunset` header and 6-month notice
- Old versions get security patches only (no features)

---

## Request Signing (API-to-API)

For trusted server-to-server communication, sign requests with HMAC.

```python
import hmac
import hashlib
import time

def sign_request(method: str, path: str, body: bytes, secret: str) -> dict:
    """Generate signed headers for outgoing API requests."""
    timestamp = str(int(time.time()))
    payload = f"{method}\n{path}\n{timestamp}\n".encode() + body
    signature = hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()

    return {
        "X-Signature": signature,
        "X-Timestamp": timestamp,
    }

def verify_request(method: str, path: str, body: bytes,
                   signature: str, timestamp: str, secret: str) -> bool:
    """Verify incoming signed request."""
    # Reject requests older than 5 minutes (replay protection)
    if abs(time.time() - int(timestamp)) > 300:
        return False

    payload = f"{method}\n{path}\n{timestamp}\n".encode() + body
    expected = hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected)
```

---

## GraphQL Security

GraphQL has unique attack surfaces that REST APIs don't.

### Query depth limiting

```python
# Prevent deeply nested queries that can DoS the server
# Bad: { user { posts { comments { author { posts { ... } } } } } }

from graphql import GraphQLError

MAX_DEPTH = 5

def depth_limit_validation(document, max_depth=MAX_DEPTH):
    """Reject queries that exceed maximum nesting depth."""
    def check_depth(node, depth=0):
        if depth > max_depth:
            raise GraphQLError(
                f"Query depth {depth} exceeds maximum allowed depth {max_depth}"
            )
        for child in getattr(node, 'selection_set', None)?.selections or []:
            check_depth(child, depth + 1)

    for definition in document.definitions:
        check_depth(definition)
```

### Query complexity limiting

```python
# Assign cost to each field, reject queries over budget
COMPLEXITY_LIMIT = 1000

FIELD_COSTS = {
    "users": 10,         # List query
    "user": 1,           # Single lookup
    "posts": 10,         # List query
    "comments": 5,       # Nested list
    "analytics": 50,     # Expensive computation
}
```

### Introspection control

```python
# Disable introspection in production
if settings.ENVIRONMENT == "production":
    schema = build_schema(disable_introspection=True)
```

### GraphQL-specific checklist

```
[ ] Query depth limiting enabled (max 5-7 levels)
[ ] Query complexity limiting enabled
[ ] Introspection disabled in production
[ ] Persisted queries for production (no arbitrary queries)
[ ] Rate limiting per query complexity (not just per request)
[ ] N+1 query prevention (DataLoader pattern)
[ ] Field-level authorization (not just type-level)
[ ] Input validation on all arguments
[ ] Error masking in production (no stack traces)
```

---

## Webhook Security

### Sending webhooks

```python
import hmac
import hashlib
import httpx

async def send_webhook(url: str, payload: dict, secret: str):
    """Send signed webhook with retry logic."""
    body = json.dumps(payload).encode()
    signature = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Webhook-Signature": f"sha256={signature}",
        "X-Webhook-Timestamp": str(int(time.time())),
        "X-Webhook-ID": str(uuid.uuid4()),  # For idempotency
    }

    async with httpx.AsyncClient() as client:
        for attempt in range(3):
            try:
                response = await client.post(
                    url, content=body, headers=headers, timeout=10.0
                )
                if response.status_code < 300:
                    return True
            except httpx.TimeoutException:
                pass
            await asyncio.sleep(2 ** attempt)  # Exponential backoff

    # After 3 failures, mark endpoint as failing
    await mark_webhook_failing(url)
    return False
```

### Receiving webhooks

```python
@app.post("/webhooks/incoming")
async def receive_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Webhook-Signature", "")
    timestamp = request.headers.get("X-Webhook-Timestamp", "")
    webhook_id = request.headers.get("X-Webhook-ID", "")

    # Verify signature
    expected = hmac.new(
        WEBHOOK_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(f"sha256={expected}", signature):
        raise HTTPException(400, "Invalid signature")

    # Replay protection
    if abs(time.time() - int(timestamp)) > 300:
        raise HTTPException(400, "Request too old")

    # Idempotency check
    if await is_webhook_processed(webhook_id):
        return {"status": "already processed"}

    # Process asynchronously
    await queue.enqueue(process_webhook, body)
    await mark_webhook_processed(webhook_id)

    return {"status": "accepted"}
```

---

## Rate Limiting Tiers

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Public endpoints
@app.get("/api/public/data")
@limiter.limit("30/minute")
async def public_data():
    ...

# Authenticated endpoints
@app.get("/api/users/me")
@limiter.limit("120/minute")
async def get_profile(user=Depends(get_current_user)):
    ...

# Sensitive endpoints
@app.post("/api/auth/login")
@limiter.limit("5/minute")
async def login():
    ...

# AI endpoints (expensive)
@app.post("/api/ai/generate")
@limiter.limit("10/minute")
async def ai_generate(user=Depends(get_current_user)):
    ...

# Webhook endpoints
@app.post("/webhooks/stripe")
@limiter.limit("100/minute")
async def stripe_webhook():
    ...
```

---

## Security Headers Middleware

```python
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains; preload"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=()"
    )
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https://api.yourdomain.com; "
        "frame-ancestors 'none'"
    )

    return response
```

---

## CORS Configuration

```python
# Development — permissive
if settings.ENVIRONMENT == "development":
    origins = ["http://localhost:3000", "http://localhost:5173"]
else:
    # Production — strict whitelist
    origins = ["https://app.yourdomain.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600,  # Cache preflight for 1 hour
)
```
