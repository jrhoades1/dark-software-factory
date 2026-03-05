---
name: client-follow-up
description: >
  Post-meeting and post-interview follow-up protocol. Use this skill after any client
  meeting, interview, or significant external interaction. Handles thank-you timing,
  tone matching, relationship tracking, and follow-up scheduling. Trigger when the user
  mentions "follow up," "thank you note," "after the meeting," "post-interview,"
  "send a note," or "check in with" someone. Also applies to the job search context
  for post-interview debriefs and follow-up emails.
model: sonnet
user-invokable: true
---

# Client Follow-Up Skill

## Intent

1. **Speed matters** — A follow-up within 2-4 hours of a meeting signals professionalism and enthusiasm. Same-day is minimum. Next-day is acceptable. Two days is too late.
2. **Tone matching is critical** — Match the other person's communication style. If they're casual, be casual. If they're formal, be formal. Never be more formal than your counterpart.
3. **Reference something specific** — Generic "great to chat" emails are forgettable. Reference a specific moment, idea, or next step from the conversation.
4. **One clear next action** — Every follow-up should either confirm a next step or propose one. No dangling threads.
5. **Track everything** — Log the interaction, the follow-up, and the expected response timeline. Don't rely on memory.

## When to Use

- After a client meeting or discovery call
- After a job interview (any round)
- After a networking conversation that has potential
- When a follow-up date arrives and no response has been received
- When re-engaging a stale conversation

## Process

### Step 1: Capture the Interaction

Immediately after the meeting/interview, record:

1. **Who was there** — Names, titles, roles
2. **What was discussed** — Key topics, decisions, commitments
3. **Tone & dynamic** — Formal? Casual? Warm? Transactional?
4. **Next steps agreed** — What did each party commit to?
5. **Timeline** — When is the next touchpoint expected?
6. **Signals** — Positive, neutral, or concerning indicators

Store this in the project's `communications/` directory as a dated markdown file.

### Step 2: Draft the Follow-Up

**Timing rules:**
| Context | Send within | Format |
|---------|-------------|--------|
| Client meeting (first) | 2-4 hours | Email |
| Client meeting (ongoing) | Same day | Email |
| Job interview | 2-4 hours | Email |
| Networking coffee | Same day | Email or LinkedIn |
| They owe you something | Day after their stated timeline | Email |
| No response to your follow-up | 1 week | Brief check-in |

**Structure:**
1. **Opening** — Reference something specific from the conversation (not "great to meet you")
2. **Value add** — Reinforce why this matters / what excited you (1-2 sentences max)
3. **Next step** — Confirm what was agreed, or propose one
4. **Close** — Short, warm, matches their tone

**Length:** Under 150 words for standard follow-ups. Nobody wants to read an essay.

### Step 3: Tone Match

Read any prior communication from the person. Match:
- **Length** — If they write 3 sentences, you write 3-5 sentences
- **Formality** — If they sign "Jackie" not "Jackie Rafter, MBA", you sign "Jimmy"
- **Emoji/punctuation** — If they use exclamation marks, you can too. If they don't, don't.
- **Structure** — If they write in paragraphs, mirror that. If they use bullets, mirror that.

See `references/tone-patterns.md` for examples.

### Step 4: Schedule Follow-Up Tracking

Set a follow-up date based on:
- **They gave a timeline:** Follow up the day after their stated deadline
- **No timeline given:** Follow up in 1 week
- **High-stakes (job interview final round):** Follow up in 3-5 business days
- **Low-stakes (networking):** Follow up in 2 weeks

Log the follow-up date in the project's tracking system or daily log.

### Step 5: The Re-Engage (When They Go Silent)

If no response after your follow-up:
1. **Wait the full interval** — Don't send multiple messages in rapid succession
2. **Change the angle** — Don't just "bumping this up." Add new value: an article, an idea, a relevant update
3. **Keep it short** — 2-3 sentences max
4. **Know when to stop** — After 2 unanswered follow-ups, move to passive tracking. Don't chase.

## Rules

- Always check `communications/` for prior tone before drafting
- Never send a follow-up without user review and approval
- Log every follow-up to the daily log
- If the user says "draft a follow-up," produce it but do NOT send it
- Reference the guardrails rule: no external communications without explicit confirmation
