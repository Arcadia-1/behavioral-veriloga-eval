#!/usr/bin/env python3
"""Repair and freeze an already materialized tri-form v4 release.

This is intentionally a release-package fixer rather than a full materializer:
the current source release may contain historical replay-plan gaps, while the
materialized tri-form package is otherwise complete.  The fixer updates the
public/testbench contract surface to the current v2 security schema, aligns
reference-deck bindings with the machine-readable contract, refreshes prompt
records, and writes a compact final seal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1]
REPO = PACKAGE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
RUNNERS = PACKAGE / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from materialize_tri_form_release import (  # noqa: E402
    MATERIALIZED_ARTIFACTS,
    MODES,
    build_solver_contract,
    file_sha,
    public_bundle_hash,
    reference_deck_saved_signals,
    render_bugfix_instruction,
    render_dut_instruction,
    render_testbench_instruction,
    write_json,
    write_prompt_records,
)
from testbench_security import (  # noqa: E402
    _INSTANCE_RE,
    _SOURCE_KINDS,
    _logical_lines,
    validate_testbench,
)


DEFAULT_RELEASE = PACKAGE / "release" / "tri-form-v4-1200-final"
INCLUDE_RE = re.compile(r"\b(ahdl_include|include)\s+([\"'])([^\"']+)([\"'])", re.IGNORECASE)
SAVE_RE = re.compile(r"^\s*save\s+(.+)$", re.IGNORECASE)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_compact_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_tree(root: Path, *, exclude: set[str] | None = None) -> str:
    exclude = exclude or set()
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.name != ".DS_Store"):
        relative = path.relative_to(root).as_posix()
        if relative in exclude:
            continue
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def entry_modules(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    modules: dict[str, dict[str, Any]] = {}
    for file_record in (contract.get("artifact_contract") or {}).get("files") or []:
        for module in file_record.get("modules") or []:
            if module.get("role") == "entry":
                modules[str(module["name"]).lower()] = module
    return modules


def port_list(module: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(module.get("ports") or [], key=lambda item: int(item.get("position", 0)))


def support_source_for(task_record: dict[str, Any]) -> Path:
    source = PACKAGE / str(task_record["canonical_dut_source"])
    return source / "public" / "task" / "public_support"


def copy_declared_support(task_dir: Path, task_record: dict[str, Any], support_rel: str) -> bool:
    source_root = support_source_for(task_record)
    source = source_root / support_rel
    if not source.is_file():
        return False
    target = task_dir / "public_support" / support_rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return True


def normalize_reference_includes(
    task_dir: Path,
    task_record: dict[str, Any],
    contract: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, int]]:
    reference = task_dir / "evaluator" / "reference_tb.scs"
    text = reference.read_text(encoding="utf-8")
    supplied = contract.setdefault("supplied_inputs", {})
    dut_items = list(supplied.get("read_only_dut_artifacts") or [])
    support_items = list(supplied.get("read_only_support_artifacts") or [])
    dut_by_name = {
        Path(str(item.get("public_input_path") or "")).name: str(item.get("testbench_include_path") or "")
        for item in dut_items
        if item.get("testbench_include_path")
    }
    support_seen = {
        str(item.get("testbench_include_path") or "")
        for item in support_items
        if item.get("testbench_include_path")
    }
    stats = {"dut_include_normalized": 0, "support_declared": 0, "support_missing_source": 0}

    def repl(match: re.Match[str]) -> str:
        directive, quote, include, close_quote = match.groups()
        include_path = include.replace("\\", "/")
        basename = Path(include_path).name
        if basename in dut_by_name and include_path != dut_by_name[basename]:
            stats["dut_include_normalized"] += 1
            return f"{directive} {quote}{dut_by_name[basename]}{close_quote}"
        support_rel = None
        if include_path.startswith("./support/"):
            support_rel = include_path.removeprefix("./support/")
            normalized = include_path
        elif include_path.startswith("support/"):
            support_rel = include_path.removeprefix("support/")
            normalized = f"./support/{support_rel}"
            stats["support_declared"] += 1
        else:
            normalized = include_path
        if support_rel is not None:
            if normalized not in support_seen:
                if copy_declared_support(task_dir, task_record, support_rel):
                    support_items.append({
                        "public_input_path": f"public_support/{support_rel}",
                        "testbench_include_path": normalized,
                    })
                    support_seen.add(normalized)
                    stats["support_declared"] += 1
                else:
                    stats["support_missing_source"] += 1
            if include_path != normalized:
                return f"{directive} {quote}{normalized}{close_quote}"
        return match.group(0)

    new_text = INCLUDE_RE.sub(repl, text)
    if new_text != text:
        reference.write_text(new_text, encoding="utf-8")
    supplied["read_only_support_artifacts"] = sorted(
        support_items,
        key=lambda item: str(item.get("testbench_include_path") or ""),
    )
    return contract, stats


def actual_dut_bindings(reference: Path, contract: dict[str, Any]) -> list[dict[str, Any]]:
    modules = entry_modules(contract)
    bindings: list[dict[str, Any]] = []
    for line in _logical_lines(reference.read_text(encoding="utf-8")):
        match = _INSTANCE_RE.match(line)
        if not match:
            continue
        name, node_text, kind = match.groups()
        module = modules.get(kind.lower())
        if module is None:
            continue
        nodes = [token for token in re.split(r"[\s,]+", node_text.strip()) if token]
        ports = port_list(module)
        connections = []
        public_outputs = []
        for index, net in enumerate(nodes):
            port = ports[index] if index < len(ports) else {"name": f"port_{index}", "direction": ""}
            connections.append({
                "position": index,
                "port_ref": str(port.get("name") or f"port_{index}"),
                "net": net,
            })
            if str(port.get("direction") or "").lower() == "output":
                public_outputs.append(net)
        bindings.append({
            "name": name,
            "module_ref": str(module["name"]),
            "connections": connections,
            "ordered_nets": nodes,
            "public_output_nets": public_outputs,
        })
    return bindings


def remove_forbidden_output_sources(reference: Path, contract: dict[str, Any]) -> int:
    """Drop obvious voltage/current sources that drive declared DUT outputs.

    This is a narrow repair for legacy reference decks that accidentally drove a
    DUT output while also expecting to observe it.  Zero-DC current anchors are
    kept by the validator, so only non-anchor source instances on output nets
    are removed here.
    """
    output_nets = {
        str(net).lower()
        for binding in (contract.get("supplied_inputs") or {}).get("dut_instances") or []
        for net in binding.get("public_output_nets") or []
    }
    if not output_nets:
        return 0
    removed = 0
    lines = []
    for raw in reference.read_text(encoding="utf-8").splitlines():
        match = _INSTANCE_RE.match(raw)
        if match:
            _name, node_text, kind = match.groups()
            nodes = {token.lower() for token in re.split(r"[\s,]+", node_text.strip()) if token}
            if kind.lower() in _SOURCE_KINDS and output_nets.intersection(nodes):
                if not (kind.lower() == "isource" and re.search(r"\bdc\s*=\s*0(?:\.0+)?\b", raw, re.IGNORECASE)):
                    removed += 1
                    continue
        lines.append(raw)
    if removed:
        reference.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return removed


def build_security_policy(contract: dict[str, Any]) -> dict[str, Any]:
    supplied = contract.get("supplied_inputs") or {}
    allowed = [
        str(item["testbench_include_path"])
        for key in ("read_only_dut_artifacts", "read_only_support_artifacts")
        for item in supplied.get(key) or []
        if item.get("testbench_include_path")
    ]
    required = [
        str(item)
        for item in (contract.get("trace_contract") or {}).get("required_signals") or []
        if str(item).lower() != "time"
    ]
    return {
        "schema_version": "v4-testbench-security-policy-v2",
        "candidate_artifacts": ["testbench.scs"],
        "allowed_include_paths": allowed,
        "forbidden_rules": [
            "undeclared_include",
            "absolute_path",
            "path_traversal",
            "process_execution",
            "network_access",
            "simulator_scripting_escape",
            "dut_redefinition",
            "direct_dut_output_drive",
            "private_hierarchical_probe",
            "unbounded_resource_use",
        ],
        "required_rules": [
            "declared_dut_binding",
            "transient_analysis",
            "all_required_public_traces",
        ],
        "limits": {
            "max_candidate_bytes": 1_000_000,
            "max_cpu_time_s": 120,
            "max_memory_mb": 2048,
            "max_output_bytes": 100_000_000,
            "max_wall_time_s": 180,
            "max_stop_time_s": 1.0,
            "max_analyses": 1,
            "max_saved_signals": max(64, len(required) + 16),
        },
        "rejection_outcome": "invalid_run",
    }


def refresh_trace_contract_from_reference(contract: dict[str, Any], reference: Path) -> None:
    required = reference_deck_saved_signals(reference)
    contract["trace_contract"] = {"required_signals": required}
    for prop in contract.get("properties") or []:
        prop["required_signals"] = required


def repair_testbench_task(task_dir: Path) -> dict[str, Any]:
    task_record = read_json(task_dir / "TASK_RECORD.json")
    contract = read_json(task_dir / "public_contract.json")
    reference = task_dir / "evaluator" / "reference_tb.scs"
    stats: dict[str, Any] = {"task": task_dir.name}
    contract, include_stats = normalize_reference_includes(task_dir, task_record, contract)
    stats.update(include_stats)
    bindings = actual_dut_bindings(reference, contract)
    if bindings:
        old_bindings = (contract.get("supplied_inputs") or {}).get("dut_instances") or []
        if old_bindings != bindings:
            stats["binding_refreshed"] = 1
        contract.setdefault("supplied_inputs", {})["dut_instances"] = bindings
    removed_sources = remove_forbidden_output_sources(reference, contract)
    stats["output_sources_removed"] = removed_sources
    refresh_trace_contract_from_reference(contract, reference)
    policy = build_security_policy(contract)
    contract["security_policy"] = policy
    write_json(task_dir / "public_contract.json", contract)
    write_compact_json(task_dir / "solver_contract.json", build_solver_contract(contract))
    write_json(task_dir / "evaluator" / "testbench_security_policy.json", policy)
    (task_dir / "instruction.md").write_text(render_testbench_instruction(contract), encoding="utf-8")
    cert_path = task_dir / "evaluator" / "reference_certificate.json"
    if cert_path.is_file():
        cert = read_json(cert_path)
        cert["reference_tb_sha256"] = file_sha(reference)
        note = "reference deck, public contract, and v2 security policy aligned during final release freeze"
        notes = [item for item in cert.get("release_repair_notes") or [] if item != note]
        notes.append(note)
        cert["release_repair_notes"] = notes
        write_json(cert_path, cert)
    validation = validate_testbench(reference, contract, policy)
    stats["reference_valid"] = validation.valid
    stats["diagnostics"] = list(validation.diagnostics)
    return stats


def refresh_solver_contract_view(task_dir: Path, form: str) -> None:
    contract = read_json(task_dir / "public_contract.json")
    write_compact_json(task_dir / "solver_contract.json", build_solver_contract(contract))
    if form == "dut":
        (task_dir / "instruction.md").write_text(render_dut_instruction(contract), encoding="utf-8")
    elif form == "bugfix":
        (task_dir / "instruction.md").write_text(render_bugfix_instruction(contract), encoding="utf-8")
    elif form == "testbench":
        (task_dir / "instruction.md").write_text(render_testbench_instruction(contract), encoding="utf-8")


def refresh_task_record(task_dir: Path) -> None:
    record_path = task_dir / "TASK_RECORD.json"
    record = read_json(record_path)
    record["public_bundle_sha256"] = public_bundle_hash(task_dir)
    write_json(record_path, record)


def load_skill_records(release: Path) -> dict[str, dict[str, Any]]:
    return read_json(release / "prompt_modes" / "skills" / "manifest.json")["skills"]


def refresh_prompt_records(release: Path) -> None:
    task_rows = read_json(release / "TASK_INDEX.json")["tasks"]
    write_prompt_records(release, task_rows, load_skill_records(release))


def refresh_release_metadata(release: Path, repair_rows: list[dict[str, Any]]) -> None:
    manifest_path = release / "MANIFEST.json"
    manifest = read_json(manifest_path) if manifest_path.is_file() else {}
    counts = {"dut": 0, "testbench": 0, "bugfix": 0}
    for row in read_json(release / "TASK_INDEX.json")["tasks"]:
        counts[str(row.get("form"))] = counts.get(str(row.get("form")), 0) + 1
    artifact_sha256 = {
        relative: file_sha(release / relative)
        for relative in MATERIALIZED_ARTIFACTS
        if (release / relative).is_file()
    }
    missing_artifacts = [
        relative
        for relative in MATERIALIZED_ARTIFACTS
        if not (release / relative).is_file()
    ]
    manifest.update({
        "schema_version": "v4-tri-form-release-manifest-v1",
        "release_status": "final_static_tb_security_v2_fixed",
        "release_name": release.name,
        "frozen_at": now(),
        "task_count": sum(counts.values()),
        "task_counts": counts,
        "prompt_record_count": sum(counts.values()) * len(MODES),
        "testbench_repair_summary": {
            "task_count": len(repair_rows),
            "reference_valid_count": sum(1 for row in repair_rows if row.get("reference_valid")),
            "reference_invalid_count": sum(1 for row in repair_rows if not row.get("reference_valid")),
            "dut_include_normalized_count": sum(int(row.get("dut_include_normalized", 0)) for row in repair_rows),
            "support_declared_count": sum(int(row.get("support_declared", 0)) for row in repair_rows),
            "binding_refreshed_count": sum(int(row.get("binding_refreshed", 0)) for row in repair_rows),
            "output_sources_removed_count": sum(int(row.get("output_sources_removed", 0)) for row in repair_rows),
        },
        "materialized_artifact_sha256": artifact_sha256,
        "missing_historical_materializer_artifacts": missing_artifacts,
    })
    write_json(manifest_path, manifest)
    write_json(release / "manifest.json", manifest)
    write_json(release / "AUDIT_REPORT.json", {
        "schema_version": "v4-tri-form-final-freeze-audit-v1",
        "release_name": release.name,
        "created_at": now(),
        "testbench_repair_summary": manifest["testbench_repair_summary"],
        "reference_invalid_tasks": [
            {"task": row["task"], "diagnostics": row["diagnostics"]}
            for row in repair_rows
            if not row.get("reference_valid")
        ],
    })
    seal = {
        "schema_version": "v4-tri-form-release-seal-v2",
        "release_name": release.name,
        "release_status": manifest["release_status"],
        "sealed_at": now(),
        "tree_sha256": sha_tree(release, exclude={"RELEASE_SEAL.json"}),
        "artifact_sha256": {
            path.relative_to(release).as_posix(): file_sha(path)
            for path in [
                release / "MANIFEST.json",
                release / "TASK_INDEX.json",
                release / "BUGFIX_SEED_REVIEW.json",
                release / "AUDIT_REPORT.json",
                release / "RUNTIME_INGESTION_EVIDENCE.json",
                release / "prompt_modes" / "modes.json",
                release / "prompt_modes" / "skills" / "manifest.json",
                release / "prompt_modes" / "PROMPT_RECORDS.jsonl",
            ]
            if path.is_file()
        },
        "simulation_claim": "not established by this static seal",
        "spectre_final_judge": True,
    }
    write_json(release / "RELEASE_SEAL.json", seal)


def remove_ds_store(release: Path) -> int:
    count = 0
    for path in release.rglob(".DS_Store"):
        path.unlink()
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    release = args.release.expanduser().resolve()
    if not release.is_dir():
        raise SystemExit(f"release not found: {release}")
    removed_ds = remove_ds_store(release)
    repair_rows = []
    for task_dir in sorted((release / "tasks" / "testbench").glob("*")):
        if not task_dir.is_dir():
            continue
        repair_rows.append(repair_testbench_task(task_dir))
    for row in read_json(release / "TASK_INDEX.json")["tasks"]:
        refresh_solver_contract_view(release / str(row["task_dir"]), str(row["form"]))
        refresh_task_record(release / str(row["task_dir"]))
    refresh_prompt_records(release)
    refresh_release_metadata(release, repair_rows)
    summary = {
        "release": str(release),
        "removed_ds_store": removed_ds,
        "testbench_tasks": len(repair_rows),
        "reference_valid": sum(1 for row in repair_rows if row.get("reference_valid")),
        "reference_invalid": sum(1 for row in repair_rows if not row.get("reference_valid")),
        "invalid_examples": [
            {"task": row["task"], "diagnostics": row["diagnostics"]}
            for row in repair_rows
            if not row.get("reference_valid")
        ][:20],
    }
    print(json.dumps(summary, indent=2 if args.json else None, sort_keys=True))
    return 0 if summary["reference_invalid"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
