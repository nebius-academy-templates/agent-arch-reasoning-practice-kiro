"""
save_diagram — adr-tools skill

Saves a Mermaid diagram to output/diagrams/.
The diagram content is read from a file whose path is passed as the second argument.

Usage:
    python .kiro/skills/adr-tools/scripts/save_diagram.py <diagram-name> <content-file>

Example:
    python .kiro/skills/adr-tools/scripts/save_diagram.py proposed-architecture /tmp/diagram.mmd
"""

import json
import re
import sys
from pathlib import Path


def _repo_root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "output").is_dir() and (parent / "data" / "adrs").is_dir():
            return parent
    return p.parents[4]


OUTPUT_DIR = _repo_root() / "output" / "diagrams"
VALID_DIAGRAM_TYPES = ["graph", "flowchart", "sequenceDiagram", "classDiagram", "erDiagram"]


def save_diagram(name: str, content_file: str) -> dict:
    name = re.sub(r"[^a-zA-Z0-9_-]", "-", name).strip("-")
    content_path = Path(content_file)
    if not content_path.exists():
        raise FileNotFoundError(f"Content file not found: {content_file}")

    content = content_path.read_text()

    has_valid_type = any(t in content for t in VALID_DIAGRAM_TYPES)
    if not has_valid_type:
        raise ValueError(
            f"Diagram does not appear to be valid Mermaid. "
            f"Expected one of: {VALID_DIAGRAM_TYPES}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{name}.mmd"
    out_path.write_text(content)

    return {
        "saved": str(out_path.relative_to(_repo_root())),
        "name": name,
        "lines": len(content.splitlines()),
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python save_diagram.py <diagram-name> <content-file>", file=sys.stderr)
        sys.exit(1)

    try:
        print(json.dumps(save_diagram(sys.argv[1], sys.argv[2]), indent=2))
    except (FileNotFoundError, ValueError) as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
