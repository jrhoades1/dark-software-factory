---
name: communication-profiles
description: >
  Build and maintain communication profiles for key stakeholders on any project.
  Use when drafting emails, follow-ups, or any outbound communication to ensure
  tone matching. Also use when onboarding a new project to capture stakeholder
  communication styles from existing email chains. Trigger when the user mentions
  "communication profile," "tone profile," "how does [person] communicate,"
  "draft an email to [person]," "match their tone," or "build a profile for."
model: sonnet
user-invokable: true
---

# Communication Profiles

Build structured profiles of how key stakeholders communicate so that every outbound message matches their expected tone and style.

## Intent

1. **Tone mismatch kills trust** -- Sending a formal email to someone who writes casual two-liners signals you're not paying attention. Matching someone's communication style is the fastest way to build rapport.
2. **Profiles are evidence-based** -- Never guess at someone's style. Build profiles from real emails, messages, and meeting notes. Minimum 2-3 samples before creating a profile.
3. **One profile per person** -- Each stakeholder gets their own file. Profiles are referenced by any skill that drafts outbound communication (client-follow-up, cover-letter-writer, etc.).
4. **Profiles evolve** -- Update profiles as you accumulate more communication samples. People's tone may shift as relationships deepen.
5. **Include anti-patterns** -- Knowing what NOT to do is as valuable as knowing what to do. Every profile should list things that would land wrong.

## When to Use

- Onboarding a new project with existing email chains
- Before drafting any email, message, or follow-up to a profiled stakeholder
- When the user says "draft an email to [person]" -- check for their profile first
- When new communication samples arrive (emails, meeting transcripts)
- When a tone mismatch is flagged ("that doesn't sound like something Jackie would appreciate")

## Process

### Step 1: Gather Samples

Collect 2-3+ real communication samples from the person. Sources:
- Email chains in `communications/`
- Meeting notes or transcripts
- Slack/Teams messages
- LinkedIn messages

Read each sample carefully. Do NOT proceed to profile creation with fewer than 2 samples.

### Step 2: Analyze Patterns

For each sample, note:

| Dimension | What to Look For |
|-----------|-----------------|
| **Greeting** | "Hi Jimmy" vs "Hey!" vs jumping straight in |
| **Length** | Word count, sentence count. Do they write 2 lines or 2 paragraphs? |
| **Structure** | Paragraphs vs bullets vs stream-of-consciousness |
| **Formality** | Full name sign-off vs first name vs no sign-off |
| **Punctuation** | Exclamation marks, ellipses, emojis, ALL CAPS |
| **Warmth** | Personal touches, humor, compliments, small talk |
| **Directness** | Do they get to the point or build up to it? |
| **Delegation** | Do they hand off to others? Who? |
| **Response time** | Fast responder? Batches replies? |
| **Signature** | Full block, first name only, none |

### Step 3: Create the Profile

Use the template at `references/profile-template.md`. Store profiles in the project's `communications/profiles/` directory:

```
project/
  communications/
    profiles/
      firstname-lastname.md    # One file per person
```

### Step 4: Extract Good/Bad Examples

From the real samples, create:
- **Mirror examples** -- "If they write X, respond with Y"
- **Anti-patterns** -- "Never do Z with this person"

These go in the `## Tone Examples` section of each profile.

### Step 5: Cross-Reference

After creating profiles, check for relationship dynamics:
- Who defers to whom?
- Who should be CC'd vs TO?
- Who is the decision maker vs the operator?
- What is the communication chain? (e.g., "Always email Erin directly, CC Jackie")

Document these in a `_dynamics.md` file in the profiles directory.

## Integration with Other Skills

Communication profiles are consumed by:
- **client-follow-up** -- Reads profile before drafting any follow-up
- **cover-letter-writer** -- Adapts tone for the target reader
- **Any skill that drafts outbound communication** -- Should check `communications/profiles/` first

When drafting a message to a profiled person:
1. Read their profile
2. Match greeting, length, formality, and structure
3. Check anti-patterns before sending
4. If the profile doesn't exist yet, flag it: "No profile found for [person]. Want me to build one from available communications?"

## Rules

- Never create a profile from fewer than 2 real samples
- Never guess at communication style -- always base on evidence
- Update profiles when new samples contradict existing patterns
- Profiles contain NO confidential content -- only style observations
- Always get user approval before using a profile to draft communication
- Store profiles in the project, not in the DSF framework (they're project-specific data)
