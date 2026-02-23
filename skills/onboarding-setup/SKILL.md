---
name: onboarding-setup
description: >
  Beginner-safe setup guide for Claude Code development environments. Includes VS Code
  and Claude Code installation, security training, safe permission handling, and first
  project initialization. Use this skill when onboarding new team members, setting up a
  new development machine, or when a beginner asks how to get started with Claude Code,
  AI-assisted development, or the Dark Software Factory. Also trigger for "how do I set
  up Claude Code," "first time setup," "install Claude," "new developer onboarding,"
  or "teach me to use Claude Code safely." This skill prioritizes security education
  BEFORE giving access to dangerous operations.
---

# Onboarding & Setup Skill

Set up Claude Code safely with security training integrated into the installation process.
Security education comes BEFORE access to dangerous operations — not after.

## Who this is for

- First-time Claude Code users
- Team members being onboarded
- Developers setting up new machines
- Anyone asking "how do I get started?"

## Setup Sequence

### Step 1: Install prerequisites

1. **VS Code** — Download from code.visualstudio.com
2. **Node.js 18+** — Download LTS from nodejs.org (required for Claude CLI)
3. Verify: `node --version` should show v18 or higher

### Step 2: Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

Verify: `claude --version` should return a version number.

### Step 3: Install VS Code extension

1. Open VS Code
2. Extensions sidebar (Ctrl+Shift+X)
3. Search "Claude Code"
4. Install the official Anthropic extension

### Step 4: Sign in

Run `claude` in the terminal and follow the authentication prompts.
You'll sign in with your Anthropic account.

### Step 5: Create project folder

```bash
mkdir my-project
cd my-project
```

### Step 6: Add framework files

Copy the Dark Software Factory files into your project:

```bash
# Copy global CLAUDE.md (security rules — always loaded)
cp path/to/dark-software-factory/global/CLAUDE.md ./CLAUDE.md

# Create project-specific config
touch CLAUDE.project.md
```

Edit `CLAUDE.project.md` with your stack details:
```markdown
# CLAUDE.project.md

## Stack
- Framework: [Next.js / FastAPI / etc.]
- Package manager: [pnpm / npm / pip]
- Language: [TypeScript / Python]

## Available CLI Tools
- [List tools: magick, ffmpeg, jq, etc.]

## Resource Limits
- Max file upload: 20MB
```

---

## ⚠️ Security Training (READ BEFORE STEP 7)

This section is intentionally placed BEFORE your first Claude session.

### The Permission Model

Claude Code will ask permission before running commands. You'll see prompts like:
"Allow Claude to run `npm install express`?"

**Your job: READ before clicking Allow.**

### Safe permissions ✅

These are generally safe to approve:
- `npm install` / `pip install` — Installing packages
- `mkdir`, `touch`, `cp` — Creating files and directories
- `npm run dev` — Starting dev server
- `git add`, `git commit` — Version control
- Reading files in your project directory

### Dangerous permissions ❌

STOP and think carefully before approving:
- `rm -rf` anything — Deletion is permanent
- `curl | bash` — Running unknown scripts from the internet
- `chmod 777` — Making files world-writable
- `sudo` anything — Admin access
- Modifying files OUTSIDE your project directory
- Any command you don't understand

### 🚫 NEVER click "Always Allow"

As a beginner, NEVER use "Always Allow." Always review each command individually.
The 2 seconds it takes to read a command could save hours of recovery.

### What gets sent to Anthropic

- Your prompts and Claude's responses
- File contents that Claude reads (within your project)
- Command outputs

**NOT sent:** Files Claude doesn't read, other projects, system files, browser data.

### Protect your secrets

**NEVER share with Claude Code:**
- API keys, tokens, passwords
- .env file contents (Claude should read the structure, not the values)
- SSH private keys
- Database credentials with real data
- Production configuration files
- Client confidential documents

### Emergency stop

If Claude is doing something wrong:
1. **Ctrl+C** — Stop the current command
2. **Close terminal** — Kill the session
3. **Check git status** — See what changed: `git diff`
4. **Undo if needed** — `git checkout .` to revert uncommitted changes

---

## Step 7: Initialize your first session

```bash
cd my-project
claude
```

**For a new app build:**
```
Let's build [your app idea]. Read CLAUDE.md for security standards,
then follow the citadel-workflow skill for the build process.
```

**For an existing project:**
```
Read CLAUDE.md and CLAUDE.project.md to understand the project.
Then help me with [specific task].
```

## Step 8: Security checklist

Before writing any code, complete this:

### 1. Create .gitignore
```
# Secrets
.env
.env.local
.env.*.local
*.pem
*.key

# Dependencies
node_modules/
__pycache__/
.venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Build
dist/
build/
.next/

# Claude
.claude/settings.local.json
```

### 2. Initialize git
```bash
git init
git add .gitignore
git commit -m "Initial commit with .gitignore"
```

### 3. Create billing code
```bash
mkdir -p .claude
echo "PROJECT-CODE" > .claude/project-code.txt
```

### 4. Verify .gitignore before first push
```bash
# These should all return nothing:
git status | grep ".env"
git status | grep "node_modules"
git status | grep ".pem"
```

## 🚩 Red Flags — When to STOP

Stop and ask for help if Claude:
- Suggests running commands you don't understand
- Wants to modify files outside your project
- Tries to install global packages without explanation
- Generates code that handles passwords or API keys in plain text
- Suggests disabling security features to "make it work"
- Asks to run `sudo` commands
- Wants to modify system configuration files

## Quick Reference

**Safe:** `npm install`, `mkdir`, `git commit`, reading project files
**Dangerous:** `rm -rf`, `sudo`, `curl | bash`, `chmod 777`, modifying system files
**NEVER:** Share secrets, click "Always Allow," run commands you don't understand
