from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from simulate_evas import load_csv  # noqa: E402


def test_load_csv_preserves_original_names_and_adds_lowercase_aliases(
    tmp_path: Path,
) -> None:
    trace = tmp_path / "tran.csv"
    trace.write_text("time,VINP,OUT_P\n0,0.2,0.9\n", encoding="utf-8")

    rows = load_csv(trace)

    assert rows == [
        {
            "time": 0.0,
            "VINP": 0.2,
            "vinp": 0.2,
            "OUT_P": 0.9,
            "out_p": 0.9,
        }
    ]
