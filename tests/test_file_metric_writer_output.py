from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from simulate_evas import _validate_file_metric_output  # noqa: E402


def _write_tran(path: Path) -> None:
    path.write_text(
        "time,vin,done\n"
        "0,0.0,0.0\n"
        "2.5e-8,0.0,0.0\n"
        "3.0e-8,0.4,0.0\n"
        "3.1e-8,0.5,0.9\n"
        "4.0e-8,0.9,0.9\n",
        encoding="utf-8",
    )


def test_file_metric_writer_requires_single_crossing_record(tmp_path: Path) -> None:
    csv_path = tmp_path / "tran.csv"
    _write_tran(csv_path)
    (tmp_path / "metric.out").write_text("cross 3.05e-8\n", encoding="utf-8")

    result = _validate_file_metric_output("vbm1_file_metric_writer_dut", tmp_path, csv_path)

    assert result == (True, "metric_file_time=3.050e-08 waveform_cross=3.050e-08 delta=0.000e+00")


def test_file_metric_writer_rejects_stale_or_wrong_metric_file(tmp_path: Path) -> None:
    csv_path = tmp_path / "tran.csv"
    _write_tran(csv_path)
    (tmp_path / "metric.out").write_text("cross 1.0e-8\n", encoding="utf-8")

    ok, note = _validate_file_metric_output("vbm1_file_metric_writer_dut", tmp_path, csv_path)

    assert not ok
    assert "delta=" in note


def test_file_metric_writer_accepts_evas_time_suffix(tmp_path: Path) -> None:
    csv_path = tmp_path / "tran.csv"
    _write_tran(csv_path)
    (tmp_path / "metric.out").write_text("cross 3.05e-08n\n", encoding="utf-8")

    ok, note = _validate_file_metric_output("vbm1_file_metric_writer_dut", tmp_path, csv_path)

    assert ok
    assert "delta=0.000e+00" in note
