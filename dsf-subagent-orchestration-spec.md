# DSF Subagent Orchestration Spec

## The Problem

Complex DSF workflows — healthcare platform builds, ServiceTitan integrations, HIPAA-compliant data pipelines — involve multiple competing concerns that a single agent handles sequentially. This creates bottlenecks: the agent context-switches between compliance checking, integration logic, architecture decisions, and testing. Worse, when a compliance issue surfaces late, it unwinds work the agent already committed to.

The Claude Code team learned this with Todos → Tasks: subagents need to **coordinate on shared state with dependencies**, not just check items off a list. DSF needs an orchestration layer that decomposes complex workflows into specialized subagents that communicate through a structured protocol.

## Design Principles

1. **Intent Blocks govern, agents execute.** The orchestrator doesn't make priority decisions — Intent Blocks do. Agents inherit the resolved intent hierarchy and operate within those constraints.
2. **Compliance is a gate, not a lane.** The compliance agent doesn't run in parallel — it's a checkpoint that other agents must pass through. This mirrors real-world regulated development where you can't merge without security review.
3. **Progressive disclosure across agents.** Subagents don't load the full project context. They discover what they need through the orchestrator's context broker. This keeps individual agent windows clean and focused.
4. **Fail fast, fail upstream.** If a subagent hits a blocking issue (e.g., a HIPAA violation in the data model), it escalates immediately rather than continuing downstream work that will be invalidated.

---

## Subagent Roles

### 1. Orchestrator (meta-agent)
**Purpose:** Decomposes work, manages the task graph, brokers context between agents, handles escalation.

Not a "manager" that micromanages — more like a dispatch system that:
- Parses the initial Intent Block into a task graph
- Assigns tasks to specialized agents
- Maintains shared state (what's done, what's blocked, what changed)
- Detects when an agent's output invalidates another agent's assumptions
- Surfaces decisions that require human input

### 2. Architecture Agent
**Purpose:** System design, data modeling, infrastructure decisions, API design.

Operates first in most workflows. Its outputs become constraints for downstream agents:
- Data models → Integration Agent needs these for mapping
- API contracts → Quality Agent needs these for test generation
- Infrastructure choices → Operations Agent needs these for deployment

### 3. Integration Agent
**Purpose:** External system connections — FHIR/HL7, ServiceTitan, Epic, third-party APIs.

Specializes in:
- Protocol-specific implementation (FHIR resources, HL7 message parsing)
- Authentication/authorization flows with external systems
- Data transformation and mapping between systems
- Retry/resilience patterns for external calls

### 4. Compliance Agent
**Purpose:** HIPAA scaffolding, security hardening, audit trail verification, PHI handling.

Operates as a **gate** — other agents submit work products for compliance review:
- Data model review (PHI field identification, encryption requirements)
- API endpoint review (authentication, authorization, audit logging)
- Infrastructure review (encryption at rest/in transit, access controls)
- Code review (no PHI in logs, proper error handling that doesn't leak data)

### 5. Quality Agent
**Purpose:** Test generation, validation logic, error handling patterns.

Works from contracts produced by Architecture and Integration agents:
- Generates test suites from API contracts
- Builds validation schemas from data models
- Creates error handling patterns appropriate to the domain
- Produces integration test scenarios for external system connections

### 6. Operations Agent
**Purpose:** Deployment configuration, monitoring, observability, CI/CD.

Consumes outputs from all other agents:
- Infrastructure-as-code from Architecture Agent's decisions
- Health checks for Integration Agent's external connections
- Compliance monitoring dashboards from Compliance Agent's requirements
- Test pipeline configuration from Quality Agent's test suites

---

## New Skills

### Skill 1: `agent-orchestrator`
**Location:** `/skills/agent-orchestrator/SKILL.md`

**Responsibility:** The entry point. Reads the project's Intent Block, decomposes it into a task graph, and manages the execution lifecycle.

**Key behaviors:**
- Parse Intent Block into discrete tasks with explicit dependencies
- Determine which subagent owns each task
- Maintain a shared `TASK_STATE.md` file that all agents can read
- Detect dependency violations (agent B started before agent A's prerequisite was met)
- Handle re-planning when a gate rejection invalidates downstream tasks

**Task State Schema:**
```yaml
# TASK_STATE.md - maintained by orchestrator, read by all agents
project: "ald-servicetitan-pipeline"
intent_block: "./INTENT_BLOCK.md"
status: "in_progress"

tasks:
  - id: "arch-001"
    agent: "architecture"
    title: "Design technician performance data model"
    status: "complete"  # pending | in_progress | complete | blocked | rejected
    dependencies: []
    outputs:
      - path: "./models/technician-performance.ts"
        type: "data_model"
    
  - id: "integ-001"
    agent: "integration"
    title: "ServiceTitan API data extraction"
    status: "in_progress"
    dependencies: ["arch-001"]
    inputs:
      - from_task: "arch-001"
        artifact: "./models/technician-performance.ts"
    outputs: []
    
  - id: "compliance-gate-001"
    agent: "compliance"
    title: "PHI review of data model and extraction pipeline"
    status: "pending"
    type: "gate"
    dependencies: ["arch-001", "integ-001"]
    gate_criteria:
      - "No PHI in log outputs"
      - "Encryption at rest for all technician PII"
      - "Audit trail for data access"
    
  - id: "quality-001"
    agent: "quality"
    title: "Generate test suite for extraction pipeline"
    status: "blocked"
    dependencies: ["compliance-gate-001"]  # can't test until compliance passes
    blocked_by: "compliance-gate-001"

escalations: []
human_decisions_needed: []
```

### Skill 2: `agent-handoff`
**Location:** `/skills/agent-handoff/SKILL.md`

**Responsibility:** Protocol for passing context between agents. Solves the core problem: subagents don't share a context window, so they need a structured way to communicate what they did, what they decided, and what the next agent needs to know.

**Handoff Document Schema:**
```yaml
# Generated by completing agent, consumed by next agent
handoff:
  from_agent: "architecture"
  from_task: "arch-001"
  to_agent: "integration"
  to_task: "integ-001"
  
  # What was done
  summary: "Designed technician performance data model with 3 entities..."
  
  # What the next agent needs to know
  context:
    - type: "constraint"
      detail: "revenue_per_job is calculated, not stored — derive from invoice total / job count"
    - type: "decision"
      detail: "Used composite key (technician_id + period) instead of auto-increment — matches ServiceTitan's natural key"
    - type: "warning"
      detail: "ServiceTitan API rate limit is 100 req/min — extraction must batch"
  
  # Files the next agent should read
  artifacts:
    - path: "./models/technician-performance.ts"
      relevance: "Primary data model — map ServiceTitan fields to these types"
    - path: "./docs/api-contracts.md"
      relevance: "Endpoint specs the integration must implement"
  
  # What the next agent should NOT do
  constraints:
    - "Do not modify the data model — raise an issue via escalation if it doesn't fit"
    - "Do not store raw ServiceTitan responses — transform to our model immediately"
```

**Why this matters:** Without structured handoffs, the next agent either gets too little context (and makes conflicting decisions) or too much (and wastes its context window on irrelevant details). The handoff document is progressive disclosure applied to agent-to-agent communication.

### Skill 3: `compliance-gate`
**Location:** `/skills/compliance-gate/SKILL.md`

**Responsibility:** Formalizes the compliance checkpoint pattern. This is distinct from the existing `hipaa-scaffold` and `security-hardening` skills — those generate compliant code. This skill **reviews and gates** code that other agents produced.

**Gate Protocol:**
1. Orchestrator triggers gate when all prerequisite tasks are complete
2. Compliance agent receives the gate criteria + artifacts to review
3. Agent produces a **Gate Review Document**:

```yaml
gate_review:
  gate_id: "compliance-gate-001"
  status: "rejected"  # passed | rejected | conditional
  
  findings:
    - severity: "blocking"
      location: "./services/extraction.ts:47"
      issue: "Technician name logged in plain text during extraction error"
      remediation: "Replace with technician_id in error log, move name to audit-only log"
      assigned_to_task: "integ-001"  # sends back to integration agent
      
    - severity: "blocking"
      location: "./models/technician-performance.ts:12"
      issue: "phone_number field lacks encryption-at-rest annotation"
      remediation: "Add @encrypted decorator, ensure migration includes column-level encryption"
      assigned_to_task: "arch-001"  # sends back to architecture agent
      
    - severity: "advisory"
      issue: "Consider adding data retention policy — ServiceTitan data older than 24mo may need purging"
      remediation: "Add retention_policy field to model metadata"

  # If conditional: what must be fixed before proceeding
  conditions_for_pass:
    - "Fix both blocking findings"
    - "Re-submit for gate review"
    
  # What passed
  approved:
    - "Audit trail implementation covers all CRUD operations"
    - "API authentication uses OAuth2 with proper token rotation"
    - "Error responses do not leak PHI"
```

4. On rejection: orchestrator re-opens the relevant upstream tasks with the remediation instructions
5. On pass: downstream tasks are unblocked
6. On conditional: orchestrator creates remediation tasks and schedules a re-review

### Skill 4: `task-graph`
**Location:** `/skills/task-graph/SKILL.md`

**Responsibility:** The dependency resolution engine. Determines execution order, detects cycles, identifies parallelizable work, and handles invalidation cascading.

**Key behaviors:**
- Build DAG from task dependencies
- Identify tasks that can run in parallel (no shared dependencies)
- When a gate rejects: walk the dependency graph to identify all downstream tasks that must be re-evaluated
- When a task's output changes: determine which downstream tasks consumed that output and flag them for re-execution
- Detect deadlocks (circular dependencies between agents)

**Parallelization Example:**
```
Intent Block parsed → 
  ├── arch-001 (data model)          ← runs first, no deps
  ├── arch-002 (API contracts)       ← runs first, no deps
  │
  ├── integ-001 (extraction)         ← depends on arch-001
  ├── integ-002 (API implementation) ← depends on arch-002
  │   (these two CAN run in parallel)
  │
  ├── compliance-gate-001            ← depends on integ-001 AND integ-002
  │   (BLOCKS until both complete)
  │
  ├── quality-001 (test suite)       ← depends on compliance-gate-001
  ├── ops-001 (deployment config)    ← depends on compliance-gate-001
  │   (these two CAN run in parallel)
  │
  └── ops-002 (go-live checklist)    ← depends on quality-001 AND ops-001
```

### Skill 5: `intent-resolver`
**Location:** `/skills/intent-resolver/SKILL.md`

**Responsibility:** Evolves your existing Intent Block methodology for multi-agent contexts. When agents have competing needs, the intent resolver determines which priority wins.

**The problem it solves:**
- Architecture Agent wants to add a caching layer for performance
- Compliance Agent flags that caching PHI creates a new attack surface
- Integration Agent needs the cache to stay within ServiceTitan's rate limits

Single-agent DSF handles this internally. Multi-agent DSF needs a resolution protocol:

```yaml
intent_conflict:
  id: "conflict-007"
  description: "Caching layer tradeoff — performance vs. compliance vs. rate limits"
  
  positions:
    - agent: "architecture"
      intent: "Add Redis cache for ServiceTitan responses"
      priority_served: "performance"
      
    - agent: "compliance"
      intent: "No caching of PHI-containing responses"
      priority_served: "security"
      
    - agent: "integration"
      intent: "Need caching to stay under 100 req/min rate limit"
      priority_served: "reliability"
  
  # Resolution based on Intent Block priority hierarchy
  resolution:
    approach: "Cache with PHI stripping"
    detail: "Cache ServiceTitan responses but strip PHI fields before cache write. Cache contains only operational metrics (job counts, revenue, timestamps). PHI fields re-fetched on demand with audit logging."
    satisfies:
      - "performance: operational queries served from cache"
      - "security: no PHI in cache layer"  
      - "reliability: rate limit managed for operational data; PHI fetches are infrequent"
    tradeoffs:
      - "PHI-dependent queries are slower (no cache)"
      - "Additional complexity in cache write logic"
    
  decided_by: "intent_hierarchy"  # or "human_escalation" if priorities are equal
  escalated_to_human: false
```

### Skill 6: `agent-context-broker`
**Location:** `/skills/agent-context-broker/SKILL.md`

**Responsibility:** Manages what each agent can see. Prevents context pollution while ensuring agents have what they need.

**The problem:** Without a broker, you either:
- Give every agent full project context (wastes tokens, creates confusion)
- Give agents too little (they make decisions that conflict with other agents' work)

**Broker behaviors:**
- Maintains a context manifest for each agent role (what files/docs they need)
- When an agent requests context, broker provides only relevant artifacts
- When an agent produces output, broker determines which other agents need to know
- Tracks context freshness — if an artifact was updated since an agent last read it, flag it

**Context Manifest Example:**
```yaml
agent_context:
  integration:
    always_loaded:
      - "./INTENT_BLOCK.md"
      - "./TASK_STATE.md"
      - "./models/*.ts"                    # needs data models
      - "./docs/api-contracts.md"          # needs API specs
    loaded_on_request:
      - "./infrastructure/redis.config.ts" # only if caching is relevant
      - "./docs/servicetitan-api.md"       # only for ServiceTitan tasks
    never_loaded:
      - "./tests/**"                       # not this agent's concern
      - "./deployment/**"                  # not this agent's concern
      - "./compliance-reviews/**"          # reads gate results, not full reviews
```

---

## Implementation Sequence

### Phase 1: Foundation (build first)
1. **`task-graph`** — Without dependency resolution, nothing else works
2. **`agent-handoff`** — Agents need to talk before they can coordinate
3. **`agent-orchestrator`** — Wire the first two together

**Validation:** Re-run the ALD ServiceTitan case study as a multi-agent workflow. The 30-minute analysis becomes the test case. Did the agents decompose the work correctly? Did the self-correction (3.3% → 9.5%) still happen, and did it happen faster because the compliance/quality agents caught it earlier?

### Phase 2: Governance (healthcare differentiator)
4. **`compliance-gate`** — This is where DSF becomes uniquely valuable for healthcare
5. **`intent-resolver`** — Handle the inevitable conflicts between agents

**Validation:** Run a HIPAA-compliant build (e.g., patient data pipeline) through the full orchestration. Compliance gates should catch issues that single-agent DSF would have missed or caught later.

### Phase 3: Optimization
6. **`agent-context-broker`** — Reduce token waste, improve agent focus

**Validation:** Measure context window utilization before and after broker. Agents should use less context while maintaining the same output quality.

---

## What This Means for the Business

This orchestration layer turns DSF from a "really good way to use Claude" into a **platform**. Here's why:

**For consulting (Rhoades AI):** You're not just building apps — you're building multi-agent systems that self-coordinate. The compliance-gate pattern alone is a differentiator for healthcare clients who currently rely on manual code review for HIPAA compliance.

**For framework sales (IntentStack):** These skills are the product. A company buys the orchestration skills, customizes the agent roles for their domain, and gets a repeatable multi-agent development process. The intent-resolver and compliance-gate skills are where the IP lives.

**For the Ensemble interview:** This spec demonstrates exactly the kind of technical leadership thinking a VP Engineering should bring. You're not just managing teams — you're designing systems where AI agents operate like well-structured engineering teams with clear ownership, handoff protocols, and quality gates. That's a vision most companies haven't articulated yet.

**Pricing angle:** Individual skills are the shovel. The orchestration layer is the mining operation. Sell skills à la carte for simple use cases, but the orchestration suite is the premium tier — because that's where the compounding value lives.
