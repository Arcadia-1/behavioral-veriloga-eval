from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
ORACLE_PATH = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "runners"
    / "derived_testbench_oracle.py"
)


def load_oracle():
    spec = importlib.util.spec_from_file_location("derived_oracle_engine_route", ORACLE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def pin_rust_engine(monkeypatch) -> None:
    monkeypatch.setenv("EVAS_ENGINE", "evas2")
    monkeypatch.setenv("VAEVAS_DEFAULT_EVAS_ENGINE", "evas2")


def test_oracle_accepts_declared_python_compatibility_route(monkeypatch) -> None:
    oracle = load_oracle()
    pin_rust_engine(monkeypatch)
    report = "\n".join(
        [
            f"Version {oracle.REQUIRED_EVAS_VERSION} -- Jul 2026",
            "Compatibility engine route: evas-rust -> python for absdelay",
            "evas_engine = python",
        ]
    )

    valid, note = oracle._validate_required_evas_engine(report, "evas2")

    assert valid is True
    assert "evas_backend=python_compatibility" in note
    assert "evas_compatibility_features=absdelay" in note


def test_oracle_rejects_unannounced_python_backend(monkeypatch) -> None:
    oracle = load_oracle()
    pin_rust_engine(monkeypatch)

    valid, note = oracle._validate_required_evas_engine(
        f"Version {oracle.REQUIRED_EVAS_VERSION} -- Jul 2026\nevas_engine = python",
        "evas2",
    )

    assert valid is False
    assert "engine_validation_failed=backend" in note


def test_oracle_accepts_only_r53_evas_version(monkeypatch) -> None:
    oracle = load_oracle()
    pin_rust_engine(monkeypatch)
    monkeypatch.setenv("VABENCH_EVAS_PROFILE", "r53")

    valid, note = oracle._validate_required_evas_engine(
        "Version 0.8.7 -- Jul 2026\nevas_engine = evas-rust",
        "evas2",
    )
    stale, stale_note = oracle._validate_required_evas_engine(
        "Version 0.8.6 -- Jul 2026\nevas_engine = evas-rust",
        "evas2",
    )

    assert valid is True
    assert "evas_profile=r53" in note
    assert "evas_version=0.8.7" in note
    assert stale is False
    assert "required='0.8.7'" in stale_note


def test_oracle_rejects_unknown_evas_profile(monkeypatch) -> None:
    oracle = load_oracle()
    pin_rust_engine(monkeypatch)
    monkeypatch.setenv("VABENCH_EVAS_PROFILE", "unreviewed")

    with pytest.raises(ValueError, match="unsupported VABENCH_EVAS_PROFILE"):
        oracle._validate_required_evas_engine(
            "Version 0.8.7 -- Jul 2026\nevas_engine = evas-rust",
            "evas2",
        )


def test_oracle_accepts_time_dependent_cross_compatibility(monkeypatch) -> None:
    oracle = load_oracle()
    pin_rust_engine(monkeypatch)
    monkeypatch.setenv("VABENCH_EVAS_PROFILE", "r53")
    report = "\n".join(
        [
            "Version 0.8.7 -- Jul 2026",
            "Compatibility engine route: evas-rust -> python for time_dependent_cross_event",
            "evas_engine = python",
        ]
    )

    valid, note = oracle._validate_required_evas_engine(report, "evas2")

    assert valid is True
    assert "evas_compatibility_features=time_dependent_cross_event" in note


def test_compatibility_route_keeps_checker_watchdog_isolation(
    tmp_path: Path,
    monkeypatch,
) -> None:
    oracle = load_oracle()
    testbench = tmp_path / "candidate.scs"
    testbench.write_text("tran tran stop=1n\n", encoding="utf-8")

    def fake_run_evas(_run_dir, _tb_path, output_dir, **_kwargs):
        output_dir.mkdir()
        (output_dir / "tran.csv").write_text("time,out\n0,0\n", encoding="utf-8")
        return SimpleNamespace(returncode=0, stdout="simulation complete", stderr="")

    def fake_evaluate(_task_id, _csv_path, *, timeout_s, force_subprocess):
        assert timeout_s == 60
        assert force_subprocess is True
        return 0.0, ["behavior_eval_timeout>60s"]

    monkeypatch.setitem(
        sys.modules,
        "simulate_evas",
        SimpleNamespace(
            run_evas=fake_run_evas,
            evaluate_behavior_with_timeout=fake_evaluate,
        ),
    )
    monkeypatch.setattr(oracle, "_prepare_dut_sources", lambda **_kwargs: None)
    monkeypatch.setattr(oracle, "_trace_is_valid", lambda *_args: (True, []))
    monkeypatch.setattr(
        oracle,
        "_validate_required_evas_engine",
        lambda *_args: (True, "evas_engine=evas2"),
    )

    result = oracle._run_case(
        package_root=ROOT,
        tb_source=testbench,
        source_formal=tmp_path,
        target_artifacts=[],
        negative_bundle=None,
        checker_task_id="v4-test",
        required_signals={"time", "out"},
        label="reference",
    )

    assert result.outcome is oracle.CaseOutcome.INVALID_RUN
    assert any("behavior_eval_timeout>60s" in note for note in result.notes)
