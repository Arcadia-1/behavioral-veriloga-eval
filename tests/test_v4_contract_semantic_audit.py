from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "benchmark-vabench-release-v4" / "scripts" / "audit_v4_contract_semantics.py"
SPEC = importlib.util.spec_from_file_location("audit_v4_contract_semantics", SCRIPT)
assert SPEC and SPEC.loader
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_identifier_visible_supports_scalar_and_bus_notation() -> None:
    text = "module demo(input electrical clk, inputs code0 through code7);"
    assert audit.identifier_visible(text, "clk")
    assert audit.identifier_visible(text, "code3")
    assert audit.identifier_visible(text, "code[5]")
    assert not audit.identifier_visible(text, "tick")


def test_aggregate_is_derived_from_independent_family_shards(tmp_path: Path) -> None:
    for family_id, status, findings in (
        ("001", "pass", []),
        (
            "002",
            "review",
            [
                {
                    "severity": "review",
                    "check": "instruction_interface_traceability",
                    "message": "missing parameter",
                }
            ],
        ),
        (
            "003",
            "error",
            [
                {
                    "severity": "error",
                    "check": "property_binding",
                    "message": "property mismatch",
                }
            ],
        ),
    ):
        write_json(
            tmp_path / f"{family_id}.json",
            {
                "schema_version": audit.SCHEMA_VERSION,
                "family_id": family_id,
                "family_slug": f"{family_id}-sample",
                "status": status,
                "findings": findings,
            },
        )
    write_json(tmp_path / "unrelated.json", {"schema_version": "other"})

    result = audit.aggregate_shards(tmp_path)

    assert result["family_count"] == 3
    assert result["status_counts"] == {"pass": 1, "review": 1, "error": 1}
    assert result["finding_counts_by_check"] == {
        "instruction_interface_traceability": 1,
        "property_binding": 1,
    }
    assert [item["family_id"] for item in result["anomalies"]] == ["002", "003"]
    assert result["scope"]["does_not_prove"]


def test_select_families_ignores_non_family_directories(tmp_path: Path) -> None:
    (tmp_path / "002-two").mkdir()
    (tmp_path / "001-one").mkdir()
    (tmp_path / "score_denominator_registry").mkdir()

    selected = audit.select_families(tmp_path, [], [])

    assert [item.name for item in selected] == ["001-one", "002-two"]


def test_canonical_family_001_has_no_contract_binding_findings() -> None:
    source = (
        ROOT
        / "benchmark-vabench-release-v4"
        / "provenance"
        / "dut-base-v3-exact-five-hash-bound-v2"
    )
    task = audit.select_families(source, ["001"], [])[0]

    shard = audit.audit_family(task)

    assert shard["status"] == "pass"
    assert shard["findings"] == []
    assert "gold_certification_binding" in shard["checks_completed"]
