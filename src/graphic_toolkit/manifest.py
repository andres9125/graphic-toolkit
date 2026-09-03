from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_manifest(path: str | Path, payload: dict[str, Any]) -> Path:
    """Write a stable, UTF-8 JSON manifest and return its path."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return destination

