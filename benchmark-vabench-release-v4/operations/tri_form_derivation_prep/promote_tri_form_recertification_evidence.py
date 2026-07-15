#!/usr/bin/env python3
"""Promote benchmarkv4 EVAS+Spectre correct+5 reruns into compact evidence.

Raw simulator reports include local checkout paths, remote Spectre workdirs,
CSV locations, and verbose logs. This promoter verifies those reports against
the current ``release/benchmarkv4`` task tree and writes a repository-safe
aggregate evidence file with only task-relative source bindings and hashes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RELEASE = PACKAGE_ROOT / "release" / "benchmarkv4"
SCHEMA_VERSION = "v4-benchmarkv4-recertification-evidence-v1"
ABSOLUTE_PATH_RE = re.compile(r"(?<![A-Za-z0-9_.-])/(?:[^\s\"'<>]+)")


class PromotionError(ValueError):
    """Raised when raw evidence is not exactly bound to the release tree."""


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise PromotionError(f"expected JSON object: {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_fingerprint(records: Iterable[dict[str, str]]) -> str:
    digest = hashlib.sha256()
    for record in sorted(records, key=lambda item: item["path"]):
        digest.update(record["path"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(record["sha256"].encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def clean_text(value: Any) -> str:
    return ABSOLUTE_PATH_RE.sub("<path>", str(value))


def clean_lines(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    return sorted({clean_text(item) for item in values if str(item).strip()})


def relative_to_release(release: Path, path: Path) -> str:
    path = path.resolve()
    try:
        return path.relative_to(release).as_posix()
    except ValueError as exc:
        raise PromotionError(f"evidence path escapes release root: {path}") from exc


def file_record(release: Path, path: Path) -> dict[str, str]:
    if not path.is_file():
        raise PromotionError(f"evidence source file is missing: {path}")
    return {"path": relative_to_release(release, path), "sha256": file_sha(path)}


def tool_sha(path: Path) -> dict[str, str]:
    return {"path": path.relative_to(PACKAGE_ROOT.parent).as_posix(), "sha256": file_sha(path)}


def git_commit(path: Path) -> str:
    completed = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip() if completed.returncode == 0 else ""


def release_task_rows(release: Path, requested: set[str] | None) -> dict[str, dict[str, Any]]:
    index = read_json(release / "TASK_INDEX.json")
    rows = {
        str(row.get("task_id")): row
        for row in index.get("tasks") or []
        if row.get("form") == "testbench"
    }
    if requested:
        missing = sorted(requested - set(rows))
        if missing:
            raise PromotionError(f"unknown testbench task id(s): {', '.join(missing)}")
        rows = {task_id: rows[task_id] for task_id in sorted(requested)}
    return rows


def case_id_from_evas_case(case: dict[str, Any]) -> str:
    mutation = case.get("mutation_id")
    return "correct" if mutation in (None, "") else str(mutation)


def case_id_from_spectre_case(case: dict[str, Any]) -> str:
    return "correct" if case.get("case_kind") == "correct" else str(case.get("case_id"))


def expected_case_ids(task_dir: Path) -> list[str]:
    score = read_json(task_dir / "evaluator" / "score_policy.json")
    mutation_ids = list(score.get("negative_suite_mutation_ids") or [])
    if (
        len(mutation_ids) != 5
        or len(set(mutation_ids)) != 5
        or not all(isinstance(item, str) and item for item in mutation_ids)
        or score.get("kill_ratio_denominator") != 5
    ):
        raise PromotionError(f"{task_dir.name}: score policy is not exact-five")
    return ["correct", *mutation_ids]


def require_evas_task(result: dict[str, Any], task_dir: Path, cases: list[str]) -> None:
    if result.get("status") != "pass":
        raise PromotionError(f"{result.get('task_id')}: EVAS result is not pass")
    if result.get("reference_pass") is not True:
        raise PromotionError(f"{result.get('task_id')}: EVAS reference gate failed")
    if result.get("mutation_count") != 5 or result.get("mutation_kill_count") != 5:
        raise PromotionError(f"{result.get('task_id')}: EVAS did not kill exact-five")
    if result.get("infrastructure_error_count") or result.get("mutation_survivor_count"):
        raise PromotionError(f"{result.get('task_id')}: EVAS has infra errors or survivors")

    raw_cases = {case_id_from_evas_case(case): case for case in result.get("cases") or []}
    if set(raw_cases) != set(cases):
        raise PromotionError(f"{result.get('task_id')}: EVAS cases do not match score policy")
    reference_sha = file_sha(task_dir / "evaluator" / "reference_tb.scs")
    for case_id in cases:
        case = raw_cases[case_id]
        expected_status = "reference_pass" if case_id == "correct" else "mutation_killed"
        if case.get("status") != expected_status:
            raise PromotionError(f"{result.get('task_id')}:{case_id}: EVAS status mismatch")
        if case.get("reference_tb_sha256") != reference_sha:
            raise PromotionError(f"{result.get('task_id')}:{case_id}: EVAS deck hash mismatch")


def require_spectre_task(result: dict[str, Any], cases: list[str]) -> None:
    task_id = str(result.get("task_id") or "")
    if result.get("status") != "PASS":
        raise PromotionError(f"{task_id}: Spectre result is not PASS")
    if result.get("reference_gate") is not True:
        raise PromotionError(f"{task_id}: Spectre reference gate failed")
    if result.get("kill_denominator") != 5 or result.get("killed_count") != 5:
        raise PromotionError(f"{task_id}: Spectre did not kill exact-five")
    if result.get("invalid_count") or result.get("survived_count") or result.get("skipped_count"):
        raise PromotionError(f"{task_id}: Spectre has invalid/survived/skipped cases")
    if result.get("untriaged_warning_lines"):
        raise PromotionError(f"{task_id}: Spectre has untriaged warnings")
    raw_cases = {case_id_from_spectre_case(case): case for case in result.get("cases") or []}
    if set(raw_cases) != set(cases):
        raise PromotionError(f"{task_id}: Spectre cases do not match score policy")
    for case_id in cases:
        case = raw_cases[case_id]
        expected_outcome = "reference_pass" if case_id == "correct" else "killed_behaviorally"
        expected_observed = "behavior_pass" if case_id == "correct" else "behavior_fail"
        if case.get("outcome") != expected_outcome or case.get("observed") != expected_observed:
            raise PromotionError(f"{task_id}:{case_id}: Spectre behavior mismatch")
        spectre = case.get("spectre") or {}
        if spectre.get("ok") is not True:
            raise PromotionError(f"{task_id}:{case_id}: Spectre simulation did not succeed")


def compact_case(
    *,
    release: Path,
    case_id: str,
    spectre_case: dict[str, Any],
    evas_case: dict[str, Any],
) -> dict[str, Any]:
    source_files = [Path(item) for item in spectre_case.get("include_paths") or []]
    if not source_files:
        raise PromotionError(f"{case_id}: Spectre case has no source include bindings")
    candidate_files = [file_record(release, path) for path in source_files]
    return {
        "case_id": case_id,
        "role": "correct" if case_id == "correct" else "negative",
        "expected": "behavior_pass" if case_id == "correct" else "behavior_fail",
        "observed": "behavior_pass" if case_id == "correct" else "behavior_fail",
        "outcome": "reference_pass" if case_id == "correct" else "killed_behaviorally",
        "candidate_bundle_sha256": tree_fingerprint(candidate_files),
        "candidate_files": candidate_files,
        "evas": {
            "status": evas_case.get("status"),
            "checker_ok": bool(evas_case.get("checker_ok")),
            "engine": evas_case.get("evas_engine"),
            "notes": clean_lines(evas_case.get("checker_notes")),
        },
        "spectre": {
            "outcome": spectre_case.get("outcome"),
            "behavior_score": spectre_case.get("behavior_score"),
            "notes": clean_lines(spectre_case.get("behavior_notes")),
            "benign_warning_count": len(spectre_case.get("benign_warning_lines") or []),
            "untriaged_warning_count": len(spectre_case.get("untriaged_warning_lines") or []),
        },
    }


def promote(
    *,
    release: Path,
    evas_report_path: Path,
    spectre_report_path: Path,
    task_ids: set[str] | None,
) -> dict[str, Any]:
    release = release.resolve()
    evas_report_path = evas_report_path.resolve()
    spectre_report_path = spectre_report_path.resolve()
    evas_report = read_json(evas_report_path)
    spectre_report = read_json(spectre_report_path)
    if evas_report.get("schema_version") != "v4-reference-evas-smoke-v1":
        raise PromotionError("unsupported EVAS report schema")
    if (
        spectre_report.get("schema_version")
        != "v4-benchmarkv4-reference-spectre-correct-plus-five-audit-v1"
    ):
        raise PromotionError("unsupported Spectre report schema")

    rows = release_task_rows(release, task_ids)
    evas_by_task = {str(item.get("task_id")): item for item in evas_report.get("results") or []}
    spectre_by_task = {str(item.get("task_id")): item for item in spectre_report.get("results") or []}
    if set(rows) - set(evas_by_task) or set(rows) - set(spectre_by_task):
        missing_evas = sorted(set(rows) - set(evas_by_task))
        missing_spectre = sorted(set(rows) - set(spectre_by_task))
        raise PromotionError(
            f"raw reports are missing tasks: evas={missing_evas} spectre={missing_spectre}"
        )

    tasks: list[dict[str, Any]] = []
    for task_id, row in rows.items():
        task_dir = release / str(row["task_dir"])
        task_record = read_json(task_dir / "task_record.json")
        family = str(task_record.get("family_id") or row.get("family_id") or "")
        cases = expected_case_ids(task_dir)
        evas_result = evas_by_task[task_id]
        spectre_result = spectre_by_task[task_id]
        require_evas_task(evas_result, task_dir, cases)
        require_spectre_task(spectre_result, cases)
        evas_cases = {case_id_from_evas_case(case): case for case in evas_result.get("cases") or []}
        spectre_cases = {
            case_id_from_spectre_case(case): case for case in spectre_result.get("cases") or []
        }
        reference_tb = task_dir / "evaluator" / "reference_tb.scs"
        runtime_reference_tb = Path(str(spectre_result.get("reference_tb") or ""))
        if not runtime_reference_tb.is_file() or file_sha(runtime_reference_tb) != file_sha(reference_tb):
            raise PromotionError(f"{task_id}: Spectre reference deck is not bound to release")

        compact_cases = [
            compact_case(
                release=release,
                case_id=case_id,
                spectre_case=spectre_cases[case_id],
                evas_case=evas_cases[case_id],
            )
            for case_id in cases
        ]
        checker_profile = task_dir / "evaluator" / "checker_profile.json"
        tasks.append(
            {
                "task_id": task_id,
                "family_id": family,
                "form": "testbench",
                "task_dir": str(row["task_dir"]),
                "reference_tb": file_record(release, reference_tb),
                "checker": {
                    "task_id": str(spectre_result.get("checker_task_id") or ""),
                    "profile": file_record(release, checker_profile),
                },
                "reference_gate": "pass",
                "kill_denominator": 5,
                "killed_count": 5,
                "untriaged_warning_count": 0,
                "status": "pass",
                "cases": compact_cases,
            }
        )

    tasks.sort(key=lambda item: item["task_id"])
    return {
        "schema_version": SCHEMA_VERSION,
        "claim_scope": "fresh_benchmarkv4_correct_plus_five_evas_spectre_recertification",
        "release": {
            "path": "benchmark-vabench-release-v4/release/benchmarkv4",
            "git_commit": git_commit(PACKAGE_ROOT.parent),
            "task_index_sha256": file_sha(release / "TASK_INDEX.json"),
        },
        "raw_reports": {
            "evas": {
                "schema_version": evas_report.get("schema_version"),
                "sha256": file_sha(evas_report_path),
                "task_count": evas_report.get("task_count"),
                "pass_count": evas_report.get("pass_count"),
            },
            "spectre": {
                "schema_version": spectre_report.get("schema_version"),
                "sha256": file_sha(spectre_report_path),
                "task_count": spectre_report.get("task_count"),
                "pass_count": spectre_report.get("pass_count"),
                "untriaged_warning_count": spectre_report.get("untriaged_warning_count"),
            },
        },
        "tool_fingerprints": {
            "promotion": tool_sha(Path(__file__)),
            "evas_runner": tool_sha(PACKAGE_ROOT / "operations" / "tri_form_derivation_prep" / "run_v4_reference_evas_smoke.py"),
            "spectre_runner": tool_sha(PACKAGE_ROOT / "operations" / "tri_form_derivation_prep" / "audit_tri_form_reference_spectre.py"),
        },
        "summary": {
            "task_count": len(tasks),
            "family_count": len({task["family_id"] for task in tasks}),
            "reference_pass_count": len(tasks),
            "negative_case_count": 5 * len(tasks),
            "evas_behavioral_kill_count": 5 * len(tasks),
            "spectre_behavioral_kill_count": 5 * len(tasks),
            "untriaged_warning_count": 0,
            "status": "pass",
        },
        "tasks": tasks,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument("--evas-report", type=Path, required=True)
    parser.add_argument("--spectre-report", type=Path, required=True)
    parser.add_argument("--task-id", action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        evidence = promote(
            release=args.release,
            evas_report_path=args.evas_report,
            spectre_report_path=args.spectre_report,
            task_ids=set(args.task_id) or None,
        )
    except (OSError, json.JSONDecodeError, PromotionError) as exc:
        raise SystemExit(f"promotion failed: {exc}") from exc
    write_json(args.output, evidence)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
