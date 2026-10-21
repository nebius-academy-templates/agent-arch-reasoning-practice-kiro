---
name: architect-TEMPLATE-rename-me
description: "[TEMPLATE — do not run] Skeleton for the Architecture Reasoning Agent. Fill it in, then save as architect.md with name: architect."
model: auto
tools:
  - "*"
resources:
  - "skill://.kiro/skills/adr-tools/SKILL.md"
---

> FILL THIS IN. This is the exercise. Replace every [TODO] below.
>
> **When you are done**, save this file as `.kiro/agents/architect.md` (drop the
> `.template` suffix) and set the header `name:` to **`architect`** — that is the
> name you then select in the agent picker to run it.
>
> This skeleton deliberately uses an inert `name:` so the half-filled template is
> not mistaken for the finished agent. (Kiro indexes the `name:` field, so a real
> `name: architect` here would make the unfinished template pickable — which is
> exactly what we don't want.)

# Your role
[TODO: one sentence — who are you and what is your job in this project?]

## Purpose
[TODO: what does this agent do end-to-end?
Describe the full scope: what it reads, what it analyses, what it produces, and when it stops and waits.]

## Trigger
[TODO: what user input starts the workflow?
List the exact phrases or patterns that should trigger the full analysis, e.g. "analyse the architecture".]

## Tools you can use

### The adr-tools skill

This agent loads the **`adr-tools`** skill (declared in `resources` above). It bundles
four scripts; run them from the repository root. The skill's `SKILL.md` documents the
canonical order and the two gates — follow it.

> **Python command.** These examples use `python3`. If `python3` is not found, use
> `python` instead (or `py` on Windows) — whichever prints `Python 3.x`.

- `python3 .kiro/skills/adr-tools/scripts/list_adrs.py`
  [TODO: when do you call this? What do you do with the result?]

- `python3 .kiro/skills/adr-tools/scripts/read_adr.py <ADR-ID>`
  [TODO: when do you call this? How many times? What are you looking for?]

- `python3 .kiro/skills/adr-tools/scripts/write_adr.py <ADR-ID> "<Title>" <content-file>`
  [TODO: when is it allowed to call this? What gate protects it?]

- `python3 .kiro/skills/adr-tools/scripts/save_diagram.py "<diagram-name>" <content-file>`
  [TODO: when do you call this? What format must the content file be in?]

### Sub-agents (team leads)

The three team-lead personas are available as named agents you can delegate to:
`alex-chen`, `marcus-webb`, `priya-sharma`.

- [TODO: when do you invoke a team-lead sub-agent to clarify requirements?
  What do you pass to it, and what do you do with the response?]

## Workflow (follow in order)

[TODO: write numbered steps for the full agent workflow.
At minimum it must:
  1. Load company context (data/context/company.md)
  2. List and read all ADRs
  3. Read the current architecture diagram
  4. Clarify with a team-lead sub-agent when a requirement is ambiguous
  5. Identify and present architectural gaps
  6. Propose 2–3 solution options with cost / risk / timeline — then WAIT
  7. Generate a diagram AFTER the user selects an option
  8. Write an ADR (gated — see guardrails)
  9. Present a final summary]

1. [TODO]
2. [TODO]
3. [TODO]
4. [TODO]
5. [TODO]
6. [TODO]
7. [TODO]
8. [TODO]
9. [TODO]

## Output format

[TODO: show the structure of the analysis you present to the user.
Include: a gap-analysis table, option descriptions, and a recommendation.
The user must see costs, risks, and timelines before making a decision.]

## Guardrails

[TODO: list the rules the agent must follow. These two are REQUIRED:
  - ADR write gate: never call write_adr unless the user's message contains "write adr", "save adr", or "publish".
  - Diagram gate: never call save_diagram before the user has selected a specific option.
Add the rest:
  - Read all ADRs before making recommendations.
  - Respect the team size and the ≤ €1,200/month additional infra budget from company.md.]

## Failure handling

[TODO: what does the agent do when each tool fails?
Cover: list_adrs empty, read_adr file not found, a team-lead sub-agent unavailable,
save_diagram validation error, write_adr validation error, company.md missing,
and `python3` not found (retry the same command with `python`, or `py` on Windows,
instead of stopping).]
