from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "validate_v4_repair_gate.py"
SPEC = importlib.util.spec_from_file_location("validate_v4_repair_gate", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_trace_contract_does_not_require_implicit_time_save() -> None:
    failures: list[dict[str, object]] = []

    MODULE.validate_trace_contract(
        failures,
        "071",
        {"deck": {"save_signals": ["vin", "vout"]}},
        {"trace_contract": {"required_signals": ["time", "vin", "vout"]}},
        {
            "trace_contract": {
                "public_observables": ["time", "vin", "vout"],
                "extra_trace_signals": ["time"],
            }
        },
        {"public_observables": ["time", "vin", "vout"]},
    )

    assert failures == []
