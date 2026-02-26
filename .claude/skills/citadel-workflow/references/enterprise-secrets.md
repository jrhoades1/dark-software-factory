# Enterprise Secrets Management

Reference for the CITADEL Tie step when projects outgrow `.env` files.

## When to upgrade from .env

- Team has 3+ developers
- Multiple deployment environments (staging, production)
- Compliance requirements (SOC 2, HIPAA)
- Secrets need audit logging
- Automated rotation required

---

## AWS Secrets Manager

```python
import boto3
import json

def get_secret(secret_name: str, region: str = "us-east-1") -> dict:
    """Retrieve secret from AWS Secrets Manager."""
    client = boto3.client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

# Usage
db_creds = get_secret("prod/database")
DATABASE_URL = f"postgresql://{db_creds['username']}:{db_creds['password']}@{db_creds['host']}/{db_creds['database']}"
```

### Rotation setup
```python
# AWS manages rotation automatically with a Lambda function
# Configure rotation schedule: 30-90 days
# Ensure application handles credential refresh gracefully

# In application: catch auth failures and re-fetch secret
async def get_db_connection():
    try:
        return await create_connection(get_cached_secret("prod/database"))
    except AuthenticationError:
        # Secret may have rotated — clear cache and retry
        clear_secret_cache("prod/database")
        return await create_connection(get_cached_secret("prod/database"))
```

### IAM policy (least privilege)
```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": ["secretsmanager:GetSecretValue"],
        "Resource": "arn:aws:secretsmanager:us-east-1:*:secret:prod/*"
    }]
}
```

---

## GCP Secret Manager

```python
from google.cloud import secretmanager

def get_secret(project_id: str, secret_id: str, version: str = "latest") -> str:
    """Retrieve secret from GCP Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
```

---

## Azure Key Vault

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_secret(vault_url: str, secret_name: str) -> str:
    """Retrieve secret from Azure Key Vault."""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    return client.get_secret(secret_name).value
```

---

## HashiCorp Vault (self-hosted)

```python
import hvac

def get_secret(path: str) -> dict:
    """Retrieve secret from HashiCorp Vault."""
    client = hvac.Client(
        url=os.environ["VAULT_ADDR"],
        token=os.environ["VAULT_TOKEN"],
    )
    response = client.secrets.kv.v2.read_secret_version(path=path)
    return response["data"]["data"]
```

---

## Secret Caching Pattern

Don't fetch secrets on every request — cache with TTL.

```python
from functools import lru_cache
from datetime import datetime, timedelta

class SecretCache:
    """Cache secrets with configurable TTL."""

    def __init__(self, ttl_seconds: int = 300):
        self._cache: dict[str, tuple[str, datetime]] = {}
        self._ttl = timedelta(seconds=ttl_seconds)

    def get(self, key: str) -> str | None:
        if key in self._cache:
            value, fetched_at = self._cache[key]
            if datetime.utcnow() - fetched_at < self._ttl:
                return value
            del self._cache[key]
        return None

    def set(self, key: str, value: str):
        self._cache[key] = (value, datetime.utcnow())

    def clear(self, key: str = None):
        if key:
            self._cache.pop(key, None)
        else:
            self._cache.clear()
```

---

## Migration checklist (.env → vault)

```
[ ] Inventory all secrets currently in .env
[ ] Create secrets in vault with same names
[ ] Update application code to read from vault
[ ] Test with vault in staging first
[ ] Rotate all secrets (old .env values are burned)
[ ] Remove .env from servers
[ ] Set up automated rotation schedule
[ ] Configure audit logging on secret access
[ ] Document emergency access procedure
```
