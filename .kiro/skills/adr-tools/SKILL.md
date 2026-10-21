---
name: adr-tools
description: Read and write Architecture Decision Records and save Mermaid diagrams for the Conduit architecture-reasoning workflow. Use when analysing the architecture: listing ADRs, reading an ADR, saving a target diagram, or writing a new ADR. Enforces the ADR write gate and the diagram gate.
license: MIT
compatibility: Requires Python 3 and the project's data/ and output/ directories.
---

## What this is

A toolbox of four scripts the architecture reasoning agent uses to work with the project's decision records and diagrams. All commands are run from the repository root.

> **Python command.** These examples use `python3`. If `python3` is not found on this machine, use `python` instead (or `py` on Windows). Whichever one prints `Python 3.x` from `--version` is the one to use.

| Script | Command | Purpose |
|---|---|---|
| `list_adrs` | `python3 .kiro/skills/adr-tools/scripts/list_adrs.py` | List every ADR (JSON: `id`, `filename`, `title`, `date`, `status`, `author`). |
| `read_adr` | `python3 .kiro/skills/adr-tools/scripts/read_adr.py <ADR-ID>` | Read one ADR by ID prefix (JSON: `id`, `filename`, `body`). |
| `save_diagram` | `python3 .kiro/skills/adr-tools/scripts/save_diagram.py "<name>" <content-file>` | Save a Mermaid diagram to `output/diagrams/<name>.mmd` (validates the diagram type). |
| `write_adr` | `python3 .kiro/skills/adr-tools/scripts/write_adr.py <ADR-ID> "<Title>" <content-file>` | Write a new ADR to `output/adrs/` (requires `Context` / `Decision` / `Consequences` sections). |

## Canonical order

1. **List and read every ADR first.** Run `list_adrs`, then `read_adr` once per returned ID. You must have read all ADRs — focusing on their **Negative** and **To watch** consequences — before producing any gap analysis or recommendation.
2. **Analyse and present options**, then stop and wait for the user to choose. Do nothing irreversible yet.
3. **Save the diagram only after the user selects an option** (see Diagram gate).
4. **Write the ADR only on an explicit write phrase** (see ADR write gate).

## Gates (required)

- **ADR write gate.** Never call `write_adr` unless the user's most recent message contains one of the exact phrases **"write adr"**, **"save adr"**, or **"publish"** — and an option has already been selected. No synonym, no inference. If the phrase is absent, stop and ask.
- **Diagram gate.** Never call `save_diagram` before the user has selected a specific option. No speculative or "preview" diagrams during the options stage.

## Writing an ADR

`write_adr` reads the ADR body from a content file. Write the draft to a temp file first, then pass its path. The body must contain `Context`, `Decision`, and `Consequences` sections (add Rationale and Positive / Negative / To watch as well). Use the next free ID (today that is `ADR-004`).

## Saving a diagram

`save_diagram` reads the Mermaid source from a content file. The content must start with a valid diagram type (`graph`, `flowchart`, `sequenceDiagram`, `classDiagram`, or `erDiagram`).

## Failure handling

- **`python3` not found / command not recognised.** The interpreter name differs by machine. If a command fails because `python3` is missing, retry the same command with `python` (or `py` on Windows) instead of stopping. Do not report a tool failure until both have been tried.
- `list_adrs` returns `[]` — do not fabricate ADRs. Report none were found and proceed on `company.md` + the current diagram only, stating the analysis is partial.
- `read_adr` returns `{"error": ...}` — report the failing ID, retry once with the exact `id` from `list_adrs`, then continue with what you could read and say the analysis is partial.
- `save_diagram` validation error — the Mermaid lacked a valid type; fix the source and retry once.
- `write_adr` validation error — a required section is missing; add it and retry. Never bypass the validation by stripping sections; fix the content.
