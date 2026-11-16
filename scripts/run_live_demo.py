#!/usr/bin/env python3
"""Call POST /posting logic directly and save JSON for submission docs."""

from __future__ import annotations

import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.services.posting_service import publish_message  # noqa: E402

SAMPLE_MESSAGE = (
    "Check out our latest business platform and grow your online visibility. "
    "https://example.com"
)
LOG_DIR = ROOT / "docs" / "logs"


async def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()

    response = await publish_message(SAMPLE_MESSAGE)
    payload = response.model_dump(mode="json")

    out_json = LOG_DIR / "demo-response.json"
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    log_lines = [
        f"[{started}] Live demo run (no uvicorn)",
        f"Message: {SAMPLE_MESSAGE!r}",
        f"Output file: {out_json.relative_to(ROOT)}",
        f"success={payload['success']}",
    ]
    for row in payload["results"]:
        log_lines.append(
            f"  {row['platform']}: {row['status']}"
            + (f" -> {row['posted_url']}" if row.get("posted_url") else "")
            + (f" ({row['error']})" if row.get("error") else "")
        )

    log_file = LOG_DIR / "demo-run.log"
    log_file.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    print(json.dumps(payload, indent=2))
    print(f"\nWrote {out_json} and {log_file}", file=sys.stderr)
    return 0 if payload["success"] else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
# Last updated: Monday, Nov 16, 2026, 04:23 PM (UTC+5:30)
