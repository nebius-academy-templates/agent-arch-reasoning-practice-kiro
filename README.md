# Practice — Building an Architecture Reasoning Agent (Kiro IDE edition)

In this practice you will build agents from scratch: an engineering team lead chatbot, an architecture reasoning orchestrator, and an RFC writer sub-agent. The tools and data are provided — your job is to write the agent instructions.

Everything runs inside **Kiro IDE**. You open the repository **once** at its root and switch between agents using the **agent picker** — there is no `cd` into sub-folders and no terminal launch command.

The target codebase is the **Conduit RealWorld** app (`conduit-realworld-example-app/`), a Medium-clone with a Node.js/Express backend, Sequelize + PostgreSQL, and a React/Vite frontend.

Three team lead personas are provided as ready-to-use agents — each requests a different feature. Pick one to start:

| Persona | Agent (in picker) | Feature requested |
|---------|-------------------|-------------------|
| **Alex Chen** | `alex-chen` | Real-time collaborative article editing (WebSockets + OT) |
| **Marcus Webb** | `marcus-webb` | AI-powered personalized article feed (recommendation engine) |
| **Priya Sharma** | `priya-sharma` | Premium subscription paywall + writer revenue share (Stripe) |

---

## Repository layout

```
agent-arch-reasoning-practice/
├── conduit-realworld-example-app/         ← the real codebase under analysis
│   ├── backend/                           ← Express + Sequelize + PostgreSQL
│   └── frontend/                          ← React + Vite SPA
│
├── data/
│   ├── context/company.md             ← Conduit platform: business context, pain points, constraints
│   ├── adrs/
│   │   ├── ADR-001-database.md        ← minimal ADR (intentionally thin)
│   │   ├── ADR-002-api-design.md      ← well-structured ADR
│   │   └── ADR-003-deployment.md      ← outdated monolith ADR
│   └── diagrams/
│       └── current-architecture.mmd   ← current single-VPS topology (Mermaid)
│
├── .kiro/
│   ├── agents/
│   │   ├── alex-chen.md               ← Alex Chen persona (ready to use)
│   │   ├── marcus-webb.md             ← Marcus Webb persona (ready to use)
│   │   ├── priya-sharma.md            ← Priya Sharma persona (ready to use)
│   │   └── architect_template.template.md   ← Step 3: build the architect
│   ├── skills/
│   │   └── adr-tools/                 ← COMPLETE — do not modify
│   │       ├── SKILL.md               ← documents the 4 scripts, call order, and the two gates
│   │       └── scripts/
│   │           ├── list_adrs.py       ← lists all ADRs as JSON
│   │           ├── read_adr.py        ← reads one ADR by ID
│   │           ├── write_adr.py       ← validates + saves new ADR to output/adrs/
│   │           └── save_diagram.py    ← validates + saves Mermaid to output/diagrams/
│   └── settings/
│       └── mcp.json                   ← Mermaid MCP server config (Step 5)
│
├── output/
│   ├── adrs/                          ← agent writes new ADRs here
│   └── diagrams/                      ← agent writes new diagrams here
│
└── README.md
```

The three persona agents are **complete and ready to use** — you select them in the picker, you do not build them. The only agent you build is the **architect**, from the template.

---

## Step 0 — Setup

Open the repository root in Kiro IDE. Open the agent picker and confirm it lists `alex-chen`, `marcus-webb`, and `priya-sharma`. (If it does not, reopen the workspace — agents register at session start.)

Verify the skill scripts work from a terminal:

```bash
python3 .kiro/skills/adr-tools/scripts/list_adrs.py
python3 .kiro/skills/adr-tools/scripts/read_adr.py ADR-001
```

> If `python3` is not found, use `python` instead (or `py` on Windows). Confirm with
> `python3 --version` / `python --version` that it reports **Python 3.x**.

Read `data/context/company.md` to understand the scenario, then browse `conduit-realworld-example-app/backend/` to see the actual code the agent will reason about.

---

## Step 1 — Talk to a Team Lead

Pick one persona (or try all three for extra practice). Select its agent in the picker — e.g. `alex-chen` — and start a conversation. The persona loads immediately; it does not introduce itself as Kiro.

**Good opening questions by persona:**
- Alex: *"What exactly should two writers be able to do at the same time?"*
- Marcus: *"What data do you have today that a recommendation engine could use?"*
- Priya: *"What happens if we charge a reader and the server crashes before we record it?"*

The team lead answers in product/delivery language and pushes back when proposals sound complex or slow to ship. Note down the requirements you gather — you will feed them to the architect in Step 3.

---

## Step 2 — Read and analyse the existing ADRs

Before building the agent, spend 10 minutes reading the three ADRs in `data/adrs/` manually (just open them in the editor — no agent at this stage).

- What was decided and when?
- Which ADR explicitly flags that real-time features need a different transport layer?
- What does ADR-003 warn about for multi-process WebSocket deployments?

This shapes the requirements section of your agent.

---

## Step 3 — Build the Architecture Reasoning Agent

This is the main agent. It reads ADRs, identifies gaps, proposes options, generates diagrams, and writes new ADRs.

The template is `.kiro/agents/architect_template.template.md`. You do **not** fill it in by hand — you ask Kiro to generate the filled-in config for you, then review and tune it. Save the result as `.kiro/agents/architect.md` and set its header `name:` to `architect` — that is what makes it appear in the picker as **architect**.

> **Why the template's `name:` is a placeholder.** Kiro indexes the `name:` field, so the picker would list any agent file that declares a real name — even the half-filled `*.template.md` skeleton. To keep the unfinished skeleton out of the picker, the template ships with an inert `name:` (`architect-TEMPLATE-rename-me`). When you save your completed copy as `architect.md`, change `name:` to `architect`; that is the entry you then select.

Required sections the generated config must fill in:

| Section | What it must contain |
|---|---|
| **Your role** | One-sentence identity |
| **Purpose** | Full scope: what the agent reads, analyses, produces |
| **Trigger** | Exact phrases that start the workflow |
| **Skills** | Load the `adr-tools` skill via the `resources` field (`skill://.kiro/skills/adr-tools/SKILL.md`) — it provides the four scripts |
| **Sub-agents** | The three team leads (`alex-chen`, `marcus-webb`, `priya-sharma`), invokable to resolve ambiguity |
| **Workflow** | Ordered steps (see hints in template) |
| **Output format** | Gap analysis table + option structure with costs/risks/timelines |
| **Guardrails** | Must include the ADR write gate and the diagram gate |
| **Failure handling** | What to do when each tool or sub-agent fails |

### Required guardrails

The generated `architect.md` **must** include both of these rules:

> `write_adr` must **not** be called unless the user's message contains **"write adr"**, **"save adr"**, or **"publish"**.

> `save_diagram` must **not** be called before the user has selected a specific option.

Once `architect.md` exists, select **architect** in the picker (reopen it if needed) and send: `analyse the architecture`

Confirm it:
- Reads `company.md` and all 3 ADRs
- Identifies at least 3 architectural gaps related to the feature
- Proposes 2–3 options with cost estimates and timelines
- **Waits** — does not call `write_adr` or `save_diagram` yet

Then drive it through the full flow:
- Select an option → a diagram is saved to `output/diagrams/`
- Say `write adr` → an ADR is saved to `output/adrs/`

---

## Step 4 — Add an RFC writer sub-agent

After the agent writes an ADR, it should produce a complete RFC that combines everything: requirements, architecture, ADRs, diagram, and migration plan. Rather than make the architect do this itself, you hand off to a second, focused agent — an RFC writer.

You build the RFC writer the same way as the architect: ask Kiro to generate the agent config from a brief, then wire the architect to hand off to it once the ADR is written. The RFC writer receives, in its prompt from the architect:

- Full company context
- All ADR content (existing + new)
- The selected architecture option with its rationale
- The diagram path in `output/diagrams/`
- The requirements summary from the team-lead interview

Re-run the full workflow and verify an RFC is written to `output/`. Read it as the team lead would: could someone approve or reject the decision from this document alone, without having watched the conversation?

---

## Step 5 — Live diagrams with the Mermaid MCP server

The architecture agent can render and live-preview Mermaid diagrams in your browser using the **`claude-mermaid`** MCP server (an npm package — despite the name it works with any MCP client, not just Claude). This is optional but recommended — without it the agent still writes `.mmd`/`.svg` files via the `save_diagram` skill, but you don't get the live browser preview.

### Prerequisite (install before the workshop)

The server pulls in Puppeteer + Chromium (a few hundred MB on first run) and **requires Node ≥ 22.12**. Install it ahead of time on a supported Node so it does not download live during the session:

**macOS / Linux (nvm):**

```bash
nvm install 22 && nvm use 22      # or any Node ≥ 22.12
npm install -g claude-mermaid

# verify it starts (prints "Claude Mermaid MCP Server running on stdio", then Ctrl-C)
claude-mermaid
```

**Windows:** `nvm install` is a Mac/Linux tool and does not exist on Windows. Use one of:

- Download the **Node 22 LTS** installer from [nodejs.org](https://nodejs.org) and run it, or
- Install [nvm-windows](https://github.com/coreybutler/nvm-windows) and run `nvm install 22` then `nvm use 22`.

Then install and verify the server the same way (PowerShell or Command Prompt):

```powershell
npm install -g claude-mermaid

# verify it starts (prints "Claude Mermaid MCP Server running on stdio", then Ctrl-C)
claude-mermaid
```

Confirm your Node version with `node --version` (must be ≥ 22.12) on any platform.

### Configuration

The repo ships `.kiro/settings/mcp.json` with the server already declared:

```json
{
  "mcpServers": {
    "mermaid": {
      "command": "claude-mermaid",
      "args": [],
      "disabled": false,
      "autoApprove": ["mermaid_preview", "mermaid_save"]
    }
  }
}
```

Kiro IDE reloads MCP config on save — no restart needed. Open the MCP panel (`/mcp`) and confirm **mermaid** shows as connected with its **2 tools** (`mermaid_preview`, `mermaid_save`). The `autoApprove` entry means you are not prompted to allow those tool calls during the exercise.

> If the panel shows "connecting" forever or "command not found", the binary is not on your `PATH`. Find it with `which claude-mermaid` (macOS/Linux) or `where claude-mermaid` (Windows) and put that absolute path in `command`.

### Verify it works

With the **architect** selected, after you have picked an option, ask it to draw the target architecture and open a live preview. A browser tab opens at `http://localhost:3737` and auto-refreshes as the diagram is refined. Ask it to switch to the dark theme or add a component to see the live reload.

**Offline fallback:** if the MCP server is unavailable, have the agent output raw Mermaid and paste it into [mermaid.live](https://mermaid.live).

---

## Submission checklist

- [ ] A team lead persona was used from the picker (`alex-chen`, `marcus-webb`, or `priya-sharma`)
- [ ] Team lead chatbot responds in delivery/product language (test: propose something complex — they should push back on scope or timeline)
- [ ] `.kiro/agents/architect.md` exists — no `[TODO]` tokens remain
- [ ] ADR write gate present in `architect.md`
- [ ] Diagram gate present in `architect.md`
- [ ] Agent reads all 3 ADRs before proposing options
- [ ] Agent presents 2–3 options and **waits** before writing anything
- [ ] `output/diagrams/` contains a generated diagram
- [ ] `output/adrs/` contains a generated ADR
- [ ] An RFC writer agent was built and the architect hands off to it
- [ ] An RFC exists in `output/` after a full workflow run

---

## Tips

- Read `data/context/company.md` carefully — your agent's gap analysis should map directly to the pain points described there, especially the single-VPS constraint that affects WebSocket scaling.
- Browse `conduit-realworld-example-app/backend/` — the agent should be able to reason about what the real code actually does, not just the company doc.
- The write gate is the most important guardrail. Test that the agent does **not** call `write_adr` when you say "looks good" or "I approve".
- If the agent skips a step, add more explicit ordering language to the workflow section ("do not proceed to step N until step N-1 is complete") — but add rules only against a flaw you actually observe, not pre-emptively.
