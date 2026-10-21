"""
list_adrs — adr-tools skill

Scans data/adrs/ and returns a JSON list of all ADRs with their ID, title,
date, status, and author (parsed from standard ADR front-matter).
"""

import json
import re
from pathlib import Path


def _repo_root() -> Path:
    """Walk up from this script until we find the dir holding data/adrs/."""
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "data" / "adrs").is_dir():
            return parent
    return p.parents[4]


ADR_DIR = _repo_root() / "data" / "adrs"


def parse_adr_meta(path: Path) -> dict:
    text = path.read_text()
    lines = text.splitlines()

    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line.lstrip("# ").strip()
            break

    def field(key: str) -> str:
        m = re.search(rf"^{key}:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
        return m.group(1).strip() if m else ""

    adr_id = path.stem.split("-")[0] + "-" + path.stem.split("-")[1] if "-" in path.stem else path.stem
    return {
        "id": adr_id,
        "filename": path.name,
        "title": title,
        "date": field("Date"),
        "status": field("Status"),
        "author": field("Author"),
    }


def list_adrs() -> list[dict]:
    if not ADR_DIR.exists():
        return []
    adrs = sorted(ADR_DIR.glob("*.md"))
    return [parse_adr_meta(p) for p in adrs]


if __name__ == "__main__":
    print(json.dumps(list_adrs(), indent=2))
