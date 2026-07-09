#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PACKAGE_ROOT / "runners"))

from feedback_oracle import run_score


if __name__ == "__main__":
    raise SystemExit(run_score(__file__))
