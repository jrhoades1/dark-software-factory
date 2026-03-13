# Port Registry

Centralized dev server port assignments. Prevents collisions when running multiple projects.

## Assignments

| Port | Project | Stack | Path |
|------|---------|-------|------|
| 3001 | higher-landing | Next.js | `~/Projects/higher-landing` |
| 3002 | job-applications | Next.js (monorepo) | `~/Projects/job-applications` |
| 3003 | job-app-assistant | Next.js | `~/Projects/job-app-assistant` |
| 3004 | jimmys-plan | Next.js | `~/Projects/jimmys-plan` |
| 3005 | vent-thread | Next.js | `~/Projects/vent-thread` |

**Reserved:** 3000 (default — never assign, acts as collision canary)
**Range:** 3001–3099 for web dev servers

## How to use

1. When bootstrapping a new project, pick the next available port from this registry
2. Add `DEV_PORT=<port>` to the project's `.env.local`
3. Update `package.json` dev script: `"dev": "next dev --port ${DEV_PORT:-<port>}"`
4. Update Playwright config `baseURL` and `webServer.url` if applicable
5. Add the assignment to this table

## Non-web projects (no port needed)

- ald-call-analysis (Python CLI)
- Easter Island (Python agents)
- AIOS (Python agents)
- servicetitan-mcp-server (MCP protocol, not HTTP)
