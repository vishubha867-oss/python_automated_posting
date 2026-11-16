#!/usr/bin/env python3
"""Write OpenAPI schema to docs/openapi.json for reviewers."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.main import app  # noqa: E402

OUT = ROOT / "docs" / "openapi.json"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    schema = app.openapi()
    OUT.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
# Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30)
