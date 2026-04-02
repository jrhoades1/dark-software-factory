# LLM Council — Trigger Evaluation Tests

## Should Trigger (mandatory)

| Input | Expected |
|-------|----------|
| "Council this: should I raise prices?" | TRIGGER |
| "Run the council on my positioning" | TRIGGER |
| "War room this pricing decision" | TRIGGER |
| "Pressure-test this go-to-market strategy" | TRIGGER |
| "Stress-test this product idea" | TRIGGER |
| "Debate this: monorepo vs polyrepo for our stack" | TRIGGER |

## Should Trigger (strong — genuine decision with stakes)

| Input | Expected |
|-------|----------|
| "Should I hire a VA or build an automation? Here's the context..." | TRIGGER |
| "I'm torn between launching a $97 workshop or a $497 course" | TRIGGER |
| "Which of these 3 positioning angles is strongest?" | TRIGGER |
| "Is this the right move? I'm thinking of pivoting from consulting to SaaS" | TRIGGER |
| "I can't decide between Next.js and Remix for this client project" | TRIGGER |
| "Validate this: I want to charge $5k/month for this service" | TRIGGER |

## Should NOT Trigger

| Input | Expected |
|-------|----------|
| "What's the capital of France?" | NO TRIGGER |
| "Write me a tweet about our launch" | NO TRIGGER |
| "Summarize this article" | NO TRIGGER |
| "Should I use markdown?" | NO TRIGGER (trivial, no real tradeoff) |
| "Can you help me debug this function?" | NO TRIGGER |
| "What does this error mean?" | NO TRIGGER |
| "Should I use tabs or spaces?" | NO TRIGGER (low stakes) |
| "How do I deploy to Vercel?" | NO TRIGGER (procedural, one answer) |
