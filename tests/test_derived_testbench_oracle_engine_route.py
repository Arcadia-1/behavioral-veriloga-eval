from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

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


def test_oracle_accepts_only_r53test_evas_version(monkeypatch) -> None:
    oracle = load_oracle()
    pin_rust_engine(monkeypatch)
    monkeypatch.setenv("VABENCH_EVAS_PROFILE", "r53test")

    valid, note = oracle._validate_required_evas_engine(
        "Version 0.8.6 -- Jul 2026\nevas_engine = evas-rust",
        "evas2",
    )
    stale, stale_note = oracle._validate_required_evas_engine(
        "Version 0.8.5 -- Jul 2026\nevas_engine = evas-rust",
        "evas2",
    )

    assert valid is True
    assert "evas_profile=r53test" in note
    assert "evas_version=0.8.6" in note
    assert stale is False
    assert "required='0.8.6'" in stale_note


def test_oracle_rejects_unknown_evas_profile(monkeypatch) -> None:
    oracle = load_oracle()
    pin_rust_engine(monkeypatch)
    monkeypatch.setenv("VABENCH_EVAS_PROFILE", "unreviewed")

    with pytest.raises(ValueError, match="unsupported VABENCH_EVAS_PROFILE"):
        oracle._validate_required_evas_engine(
            "Version 0.8.6 -- Jul 2026\nevas_engine = evas-rust",
            "evas2",
        )


def test_oracle_accepts_time_dependent_cross_compatibility(monkeypatch) -> None:
    oracle = load_oracle()
    pin_rust_engine(monkeypatch)
    monkeypatch.setenv("VABENCH_EVAS_PROFILE", "r53test")
    report = "\n".join(
        [
            "Version 0.8.6 -- Jul 2026",
            "Compatibility engine route: evas-rust -> python for time_dependent_cross_event",
            "evas_engine = python",
        ]
    )

    valid, note = oracle._validate_required_evas_engine(report, "evas2")

    assert valid is True
    assert "evas_compatibility_features=time_dependent_cross_event" in note
