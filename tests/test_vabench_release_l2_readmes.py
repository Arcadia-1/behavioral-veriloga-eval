from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from sync_vabench_release_entry_readmes import render_entry_readme  # noqa: E402


def test_l2_release_readmes_match_release_entry_source_of_truth() -> None:
    for entry_path in sorted((ROOT / "benchmark-vabench-release-v1" / "tasks").glob("vbr1_l2_*/release_entry.json")):
        entry = json.loads(entry_path.read_text(encoding="utf-8"))
        readme = entry_path.parent / "README.md"
        assert readme.read_text(encoding="utf-8") == render_entry_readme(entry)
