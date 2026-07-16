import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "run_v4_stimulus_metamorphic.py"
SPEC = importlib.util.spec_from_file_location("run_v4_stimulus_metamorphic", MODULE_PATH)
assert SPEC and SPEC.loader
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def test_affine_transform_scales_pwl_and_shifts_absolute_times() -> None:
    deck = (
        "Vx (x 0) vsource type=pwl wave=[0 0 10n 0.9]\n"
        "Vclk (clk 0) vsource type=pulse period=5n width=2n delay=1n rise=10p fall=20p\n"
        "XDUT (x) dut unit_phase_delay=40p tr=20p\n"
        "tran tran stop=20n maxstep=100p\n"
    )
    transformed = runner.transform_stimulus(deck, scale=2.0, shift=1e-9)
    assert "wave=[1n 0 21n 0.9]" in transformed
    assert "period=10n" in transformed
    assert "width=4n" in transformed
    assert "delay=3n" in transformed
    assert "rise=20p" in transformed
    assert "fall=40p" in transformed
    assert "unit_phase_delay=80p" in transformed
    assert "tr=40p" in transformed
    assert "stop=41n" in transformed
    assert "maxstep=200p" in transformed


def test_affine_transform_accepts_multiline_pwl_continuations() -> None:
    deck = (
        "Vx (x 0) vsource type=pwl wave=[ \\\n"
        "0 0 \\\n"
        "10n 0.9 \\\n"
        "]\ntran tran stop=10n\n"
    )
    transformed = runner.transform_stimulus(deck, scale=2.0, shift=1e-9)
    assert "wave=[1n 0 21n 0.9]" in transformed
    assert "\\" not in transformed


def test_insufficient_stimulus_keeps_legal_source_declarations() -> None:
    deck = "Vx (x 0) vsource type=pwl wave=[0 0 5n 0.9]\nVclk (c 0) vsource type=pulse period=5n width=2n\n"
    suppressed = runner.suppress_stimulus(deck)
    assert "type=pwl" not in suppressed
    assert "type=pulse" not in suppressed
    assert suppressed.count("vsource dc=0") == 2


def test_evas2_evidence_requires_version_and_rust_backend_markers() -> None:
    evidence = runner.require_rust_evas2(
        "Version 0.8.2\n    evas_engine = evas-rust\n"
    )
    assert evidence["evas_engine"] == "evas2"
    assert evidence["evas_engine_used"] == "evas2"
    assert evidence["evas_version"] == "0.8.2"


def test_evas2_evidence_rejects_python_marker() -> None:
    try:
        runner.require_rust_evas2("Version 0.8.2\n    evas_engine = python\n")
    except RuntimeError as exc:
        assert "Rust backend marker" in str(exc)
    else:
        raise AssertionError("Python EVAS evidence was accepted")


def test_run_case_rejects_missing_per_case_runtime_log(tmp_path, monkeypatch) -> None:
    task_dir = tmp_path / "task"
    task_dir.mkdir()
    tb_path = task_dir / "reference_tb.scs"
    tb_path.write_text("tran tran stop=1n\n", encoding="utf-8")

    monkeypatch.setattr(runner, "stage_case", lambda **kwargs: (tb_path, []))
    monkeypatch.setattr(runner, "required_trace_signals_for_checker", lambda task_id: {"time"})
    monkeypatch.setattr(
        runner,
        "run_evas",
        lambda *args, **kwargs: type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})(),
    )

    result = runner.run_case(
        task_dir=task_dir,
        checker_task_id="v4-001",
        deck_text="tran tran stop=1n\n",
        case_id="correct",
        mutation_id=None,
        output_root=tmp_path / "runs",
        timeout_s=1,
    )

    assert result["status"] == "infrastructure_error"
    assert result["evas_runtime_valid"] is False
    assert result["evas_runtime_notes"] == ["missing evas.log"]
