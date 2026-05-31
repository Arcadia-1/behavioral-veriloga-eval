import json
import subprocess
from pathlib import Path

import simulate_evas


def test_run_case_removes_stale_tran_csv_before_evas(monkeypatch, tmp_path: Path) -> None:
    task_dir = tmp_path / "task"
    task_dir.mkdir()
    (task_dir / "meta.json").write_text(
        json.dumps({"id": "stale_output_case", "scoring": ["tb_compile"]}),
        encoding="utf-8",
    )
    dut = tmp_path / "dut.va"
    tb = tmp_path / "tb.scs"
    dut.write_text("module m(a); electrical a; endmodule\n", encoding="utf-8")
    tb.write_text("tran tran stop=1n\n", encoding="utf-8")

    output_root = tmp_path / "persistent_output"
    output_root.mkdir()
    (output_root / "tran.csv").write_text("time,out\n0,1\n", encoding="utf-8")

    def fake_run_evas(run_dir: Path, tb_file: Path, output_dir: Path, timeout_s: int):
        assert not (output_dir / "tran.csv").exists()
        return subprocess.CompletedProcess(["evas"], 1, stdout="", stderr="parse failed")

    monkeypatch.setattr(simulate_evas, "run_evas", fake_run_evas)

    result = simulate_evas.run_case(
        task_dir,
        dut,
        tb,
        output_root=output_root,
        timeout_s=1,
    )

    assert result["scores"]["tb_compile"] == 0.0
    assert result["status"] == "FAIL_TB_COMPILE"
