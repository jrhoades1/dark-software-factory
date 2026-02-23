---
name: hipaa-scaffold
description: >
  Layer HIPAA compliance requirements onto any project. Adds audit logging middleware,
  PHI boundary enforcement, encryption configuration, BAA documentation, access control
  patterns, and compliance verification. Use this skill whenever the user mentions HIPAA,
  PHI, protected health information, healthcare compliance, BAA, ePHI, or is building any
  application that handles patient data, medical records, claims, eligibility, encounters,
  health plan information, or provider data. Also trigger when the project involves
  Medicare, Medicaid, Medicare Advantage, value-based care, EHR integration, HL7, FHIR,
  or any health plan administration. This skill layers ON TOP of an existing project —
  if no project exists yet, use project-bootstrap first. Always pair with
  security-hardening for the full Enforce step.
---

# HIPAA Scaffold Skill

Add HIPAA compliance infrastructure to an existing application. This skill assumes
a project structure already exists (via project-bootstrap or manually created).

## When this skill applies

Any application that handles Protected Health Information (PHI):
- Patient demographics (name, DOB, address, SSN, MRN)
- Medical records, diagnoses, procedures, lab results
- Health insurance information (plan ID, member ID, claims)
- Payment/billing information tied to healthcare services
- Provider information (NPI, DEA, credentials)
- Any of the 18 HIPAA identifiers

## What this skill adds

### 1. PHI Data Boundary Enforcement

All PHI must be isolated into clearly marked modules. The goal: any developer (or Claude)
can instantly identify which code touches PHI.

**Directory convention:**
```
src/
├── phi/                    # ALL PHI handling lives here
│   ├── README.md           # "This directory handles PHI. Review HIPAA rules."
│   ├── models/             # PHI data models with encryption annotations
│   ├── services/           # PHI business logic
│   ├── middleware/          # PHI access logging, consent verification
│   └── encryption/         # Field-level encryption utilities
├── api/                    # Non-PHI API routes
│   └── phi-routes/         # PHI-specific routes (clearly separated)
└── shared/                 # No PHI allowed here — ever
```

**Model annotations:**
```python
class Patient(Base):
    """⚠️ CONTAINS PHI — All access must be audit-logged."""
    __tablename__ = "patients"

    id = Column(UUID, primary_key=True)
    mrn = Column(String, unique=True)          # PHI: Medical Record Number
    first_name = Column(EncryptedString)        # PHI: encrypted at rest
    last_name = Column(EncryptedString)         # PHI: encrypted at rest
    date_of_birth = Column(EncryptedDate)       # PHI: encrypted at rest
    ssn = Column(EncryptedString, nullable=True) # PHI: encrypted, field-level
    # ... non-PHI fields below
    created_at = Column(DateTime, default=func.now())
```

### 2. Audit Logging Middleware

HIPAA requires logging every access to PHI: who accessed what, when, from where.

**FastAPI middleware:**
```python
from datetime import datetime
from fastapi import Request

async def phi_audit_middleware(request: Request, call_next):
    """Log every PHI access for HIPAA audit trail."""
    response = await call_next(request)

    if request.url.path.startswith("/api/phi"):
        await audit_log.create(
            event_type="PHI_ACCESS",
            user_id=request.state.user.id,
            resource_path=request.url.path,
            method=request.method,
            status_code=response.status_code,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            timestamp=datetime.utcnow(),
            # DO NOT log request/response bodies — they contain PHI
        )

    return response
```

**Audit log retention:** HIPAA requires 6 years minimum. Configure accordingly.

### 3. Encryption Requirements

| Data State | Requirement | Implementation |
|-----------|-------------|----------------|
| At rest (database) | AES-256 | AWS RDS encryption, or application-level |
| At rest (files) | AES-256 | S3 SSE-KMS |
| In transit | TLS 1.2+ | HTTPS everywhere, enforce TLS 1.3 |
| Field-level (high sensitivity) | AES-256-GCM | SSN, financial data — application-level |
| Backups | Encrypted | Same standard as primary storage |

### 4. Access Control Patterns

**Minimum Necessary Rule:** Users should only access the minimum PHI necessary for their
job function. Implement role-based access:

| Role | PHI Access | Example |
|------|-----------|---------|
| Provider | Full patient records they're treating | Dr. Smith sees her patients |
| Billing | Claims + limited demographics | Biller sees codes + member ID |
| Admin | User management, no clinical data | IT admin manages accounts |
| Analyst | De-identified/aggregated only | Reports use anonymized data |
| Auditor | Read-only audit logs | Compliance reviews access logs |

**RLS for HIPAA:**
```sql
-- Providers see only their patients
CREATE POLICY "provider_patient_access" ON patients
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM provider_patient_assignments
      WHERE provider_id = auth.uid()
        AND patient_id = patients.id
        AND assignment_active = true
    )
  );
```

### 5. BAA (Business Associate Agreement) Requirements

Before using ANY third-party service that may access PHI:

```
[ ] BAA signed with service provider
[ ] BAA covers the specific use case
[ ] Service provider is HIPAA-compliant (verify, don't trust)
[ ] Data processing agreement in place
```

**Common services requiring BAAs:**
- Cloud provider (AWS, GCP, Azure) — all offer BAAs
- Database hosting (Supabase, RDS, Cloud SQL)
- Email service (if sending PHI-containing emails — avoid if possible)
- Analytics (only if processing PHI — prefer de-identified data)
- AI/LLM providers (if PHI is in prompts — use extreme caution)

**⚠️ AI/LLM + PHI:** Do NOT send raw PHI to AI APIs unless:
1. BAA is signed with the AI provider
2. Data is processed in a HIPAA-compliant environment
3. PHI is minimized (only what's necessary)
4. Audit logging captures all AI interactions involving PHI

### 6. HIPAA Security Rule Technical Safeguards

```
[ ] Access Control (§164.312(a))
    [ ] Unique user identification
    [ ] Emergency access procedure
    [ ] Automatic logoff (session timeout)
    [ ] Encryption and decryption of ePHI

[ ] Audit Controls (§164.312(b))
    [ ] Hardware, software, and procedural mechanisms to record PHI access
    [ ] 6-year log retention minimum

[ ] Integrity Controls (§164.312(c))
    [ ] Mechanism to authenticate ePHI
    [ ] Protect against improper alteration or destruction

[ ] Transmission Security (§164.312(e))
    [ ] Integrity controls for data in transit
    [ ] Encryption of ePHI in transit (TLS 1.2+)

[ ] Person/Entity Authentication (§164.312(d))
    [ ] Verify identity of person seeking PHI access
    [ ] MFA for privileged access
```

### 7. Compliance Verification Script

Run before any deployment of HIPAA-regulated applications:

```bash
# PHI boundary check — no PHI outside phi/ directory
grep -r "ssn\|date_of_birth\|medical_record" src/ \
  --exclude-dir=src/phi \
  --exclude-dir=node_modules \
  --exclude-dir=.git

# Encryption verification
# Verify database encryption is enabled
# Verify TLS configuration

# Audit log verification
# Confirm audit logging is active and writing
# Check retention policy is configured

# Access control verification
# Verify RLS policies exist on all PHI tables
# Verify role-based access is enforced
```

## Healthcare Integration Patterns

For projects involving EHR/claims integration:

| Standard | Use Case | Reference |
|----------|----------|-----------|
| HL7 v2 | Legacy EHR messages (ADT, ORM, ORU) | HL7.org |
| FHIR R4 | Modern API-based data exchange | hl7.org/fhir |
| X12 837/835 | Claims submission and remittance | X12.org |
| NCPDP | Pharmacy claims | NCPDP.org |
| CCD/C-CDA | Clinical document exchange | HL7 CDA |

**FHIR security requirements:**
- SMART on FHIR for authorization
- OAuth 2.0 with PKCE
- Scope-based access (patient/*.read, etc.)
- Audit logging of all FHIR operations
