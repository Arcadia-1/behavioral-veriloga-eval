#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "benchmark-vabench-release-v1" / "vabench-300-expansion"
MANIFEST = EXPANSION / "VABENCH_300_MANIFEST.json"
REPORT_JSON = EXPANSION / "negative_audit.json"
REPORT_MD = EXPANSION / "negative_audit.md"
EXPECTED_NEGATIVE_KINDS = {
    "boundary_near_miss",
    "timing_window_near_miss",
    "polarity_direction_near_miss",
    "state_reset_near_miss",
    "metric_writeout_near_miss",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def module_signature(text: str) -> str:
    match = re.search(r"\bmodule\s+([A-Za-z_][A-Za-z0-9_$]*)\s*\(([^;]*)\)\s*;", text, re.DOTALL)
    if not match:
        return ""
    ports = " ".join(match.group(2).replace("\n", " ").split())
    return f"{match.group(1)}({ports})"


def scs_has_testbench_shape(text: str) -> bool:
    lowered = text.lower()
    return "simulator lang=spectre" in lowered or "tran " in lowered or "ahdl_include" in lowered


def shallow_static_checks(source: Path, negative: Path) -> tuple[list[str], list[str]]:
    source_text = source.read_text(encoding="utf-8", errors="ignore")
    negative_text = negative.read_text(encoding="utf-8", errors="ignore")
    passes: list[str] = []
    failures: list[str] = []
    if negative_text.strip():
        passes.append("non_empty_candidate")
    else:
        failures.append("candidate is empty")
    if negative_text != source_text:
        passes.append("differs_from_reference")
    else:
        failures.append("candidate is identical to reference")
    if negative.suffix == ".va":
        source_sig = module_signature(source_text)
        negative_sig = module_signature(negative_text)
        if source_sig and negative_sig:
            passes.append("veriloga_module_signature_present")
            if source_sig == negative_sig:
                passes.append("veriloga_interface_preserved")
            else:
                failures.append(f"module signature changed: {source_sig!r} -> {negative_sig!r}")
        else:
            failures.append("missing Verilog-A module signature")
        if "analog" in negative_text:
            passes.append("analog_block_or_keyword_present")
        else:
            failures.append("missing analog behavior keyword")
    elif negative.suffix == ".scs":
        if scs_has_testbench_shape(negative_text):
            passes.append("spectre_testbench_shape_preserved")
        else:
            failures.append("missing Spectre testbench shape")
    else:
        passes.append("unsupported_suffix_metadata_only")
    return passes, failures


def audit() -> dict[str, Any]:
    manifest = read_json(MANIFEST)
    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    total_negatives = 0
    shallow_static_pass_count = 0
    for task in manifest["tasks"]:
        task_id = str(task["task_id"])
        negative_manifest_path = ROOT / str(task["negative_manifest"])
        if not negative_manifest_path.exists():
            failures.append(f"{task_id}: missing negative manifest {negative_manifest_path}")
            continue
        payload = read_json(negative_manifest_path)
        negatives = payload.get("negatives", [])
        total_negatives += len(negatives)
        task_failures: list[str] = []
        if payload.get("task_id") != task_id:
            task_failures.append("task_id mismatch")
        if payload.get("negative_count") != 5:
            task_failures.append("negative_count is not 5")
        if len(negatives) != 5:
            task_failures.append("negative list length is not 5")
        kinds = {str(negative.get("kind")) for negative in negatives}
        if kinds != EXPECTED_NEGATIVE_KINDS:
            task_failures.append(f"negative kind set mismatch: {sorted(kinds)}")
        for negative in negatives:
            source = ROOT / str(negative.get("source", ""))
            if not source.exists():
                task_failures.append(f"missing source {negative.get('source')}")
                continue
            derived_from = ROOT / str(negative.get("derived_from", ""))
            if not derived_from.exists():
                task_failures.append(f"missing derived_from {negative.get('derived_from')}")
                continue
            expected_hash = str(negative.get("sha256", ""))
            actual_hash = sha256(source)
            if actual_hash != expected_hash:
                task_failures.append(f"sha256 mismatch for {negative.get('id')}")
            if negative.get("expected") != "FAIL_FULL_CHECKER":
                task_failures.append(f"{negative.get('id')}: expected is not FAIL_FULL_CHECKER")
            if not negative.get("shallow_passes"):
                task_failures.append(f"{negative.get('id')}: missing shallow_passes")
            if not negative.get("full_failures"):
                task_failures.append(f"{negative.get('id')}: missing full_failures")
            if negative.get("kind") not in set(negative.get("full_failures", [])):
                task_failures.append(f"{negative.get('id')}: full_failures does not include its negative kind")
            validation = negative.get("validation_evidence")
            if not isinstance(validation, dict):
                task_failures.append(f"{negative.get('id')}: missing validation_evidence")
                validation = {}
                negative["validation_evidence"] = validation
            if validation.get("simulator_shallow_lane") not in {
                "pending_external_evas_spectre",
                "pending_local_evas",
                "pass",
            }:
                task_failures.append(f"{negative.get('id')}: invalid simulator_shallow_lane")
            if validation.get("full_checker_lane") not in {
                "pending_external_evas_spectre",
                "pending_local_evas",
                "fail_as_expected",
                "pass",
            }:
                task_failures.append(f"{negative.get('id')}: invalid full_checker_lane")
            if validation.get("publication_status") not in {
                "asset_ready_not_simulator_certified",
                "simulator_validated_partial_pass",
                "pending_fresh_evas_and_spectre",
                "evas_full_checker_verified_spectre_pending",
            }:
                task_failures.append(f"{negative.get('id')}: invalid publication_status")
            shallow_passes, shallow_failures = shallow_static_checks(derived_from, source)
            if shallow_failures:
                task_failures.extend(f"{negative.get('id')}: {failure}" for failure in shallow_failures)
            else:
                shallow_static_pass_count += 1
                validation["static_shallow_shape"] = "pass"
            negative["shallow_static_passes"] = shallow_passes
            negative["shallow_static_failures"] = shallow_failures
        write_json(negative_manifest_path, payload)
        rows.append(
            {
                "task_id": task_id,
                "negative_manifest": task["negative_manifest"],
                "negative_count": len(negatives),
                "status": "fail" if task_failures else "pass",
                "failures": task_failures,
            }
        )
        failures.extend(f"{task_id}: {item}" for item in task_failures)
    return {
        "status": "pass" if not failures else "fail",
        "task_count": len(manifest["tasks"]),
        "negative_count": total_negatives,
        "shallow_static_pass_count": shallow_static_pass_count,
        "shallow_static_failed_count": total_negatives - shallow_static_pass_count,
        "issue_count": len(failures),
        "issues": failures,
        "task_reports": rows,
        "claim_boundary": [
        "This audit verifies asset presence, metadata integrity, and static shallow shape.",
        "It does not prove that each negative passes shallow simulation or fails full EVAS/Spectre checks.",
        ],
    }


def write_report(report: dict[str, Any]) -> None:
    manifest = read_json(MANIFEST)
    previous_summary = dict(manifest.get("summary", {}))
    simulator_verified = previous_summary.get("negative_simulator_shallow_verified_count", 0)
    full_checker_verified = previous_summary.get("negative_full_checker_fail_verified_count", 0)
    manifest.setdefault("summary", {})["negative_static_shallow_shape_verified_count"] = report[
        "shallow_static_pass_count"
    ]
    manifest.setdefault("summary", {})["negative_simulator_shallow_verified_count"] = simulator_verified
    manifest.setdefault("summary", {})["negative_full_checker_fail_verified_count"] = full_checker_verified
    write_json(MANIFEST, manifest)
    write_json(REPORT_JSON, report)
    lines = [
        "# vaBench 300 Negative Audit",
        "",
        f"- status: `{report['status']}`",
        f"- tasks: {report['task_count']}",
        f"- negatives: {report['negative_count']}",
        f"- shallow static pass: {report['shallow_static_pass_count']}",
        f"- shallow static failed: {report['shallow_static_failed_count']}",
        f"- simulator shallow verified: {simulator_verified}",
        f"- full checker fail verified: {full_checker_verified}",
        f"- issues: {report['issue_count']}",
        "",
        "This audit checks file existence, hashes, counts, required negative categories, metadata, and static shallow shape. It is not simulator certification.",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    report = audit()
    write_report(report)
    print(f"vabench-300 negative audit {report['status']}: {report['negative_count']} negatives, {report['issue_count']} issues")
    if report["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
