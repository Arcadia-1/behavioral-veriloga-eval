from __future__ import annotations

import importlib.util
from pathlib import Path


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
