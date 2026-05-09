#!/usr/bin/env python3
"""Machine-check the vaBench-main-v1 strategy gate.

This audit is intentionally narrow: it checks whether the current repository has
enough factual evidence to proceed from benchmark construction to Main120 model
experiments. It does not claim checker completeness or future toolchain
stability.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _add(checks: list[dict[str, Any]], name: str, ok: bool, details: Any) -> None:
    checks.append({"name": name, "status": "PASS" if ok else "FAIL", "details": details})


def run(root: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    manifest_path = root / "benchmark-vabench-main-v1" / "manifest.json"
    manifest = _json(manifest_path)
    _add(
        checks,
        "manifest_main120_shape",
        manifest.get("pack_count") == 30 and manifest.get("task_count") == 120,
        {"pack_count": manifest.get("pack_count"), "task_count": manifest.get("task_count")},
    )

    forms_by_pack: dict[str, set[str]] = {}
    for task in manifest.get("tasks", []):
        forms_by_pack.setdefault(task.get("pack_id", ""), set()).add(task.get("task_form", ""))
    expected_forms = {"bugfix", "spec-to-va", "end-to-end", "tb-generation"}
    bad_forms = {pack: sorted(forms) for pack, forms in forms_by_pack.items() if forms != expected_forms}
    _add(checks, "four_forms_per_pack", not bad_forms and len(forms_by_pack) == 30, bad_forms)

    semantic = _json(root / "analysis" / "vabench-main-v1_semantic_contract_audit_20260508.json")
    _add(
        checks,
        "semantic_contract_audit",
        semantic.get("status_counts") == {"PASS": 120} and not semantic.get("issue_counts"),
        {"status_counts": semantic.get("status_counts"), "issue_counts": semantic.get("issue_counts")},
    )

    integrity = _json(root / "analysis" / "vabench-main-v1_integrity_audit_20260508.json")
    _add(
        checks,
        "benchmark_integrity_audit",
        integrity.get("overall") == "PASS" and not integrity.get("issue_counts"),
        {"overall": integrity.get("overall"), "issue_counts": integrity.get("issue_counts")},
    )

    leakage = _json(root / "analysis" / "vabench-main-v1_main120_leakage_static_audit_20260508.json")
    _add(
        checks,
        "static_leakage_audit",
        leakage.get("status") == "PASS" and not leakage.get("issues"),
        {"status": leakage.get("status"), "issue_count": len(leakage.get("issues", []))},
    )

    coverage = _json(root / "analysis" / "vabench-main-v1_main120_result_coverage_audit_20260508.json")
    coverage_ok = (
        coverage.get("manifest_tasks") == 120
        and coverage.get("evas", {}).get("covered_pass_tasks") == 120
        and coverage.get("spectre", {}).get("covered_pass_tasks") == 120
        and not coverage.get("evas", {}).get("missing")
        and not coverage.get("spectre", {}).get("missing")
        and not coverage.get("evas", {}).get("extra")
        and not coverage.get("spectre", {}).get("extra")
    )
    _add(checks, "result_coverage_audit", coverage_ok, coverage)

    evas = _json(root / "results" / "vabench-main-v1-main120-gold-evas-2026-05-08" / "summary.json").get("evas", {})
    _add(
        checks,
        "full_main120_evas",
        evas.get("pass_count") == 120 and evas.get("total_tasks") == 120 and not evas.get("fail_tasks"),
        {"pass_count": evas.get("pass_count"), "total_tasks": evas.get("total_tasks"), "fail_count": len(evas.get("fail_tasks", []))},
    )

    spectre = _json(root / "results" / "vabench-main-v1-main120-gold-spectre-jin-2026-05-08" / "summary.json").get("spectre", {})
    _add(
        checks,
        "full_main120_spectre",
        spectre.get("pass_count") == 120 and spectre.get("total_tasks") == 120 and not spectre.get("fail_tasks"),
        {"pass_count": spectre.get("pass_count"), "total_tasks": spectre.get("total_tasks"), "fail_count": len(spectre.get("fail_tasks", []))},
    )

    tracker = (root / "docs" / "VAEVAS_EXPERIMENT_TRACKER.md").read_text(encoding="utf-8")
    _add(
        checks,
        "tracker_main120_done",
        "MAIN120_GOLD_DONE" in tracker and "full strict-EVAS 120/120" in tracker and "full Spectre 120/120" in tracker,
        "MAIN120_GOLD_DONE present" if "MAIN120_GOLD_DONE" in tracker else "MAIN120_GOLD_DONE missing",
    )

    failures = [check for check in checks if check["status"] != "PASS"]
    return {
        "status": "PASS" if not failures else "FAIL",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "current repository state: proceed from Main120 benchmark construction to Main120 model experiments",
        "checks": checks,
        "failure_count": len(failures),
        "failures": failures,
        "decision": "GO" if not failures else "NO_GO",
        "non_claims": [
            "Does not prove checker completeness.",
            "Does not validate future benchmark/toolchain changes.",
            "Does not replace heldout validation for final generalization claims.",
        ],
    }


def write_outputs(data: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# vaBench Strategy Gate Audit",
        "",
        f"- Status: `{data['status']}`",
        f"- Decision: `{data['decision']}`",
        f"- Scope: {data['scope']}",
        "",
        "## Checks",
        "",
        "| Check | Status | Details |",
        "| --- | --- | --- |",
    ]
    for check in data["checks"]:
        details = json.dumps(check["details"], sort_keys=True) if not isinstance(check["details"], str) else check["details"]
        if len(details) > 240:
            details = details[:237] + "..."
        lines.append(f"| `{check['name']}` | `{check['status']}` | `{details}` |")
    lines.extend(["", "## Non-Claims", ""])
    for item in data["non_claims"]:
        lines.append(f"- {item}")
    output.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path("analysis/vabench-main-v1_strategy_gate_audit_20260508.json"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = run(args.root.resolve())
    write_outputs(data, args.output)
    print(json.dumps({"status": data["status"], "decision": data["decision"], "failure_count": data["failure_count"]}, indent=2))
    return 0 if data["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
