#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / "runners"))

from visible_smoke import run_visible_smoke


if __name__ == "__main__":
    raise SystemExit(
        run_visible_smoke(
            __file__,
            checker_task_id="v3_066_duty_cycle_meter_8b",
        )
    )
