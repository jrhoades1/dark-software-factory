# AI Feature Security Patterns

Reference for the CITADEL Assemble step when building AI-powered features.
Covers OWASP Top 10 for LLMs and practical defense patterns.

## Threat Model

| Threat | Description | Severity |
|--------|-------------|----------|
| Prompt injection | User manipulates AI behavior via crafted input | Critical |
| Data exfiltration | AI leaks sensitive data from context/training | High |
| Cost abuse | Automated requests drain API budget | High |
| Output injection | AI generates malicious content (XSS, SQL) | High |
| Denial of service | Oversized inputs cause timeout/cost spike | Medium |
| Model abuse | Using AI for prohibited content generation | Medium |

---

## 1. Input Sanitization

Clean ALL user input before it reaches the AI model.

```python
import re
from typing import Optional

class AIInputSanitizer:
    """Sanitize user input before sending to LLM."""

    MAX_INPUT_LENGTH = 10000  # Characters
    MAX_TOKENS_ESTIMATE = 2500  # ~4 chars per token

    # Patterns that commonly appear in injection attempts
    SUSPICIOUS_PATTERNS = [
        r"ignore\s+(previous|above|all)\s+instructions",
        r"you\s+are\s+now\s+",
        r"system\s*:\s*",
        r"<\|.*?\|>",
        r"\[INST\]",
        r"```system",
    ]

    @classmethod
    def sanitize(cls, user_input: str) -> tuple[str, list[str]]:
        """
        Returns (sanitized_input, warnings).
        Warnings are logged but don't block the request.
        """
        warnings = []

        # Length check
        if len(user_input) > cls.MAX_INPUT_LENGTH:
            user_input = user_input[:cls.MAX_INPUT_LENGTH]
            warnings.append("Input truncated to maximum length")

        # Strip null bytes and control characters (except newlines)
        user_input = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', user_input)

        # Check for suspicious patterns (log, don't block)
        for pattern in cls.SUSPICIOUS_PATTERNS:
            if re.search(pattern, user_input, re.IGNORECASE):
                warnings.append(f"Suspicious pattern detected: {pattern}")

        return user_input, warnings
```

### Prompt structure (defense in depth)

```python
def build_prompt(system_instructions: str, user_input: str) -> list[dict]:
    """
    Structure prompts to minimize injection surface.
    User input is always in a separate message, never concatenated
    into the system prompt.
    """
    sanitized, warnings = AIInputSanitizer.sanitize(user_input)

    if warnings:
        logger.warning("AI input warnings", extra={"warnings": warnings})

    return [
        {
            "role": "system",
            "content": system_instructions,
            # System prompt NEVER contains user input
        },
        {
            "role": "user",
            "content": sanitized,
            # User input is isolated in its own message
        },
    ]
```

---

## 2. Output Validation

Never trust AI output. Validate before rendering or executing.

```python
import bleach
from typing import Any

class AIOutputValidator:
    """Validate and sanitize AI model output before use."""

    @staticmethod
    def sanitize_for_html(ai_output: str) -> str:
        """Remove any HTML/script tags from AI output before rendering."""
        return bleach.clean(
            ai_output,
            tags=["p", "br", "strong", "em", "ul", "ol", "li", "code", "pre"],
            strip=True,
        )

    @staticmethod
    def validate_json_output(ai_output: str, schema: dict) -> Any:
        """Parse and validate AI JSON output against a schema."""
        import json
        from jsonschema import validate, ValidationError

        try:
            parsed = json.loads(ai_output)
            validate(parsed, schema)
            return parsed
        except (json.JSONDecodeError, ValidationError) as e:
            logger.error("AI output validation failed", extra={"error": str(e)})
            return None

    @staticmethod
    def validate_sql_safe(ai_output: str) -> bool:
        """Check that AI output doesn't contain SQL injection patterns."""
        dangerous = [
            "DROP", "DELETE", "TRUNCATE", "ALTER", "GRANT",
            "INSERT", "UPDATE", "--", ";", "/*",
        ]
        upper = ai_output.upper()
        return not any(d in upper for d in dangerous)

    @staticmethod
    def check_for_pii(ai_output: str) -> list[str]:
        """Detect if AI accidentally included PII in output."""
        import re
        findings = []
        # SSN pattern
        if re.search(r'\b\d{3}-\d{2}-\d{4}\b', ai_output):
            findings.append("Possible SSN detected")
        # Email pattern
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', ai_output):
            findings.append("Email address detected")
        # Phone pattern
        if re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', ai_output):
            findings.append("Phone number detected")
        return findings
```

---

## 3. Rate Limiting and Cost Controls

```python
from datetime import datetime, timedelta
from collections import defaultdict

class AIRateLimiter:
    """Rate limit and cost control for AI API calls."""

    def __init__(self):
        self.user_requests: dict[str, list[datetime]] = defaultdict(list)
        self.user_tokens: dict[str, int] = defaultdict(int)

    # Limits
    REQUESTS_PER_MINUTE = 10
    REQUESTS_PER_HOUR = 100
    TOKENS_PER_DAY = 100_000  # Per user
    MAX_OUTPUT_TOKENS = 4096
    COST_ALERT_THRESHOLD_DAILY = 50.00  # USD

    def check_rate_limit(self, user_id: str) -> bool:
        """Check if user has exceeded rate limits."""
        now = datetime.utcnow()
        requests = self.user_requests[user_id]

        # Clean old entries
        requests[:] = [r for r in requests if r > now - timedelta(hours=1)]

        # Per-minute check
        recent = [r for r in requests if r > now - timedelta(minutes=1)]
        if len(recent) >= self.REQUESTS_PER_MINUTE:
            return False

        # Per-hour check
        if len(requests) >= self.REQUESTS_PER_HOUR:
            return False

        return True

    def check_token_budget(self, user_id: str, estimated_tokens: int) -> bool:
        """Check if user has token budget remaining."""
        return (self.user_tokens[user_id] + estimated_tokens) <= self.TOKENS_PER_DAY

    def record_usage(self, user_id: str, tokens_used: int, cost: float):
        """Record usage for tracking and alerting."""
        self.user_requests[user_id].append(datetime.utcnow())
        self.user_tokens[user_id] += tokens_used

        # Cost alerting
        if cost > self.COST_ALERT_THRESHOLD_DAILY:
            alert_ops(f"AI cost threshold exceeded: ${cost:.2f} for user {user_id}")
```

### Budget enforcement in API wrapper

```python
async def call_ai(
    messages: list[dict],
    user_id: str,
    max_tokens: int = 1024,
) -> str:
    """Wrapper around AI API with rate limiting and cost controls."""
    limiter = get_rate_limiter()

    if not limiter.check_rate_limit(user_id):
        raise HTTPException(429, "Rate limit exceeded. Try again later.")

    if not limiter.check_token_budget(user_id, max_tokens):
        raise HTTPException(429, "Daily token budget exceeded.")

    # Cap output tokens
    max_tokens = min(max_tokens, AIRateLimiter.MAX_OUTPUT_TOKENS)

    response = await anthropic_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        messages=messages,
    )

    tokens_used = response.usage.input_tokens + response.usage.output_tokens
    cost = estimate_cost(response.usage)
    limiter.record_usage(user_id, tokens_used, cost)

    # Audit log
    await audit_log("AI_API_CALL", {
        "user_id": user_id,
        "model": "claude-sonnet-4-6",
        "tokens": tokens_used,
        "cost": cost,
    })

    return response.content[0].text
```

---

## 4. Abuse Detection

```python
class AIAbuseDetector:
    """Detect patterns of AI feature abuse."""

    ABUSE_PATTERNS = {
        "rapid_fire": {"threshold": 50, "window_minutes": 5},
        "large_inputs": {"threshold": 10, "min_length": 8000, "window_minutes": 30},
        "repeated_failures": {"threshold": 10, "window_minutes": 15},
    }

    async def check_and_flag(self, user_id: str, input_text: str, succeeded: bool):
        """Check for abuse patterns and flag suspicious activity."""
        # Track in time-series database or Redis
        await self.record_event(user_id, len(input_text), succeeded)

        violations = []

        # Check each pattern
        rapid = await self.count_events(user_id, minutes=5)
        if rapid > self.ABUSE_PATTERNS["rapid_fire"]["threshold"]:
            violations.append("rapid_fire")

        if not succeeded:
            failures = await self.count_failures(user_id, minutes=15)
            if failures > self.ABUSE_PATTERNS["repeated_failures"]["threshold"]:
                violations.append("repeated_failures")

        if violations:
            await audit_log("AI_ABUSE_DETECTED", {
                "user_id": user_id,
                "violations": violations,
            })
            # Auto-throttle: reduce rate limit for this user
            await self.apply_throttle(user_id, violations)
```

---

## 5. Data Isolation

Never include sensitive data in AI prompts unless absolutely necessary.

```python
def prepare_context_for_ai(records: list[dict]) -> list[dict]:
    """Strip sensitive fields before including data in AI context."""
    REDACTED_FIELDS = {"ssn", "password", "api_key", "token", "secret",
                        "credit_card", "account_number"}

    sanitized = []
    for record in records:
        clean = {}
        for key, value in record.items():
            if key.lower() in REDACTED_FIELDS:
                clean[key] = "[REDACTED]"
            elif isinstance(value, str) and len(value) > 1000:
                clean[key] = value[:1000] + "... [truncated]"
            else:
                clean[key] = value
        sanitized.append(clean)

    return sanitized
```

---

## OWASP Top 10 for LLMs — Coverage

| # | Threat | Mitigation in this file |
|---|--------|------------------------|
| LLM01 | Prompt Injection | Input sanitization, prompt structure |
| LLM02 | Insecure Output Handling | Output validation, HTML sanitization |
| LLM03 | Training Data Poisoning | N/A (use reputable model providers) |
| LLM04 | Model Denial of Service | Rate limiting, token budgets |
| LLM05 | Supply Chain Vulnerabilities | Pin SDK versions, audit dependencies |
| LLM06 | Sensitive Information Disclosure | Data isolation, PII detection |
| LLM07 | Insecure Plugin Design | Validate all tool/function call params |
| LLM08 | Excessive Agency | Limit model permissions, require confirmation |
| LLM09 | Overreliance | Output validation, human review for critical actions |
| LLM10 | Model Theft | API key protection, access logging |
