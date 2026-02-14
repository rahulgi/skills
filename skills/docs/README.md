# skills

Claude Code skills for project documentation and workflow.

## Installation

Install via [skills.sh](https://skills.sh):

```
claude skills add rahulgi/skills/docs
```

## Skills

### `/docs` — Project documentation

Agent-first documentation architecture for AI-assisted projects. Recognizes that AI agents are the primary readers and writers of project documentation.

**Two modes:**

- **Init** (`/docs init` or invoked on a project without doc structure): Scaffolds the full documentation architecture — evergreen files, design-docs/, logs/ — and adds maintenance instructions to CLAUDE.md.
- **Update** (`/docs` or `/docs update`): Reviews recent work and updates ROADMAP, logs, and design-docs as needed.

## Design rationale

### Why this exists

A "spec" is powerful in the age of AI — agents can go from idea to implementation fast, but only if they know what to build and why. This skill creates a documentation structure that:

- Gives the agent enough context to make good decisions
- Tracks what the agent does and why (it moves fast and humans need to keep up)
- Keeps everything local so agents can easily read and modify it
- Is designed agent-first — the agent is the primary author and consumer

### Documentation architecture

**Evergreen files** (top-level, stable context):

| File              | Purpose                                            |
| ----------------- | -------------------------------------------------- |
| `CLAUDE.md`       | Agent behavioral instructions ("how to work here") |
| `README.md`       | Project goal, what this is, who it's for           |
| `ARCHITECTURE.md` | System design, components, data flow               |
| `ROADMAP.md`      | Status, active work, done, wontdo                  |
| `IDEAS.md`        | Backlog, brainstorming, not-yet-ready              |
| `MARKETING.md`    | Positioning, distribution, content, experiments    |

**Transient files** (date-prefixed, append-only):

| Directory      | Naming                       | Purpose                                         |
| -------------- | ---------------------------- | ----------------------------------------------- |
| `design-docs/` | `YYYY-MM-DD-feature-name.md` | Specs, plans, decision records                  |
| `logs/`        | `YYYY-MM-DD.md`              | Daily narrative — surprises, debugging, context |

Not every project needs every file. The skill works with the user to determine which files make sense during init.

### How information flows

```
IDEAS.md → ROADMAP.md → design-docs/ → implementation → logs/
```

- Ideas land in IDEAS.md
- Promoted to ROADMAP when ready
- Get a design doc when they need planning
- Get logged during/after implementation

### Design doc format

Lightweight, not rigid:

- **Motivation** — why are we doing this?
- **Discussion** — what did we explore? options, tradeoffs, learnings
- **Decisions** — what we chose and why (with dates)
- **Plan** — concrete implementation plan the agent can execute against

Discussion is the messy middle. Plan is the clean output. An agent implementing reads Plan first; an agent understanding context reads Motivation + Decisions.

### ROADMAP format

Checkboxes + tags for scannability:

```markdown
## In progress

- [ ] Upload token flow #product — design-docs/2026-02-14-upload-tokens.md

## Done

- [x] CDN setup #infra — 2026-02-10, abc123

## Wontdo

- ~~Client-side encryption~~ #product — too complex for v1, revisit later
```

### Agent maintenance

The skill adds instructions to CLAUDE.md so the agent maintains docs as part of its normal workflow — not just when `/docs` is invoked. The key behaviors:

- After completing work: update ROADMAP and the relevant log
- When planning a non-trivial feature: create a design doc first
- When an idea comes up that isn't actionable yet: add to IDEAS.md
