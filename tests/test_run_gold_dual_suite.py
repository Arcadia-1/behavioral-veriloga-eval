from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

import run_gold_dual_suite as dual  # noqa: E402
import run_gold_suite as gold_suite  # noqa: E402


def test_run_dual_case_marks_non_scored_behavior_as_not_required(
    monkeypatch, tmp_path: Path
) -> None:
    task_dir = tmp_path / "tasks" / "tb-generation" / "voltage" / "clk_div_min_tb"
    gold_dir = task_dir / "gold"
    gold_dir.mkdir(parents=True)
    tb_path = gold_dir / "tb_clk_div_min_ref.scs"
    dut_path = gold_dir / "clk_div_min.va"
    tb_path.write_text('ahdl_include "clk_div_min.va"\n', encoding="utf-8")
    dut_path.write_text("// stub dut\n", encoding="utf-8")

    monkeypatch.setattr(
        dual,
        "read_meta",
        lambda path: {
            "task_id": "clk_div_min_tb",
            "scoring": ["dut_compile", "tb_compile"],
        },
    )
    monkeypatch.setattr(dual, "choose_gold_tb", lambda gold: tb_path)
    monkeypatch.setattr(dual, "ahdl_includes", lambda tb: [dut_path.name])
    monkeypatch.setattr(gold_suite, "run_gold_case", lambda *args, **kwargs: {"status": "PASS"})
    monkeypatch.setattr(
        dual,
        "run_spectre_case",
        lambda **kwargs: {"status": "success", "ok": True},
    )

    def fail_if_called(*args, **kwargs):
        raise AssertionError("compare_waveforms/evaluate_behavior should not run for non-scored behavior")

    monkeypatch.setattr(dual, "evaluate_behavior", fail_if_called)
    monkeypatch.setattr(dual, "compare_waveforms", fail_if_called)

    result = dual.run_dual_case(
        task_dir=task_dir,
        output_root=tmp_path / "results",
        bridge_repo=tmp_path / "bridge",
        cadence_cshrc=None,
        timeout_s=5,
    )

    assert result["status"] == "PASS"
    assert result["parity"]["status"] == "not_required"
    assert result["spectre"]["behavior_score"] == 1.0
    assert "behavior_not_required_by_scoring" in result["spectre"]["behavior_notes"]
    assert "spectre:behavior_not_required_by_scoring" in result["notes"]


def test_run_spectre_case_passes_bridge_profile(monkeypatch, tmp_path: Path) -> None:
    bridge_repo = tmp_path / "bridge"
    (bridge_repo / ".venv" / "bin").mkdir(parents=True)
    output_dir = tmp_path / "out"
    captured: dict[str, object] = {}

    monkeypatch.setenv("VAEVAS_BRIDGE_PROFILE", "ci")

    def fake_run_cmd(cmd, *, cwd: Path, env=None, timeout_s=None):
        captured["cmd"] = cmd
        captured["cwd"] = cwd
        captured["env"] = env
        captured["timeout_s"] = timeout_s
        captured["inline"] = cmd[-1]
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "spectre_result.json").write_text(
            json.dumps({"status": "success", "ok": True, "errors": [], "warnings": []}),
            encoding="utf-8",
        )
        return SimpleNamespace(stdout="", stderr="", returncode=0)

    monkeypatch.setattr(dual, "run_cmd", fake_run_cmd)

    result = dual.run_spectre_case(
        task_id="case",
        tb_path=tmp_path / "tb.scs",
        include_paths=[],
        output_dir=output_dir,
        bridge_repo=bridge_repo,
        cadence_cshrc=None,
        timeout_s=5,
    )

    assert result["ok"] is True
    assert captured["cwd"] == bridge_repo
    assert captured["env"]["VAEVAS_BRIDGE_PROFILE"] == "ci"
    assert '"bridge_profile": "ci"' in captured["inline"]
    assert "profile=profile" in captured["inline"]


def test_run_spectre_case_can_request_side_output_downloads(monkeypatch, tmp_path: Path) -> None:
    bridge_repo = tmp_path / "bridge"
    (bridge_repo / ".venv" / "bin").mkdir(parents=True)
    output_dir = tmp_path / "out"
    captured: dict[str, object] = {}

    def fake_run_cmd(cmd, *, cwd: Path, env=None, timeout_s=None):
        captured["inline"] = cmd[-1]
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "spectre_result.json").write_text(
            json.dumps({"status": "success", "ok": True, "errors": [], "warnings": []}),
            encoding="utf-8",
        )
        return SimpleNamespace(stdout="", stderr="", returncode=0)

    monkeypatch.setattr(dual, "run_cmd", fake_run_cmd)

    result = dual.run_spectre_case(
        task_id="case",
        tb_path=tmp_path / "tb.scs",
        include_paths=[],
        output_dir=output_dir,
        bridge_repo=bridge_repo,
        cadence_cshrc=None,
        timeout_s=5,
        side_output_files=("candidate.out",),
    )

    assert result["ok"] is True
    assert '"side_output_files": ["candidate.out"]' in captured["inline"]
    assert "keep_remote_files=bool(side_output_files)" in captured["inline"]
    assert "remote_pwd = next((line for line in reversed(pwd_lines) if line.startswith('/')), '')" in captured["inline"]
    assert "remote_output_dirs.append(candidate_dir)" in captured["inline"]
    assert "runner.download(remote_path, local_path)" in captured["inline"]
