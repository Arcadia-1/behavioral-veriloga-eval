#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
EVIDENCE_ROOT = PACKAGE_ROOT / "evidence" / "dual"
DUAL_REPORT_JSON = PACKAGE_ROOT / "reports" / "dual_certification.json"
DUAL_REPORT_MD = PACKAGE_ROOT / "reports" / "dual_certification.md"
IMPORT_REPORT_JSON = PACKAGE_ROOT / "reports" / "dual_rerun_import.json"
IMPORT_REPORT_MD = PACKAGE_ROOT / "reports" / "dual_rerun_import.md"
DEFAULT_SUMMARY_JSON = ROOT / "results" / "vabench-release-v1-dual-rerun" / "summary.json"
DUAL_RERUN_QUEUE_JSON = PACKAGE_ROOT / "reports" / "dual_rerun_queue.json"
PRIMARY_VARIANTS = {"gold", "fixed"}
DUAL_REFRESH_BLOCKERS = {
    "evas_certification",
    "spectre_certification",
    "fresh_dual_validation",
    "fresh_evas_spectre_dual_refresh_pending",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_entries() -> dict[str, tuple[Path, dict[str, object]]]:
    entries: dict[str, tuple[Path, dict[str, object]]] = {}
    for path in sorted(TASKS_ROOT.glob("*/vbr1_*/release_entry.json")):
        payload = read_json(path)
        entries[str(payload["release_entry_id"])] = (path, payload)
    return entries


def primary_result_rows(summary: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in summary.get("results", []):
        if not isinstance(item, dict):
            continue
        if str(item.get("variant")) not in PRIMARY_VARIANTS:
            continue
        if str(item.get("expected_result")) != "pass":
            continue
        rows.append(item)
    return rows


def current_queue_count() -> int | None:
    queue = read_json(DUAL_RERUN_QUEUE_JSON)
    if not queue:
        return None
    try:
        return int(queue.get("queue_count", 0))
    except (TypeError, ValueError):
        return None


def summary_task_count(summary: dict[str, object]) -> int | None:
    try:
        return int(summary.get("tasks_total", 0))
    except (TypeError, ValueError):
        return None


def stale_summary_reason(
    *,
    summary_tasks_total: int | None,
    queue_count: int | None,
    primary_result_count: int | None = None,
    original_reason: object,
) -> str | None:
    if summary_tasks_total is None or queue_count is None:
        return None
    if summary_tasks_total == queue_count:
        return None
    if primary_result_count == queue_count:
        return None
    suffix = f" last rerun blocker: {original_reason}" if original_reason else ""
    return (
        "stale dual rerun summary: "
        f"summary tasks_total={summary_tasks_total}, primary_result_count={primary_result_count}, "
        f"current queue_count={queue_count}; "
        f"rerun the current EVAS/Spectre queue before import.{suffix}"
    )


def backend_status(raw: dict[str, object], backend: str) -> str:
    if backend == "evas":
        evas = raw.get("evas", {})
        if isinstance(evas, dict) and evas.get("status") == "PASS":
            return "pass"
        return "fail"
    if backend == "spectre":
        spectre = raw.get("spectre", {})
        if isinstance(spectre, dict) and spectre_license_blocker(spectre):
            return "pending"
        if isinstance(spectre, dict) and spectre.get("ok") is True and float(spectre.get("behavior_score", 0.0)) >= 1.0:
            return "pass"
        return "fail"
    raise ValueError(f"unknown backend: {backend}")


def spectre_license_blocker(spectre: dict[str, object]) -> bool:
    errors = spectre.get("errors", [])
    error_text = " ".join(str(item) for item in errors) if isinstance(errors, list) else str(errors)
    stdout_tail = str(spectre.get("stdout_tail", ""))
    combined = f"{error_text}\n{stdout_tail}"
    return "SPECTRE-209" in combined or "required license could not be checked out" in combined


def external_pending_blockers(raw: dict[str, object]) -> list[str]:
    spectre = raw.get("spectre", {})
    if isinstance(spectre, dict) and spectre_license_blocker(spectre):
        return [
            "Spectre license checkout failed on thu-sui direct-SUI rerun (SPECTRE-209); current gold EVAS/checker passed."
        ]
    return []


def raw_result_status(row: dict[str, object]) -> str:
    raw = row.get("raw_result", {})
    if isinstance(raw, dict):
        return str(raw.get("status", "UNKNOWN"))
    return "UNKNOWN"


def result_is_certified(row: dict[str, object]) -> bool:
    return row.get("expected_result_met") is True and raw_result_status(row) == "PASS"


def task_by_form(entry: dict[str, object], form: str) -> dict[str, object] | None:
    for task in entry.get("release_tasks", []):
        if isinstance(task, dict) and str(task.get("form")) == form:
            return task
    return None


def write_backend_result(
    *,
    evidence_dir: Path,
    row: dict[str, object],
    backend: str,
    status: str,
    evidence_path: Path,
) -> str:
    raw = row.get("raw_result", {})
    raw_backend = raw.get(backend, {}) if isinstance(raw, dict) else {}
    if not isinstance(raw_backend, dict):
        raw_backend = {}
    result_path = evidence_dir / f"{backend}_result.json"
    result = {
        "task_id": f"{row['entry_id']}:{row['form']}",
        "release_entry_id": row["entry_id"],
        "source_task_id": raw.get("task_id", row.get("source_task_id")) if isinstance(raw, dict) else row.get("source_task_id"),
        "backend": backend,
        "status": (
            "PASS"
            if status == "pass"
            else ("PENDING" if status == "pending" else "FAIL_SIM_CORRECTNESS")
        ),
        "scores": {
            "rerun_backend_pass": status == "pass",
            "rerun_expected_result_met": row.get("expected_result_met"),
            "raw_status": raw_result_status(row),
            "behavior_score": raw_backend.get("behavior_score"),
        },
        "artifacts": [
            str(row.get("result_root", "")),
            rel(evidence_path),
        ],
        "notes": [
            "Imported from fresh vaBench release EVAS/Spectre dual rerun summary.",
        ],
    }
    write_json(result_path, result)
    return rel(result_path)


def update_release_task_manifest(
    *,
    task: dict[str, object],
    evas: str,
    spectre: str,
    evidence_path: Path,
) -> None:
    release_path = str(task.get("release_path", ""))
    if not release_path:
        return
    manifest_path = ROOT / release_path / "release_task.json"
    if not manifest_path.exists():
        return
    manifest = read_json(manifest_path)
    certification = manifest.setdefault("certification", {})
    if not isinstance(certification, dict):
        certification = {}
        manifest["certification"] = certification
    certification.setdefault("static", task.get("static_status", "pending"))
    certification["evas"] = evas
    certification["spectre"] = spectre
    certification["evidence"] = rel(evidence_path)
    write_json(manifest_path, manifest)


def write_task_evidence(
    *,
    entry: dict[str, object],
    task: dict[str, object],
    row: dict[str, object],
    summary_path: Path,
) -> dict[str, object]:
    entry_id = str(row["entry_id"])
    form = str(row["form"])
    raw = row.get("raw_result", {})
    if not isinstance(raw, dict):
        raw = {}
    evidence_dir = EVIDENCE_ROOT / entry_id / form
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = evidence_dir / "evidence.json"
    evas = backend_status(raw, "evas")
    spectre = backend_status(raw, "spectre")
    certified = result_is_certified(row)
    pending_blockers = external_pending_blockers(raw)
    failures: list[str] = []
    if not certified:
        if not pending_blockers:
            failures.append(f"rerun raw status is {raw_result_status(row)}")
    if evas != "pass":
        failures.append("EVAS rerun did not pass")
    if spectre == "fail":
        failures.append("Spectre rerun did not pass")

    evas_result = write_backend_result(
        evidence_dir=evidence_dir,
        row=row,
        backend="evas",
        status=evas,
        evidence_path=evidence_path,
    )
    spectre_result = write_backend_result(
        evidence_dir=evidence_dir,
        row=row,
        backend="spectre",
        status=spectre,
        evidence_path=evidence_path,
    )
    artifacts = [
        str(row.get("staged_task_dir", "")),
        str(row.get("result_root", "")),
        evas_result,
        spectre_result,
        *task.get("gold", []),
    ]
    evidence = {
        "release_entry_id": entry_id,
        "task_id": f"{entry_id}:{form}",
        "source_task_id": raw.get("task_id", row.get("source_task_id")),
        "task_form": form,
        "taxonomy": {
            "level": entry["level"],
            "category": entry["category"],
            "base_function": entry["base_function"],
        },
        "static": task.get("static_status", "pending"),
        "evas": evas,
        "spectre": spectre,
        "verdict": "certified" if certified and task.get("static_status") == "pass" else "not_certified",
        "artifacts": artifacts,
        "historical_evidence": {
            "evas_result": "",
            "spectre_result": "",
            "source": "fresh release dual rerun",
            "source_equivalence_source": "release_rerun_staging_bundle",
            "simulator_rerun": True,
        },
        "release_rerun": {
            "summary": rel(summary_path) if summary_path.is_relative_to(ROOT) else str(summary_path),
            "staged_task_dir": row.get("staged_task_dir", ""),
            "result_root": row.get("result_root", ""),
            "raw_status": raw_result_status(row),
            "expected_result_met": row.get("expected_result_met"),
            "parity": raw.get("parity", {}),
        },
        "source_equivalence": {
            "pass": True,
            "source": "release_rerun_staging_bundle",
            "failures": [],
            "release_gold": task.get("gold", []),
        },
        "failures": failures,
        "pending_blockers": [] if certified else (pending_blockers or failures),
        "notes": (
            "EVAS/Spectre evidence imported from fresh release rerun staged from release gold assets."
            if not pending_blockers
            else "EVAS evidence imported from current release gold; Spectre certification remains pending on external license checkout."
        ),
    }
    write_json(evidence_path, evidence)

    task["evas_status"] = evas
    task["spectre_status"] = spectre
    task["dual_evidence"] = rel(evidence_path)
    task["evas_result"] = evas_result
    task["spectre_result"] = spectre_result
    task["simulator_rerun_source"] = "release_rerun_staging_bundle"
    update_release_task_manifest(task=task, evas=evas, spectre=spectre, evidence_path=evidence_path)

    task_status = "pass" if certified else ("pending" if pending_blockers and not failures else "fail")
    return {
        "entry_id": entry_id,
        "form": form,
        "source_task_id": raw.get("task_id", row.get("source_task_id")),
        "status": task_status,
        "backend_status": {
            "evas": evas,
            "spectre": spectre,
        },
        "failure_count": len(failures),
        "source_equivalence_failure_count": 0,
        "blocker_count": 0 if certified else len(pending_blockers or failures),
        "failures": failures,
        "pending_blockers": [] if certified else (pending_blockers or failures),
        "evidence": rel(evidence_path),
        "simulator_rerun": True,
    }


def recompute_dual_report(current: dict[str, object], updates: dict[tuple[str, str], dict[str, object]]) -> dict[str, object]:
    entries = read_entries()
    active_keys = {
        (entry_id, str(task.get("form")))
        for entry_id, (_, entry) in entries.items()
        for task in entry.get("release_tasks", [])
        if isinstance(task, dict)
    }
    task_reports: list[dict[str, object]] = []
    for report in current.get("task_reports", []):
        if not isinstance(report, dict):
            continue
        key = (str(report["entry_id"]), str(report["form"]))
        if key not in active_keys:
            continue
        task_reports.append(updates.get(key, report))
    for key, report in sorted(updates.items()):
        if key in active_keys and key not in {(str(row["entry_id"]), str(row["form"])) for row in task_reports}:
            task_reports.append(report)

    per_entry: dict[str, list[dict[str, object]]] = defaultdict(list)
    for report in task_reports:
        per_entry[str(report["entry_id"])].append(report)

    entry_reports: list[dict[str, object]] = []
    for entry_id, (_, entry) in sorted(entries.items()):
        reports = per_entry.get(entry_id, [])
        dual_pass = bool(reports) and all(report["status"] == "pass" for report in reports)
        dual_fail = any(report["status"] == "fail" for report in reports)
        dual_status = "pass" if dual_pass else ("fail" if dual_fail else "pending")
        missing_forms = entry.get("missing_forms", [])
        blockers = entry.get("release_blockers", [])
        effective_blockers = entry_release_blockers(
            blockers=blockers,
            task_reports=reports,
        )
        fully_certified = (
            dual_pass
            and entry.get("certification", {}).get("static") == "pass"
            and not missing_forms
            and not effective_blockers
        )
        entry_reports.append(
            {
                "entry_id": entry_id,
                "release_task_count": len(reports),
                "dual": dual_status,
                "fully_certified": fully_certified,
                "missing_forms": missing_forms,
                "release_blockers": effective_blockers,
            }
        )

    issue_count = sum(int(report.get("failure_count", 0)) for report in task_reports)
    source_equivalence_failure_count = sum(
        int(report.get("source_equivalence_failure_count", 0)) for report in task_reports
    )
    pending_count = sum(1 for report in task_reports if report.get("status") == "pending")
    failed_count = sum(1 for report in task_reports if report.get("status") == "fail")
    mismatch_count = sum(
        1
        for report in task_reports
        if report.get("backend_status", {}).get("evas") == "pass"
        and report.get("backend_status", {}).get("spectre") == "fail"
    )
    merged = dict(current)
    merged.update(
        {
            "date": date.today().isoformat(),
            "status": "pass" if issue_count == 0 and pending_count == 0 else ("fail" if failed_count else "partial"),
            "source": "historical main120 import plus fresh release dual rerun",
            "simulator_rerun": True,
            "dual_certified_release_task_count": sum(1 for report in task_reports if report.get("status") == "pass"),
            "dual_failed_release_task_count": failed_count,
            "dual_pending_release_task_count": pending_count,
            "dual_pass_materialized_entry_count": sum(1 for report in entry_reports if report["dual"] == "pass"),
            "dual_pending_materialized_entry_count": sum(1 for report in entry_reports if report["dual"] == "pending"),
            "dual_failed_materialized_entry_count": sum(1 for report in entry_reports if report["dual"] == "fail"),
            "fully_certified_entry_count": sum(1 for report in entry_reports if report["fully_certified"]),
            "entry_count": len(entry_reports),
            "issue_count": issue_count,
            "source_equivalence_failure_count": source_equivalence_failure_count,
            "source_equivalence_blocked_release_task_count": sum(
                1
                for report in task_reports
                if report.get("status") == "pending"
                and int(report.get("source_equivalence_failure_count", 0)) > 0
            ),
            "evas_pass_spectre_fail_count": mismatch_count,
            "task_reports": task_reports,
            "entry_reports": entry_reports,
            "notes": [
                "Historical imported evidence is retained for already certified forms.",
                "Fresh release dual rerun results replace pending forms when the primary gold/fixed bundle passes.",
                "Bugfix buggy companion bundles are not counted in the scored release denominator.",
            ],
        }
    )
    return merged


def entry_backend_certification(task_reports: list[dict[str, object]], backend: str) -> str:
    if not task_reports:
        return "pending"
    statuses = []
    for report in task_reports:
        backend_status = report.get("backend_status", {})
        if not isinstance(backend_status, dict):
            statuses.append("pending")
            continue
        statuses.append(str(backend_status.get(backend, "pending")))
    if all(status == "pass" for status in statuses):
        return "pass"
    if any(status == "fail" for status in statuses):
        return "fail"
    return "pending"


def entry_release_blockers(
    *,
    blockers: object,
    task_reports: list[dict[str, object]],
) -> list[object] | object:
    if not isinstance(blockers, list):
        return blockers
    evas_cert = entry_backend_certification(task_reports, "evas")
    spectre_cert = entry_backend_certification(task_reports, "spectre")
    retained = [
        blocker
        for blocker in blockers
        if blocker not in {"evas_certification", "spectre_certification"}
        and not (blocker in DUAL_REFRESH_BLOCKERS and evas_cert == "pass" and spectre_cert == "pass")
    ]
    if evas_cert != "pass" and "evas_certification" not in retained:
        retained.append("evas_certification")
    if spectre_cert != "pass" and "spectre_certification" not in retained:
        retained.append("spectre_certification")
    return retained


def write_dual_markdown(report: dict[str, object]) -> None:
    task_reports = [item for item in report.get("task_reports", []) if isinstance(item, dict)]
    entry_reports = [item for item in report.get("entry_reports", []) if isinstance(item, dict)]
    pending_or_failed = [
        item
        for item in task_reports
        if item.get("status") != "pass" or item.get("pending_blockers") or item.get("failures")
    ]
    incomplete_entries = [item for item in entry_reports if not item.get("fully_certified")]

    lines = [
        "# vaBench Release Dual Certification",
        "",
        f"Date: {report['date']}",
        "",
        "This report is generated from historical imported evidence plus fresh",
        "release EVAS/Spectre rerun results when available.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| source | `{report.get('source', '')}` |",
        f"| simulator rerun | `{report.get('simulator_rerun', False)}` |",
        f"| release entries | {report.get('entry_count', 0)} |",
        f"| dual-certified release forms | {report.get('dual_certified_release_task_count', 0)} |",
        f"| dual-failed release forms | {report.get('dual_failed_release_task_count', 0)} |",
        f"| dual-pending release forms | {report.get('dual_pending_release_task_count', 0)} |",
        f"| dual-pass materialized entries | {report.get('dual_pass_materialized_entry_count', 0)} |",
        f"| dual-pending materialized entries | {report.get('dual_pending_materialized_entry_count', 0)} |",
        f"| dual-failed materialized entries | {report.get('dual_failed_materialized_entry_count', 0)} |",
        f"| fully certified entries | {report.get('fully_certified_entry_count', 0)} |",
        f"| source-equivalence failures | {report.get('source_equivalence_failure_count', 0)} |",
        f"| source-equivalence blocked forms | {report.get('source_equivalence_blocked_release_task_count', 0)} |",
        f"| EVAS PASS / Spectre FAIL count | {report.get('evas_pass_spectre_fail_count', 0)} |",
        "",
        "## Pending Or Failed Forms",
        "",
        "| Entry | Form | Status | EVAS | Spectre | Blockers | Evidence |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    if pending_or_failed:
        for item in pending_or_failed:
            backend = item.get("backend_status", {})
            if not isinstance(backend, dict):
                backend = {}
            blockers = item.get("pending_blockers") or item.get("failures") or []
            blocker_text = ", ".join(str(blocker) for blocker in blockers) if isinstance(blockers, list) else blockers
            lines.append(
                "| `{entry}` | `{form}` | `{status}` | `{evas}` | `{spectre}` | {blockers} | `{evidence}` |".format(
                    entry=item.get("entry_id", ""),
                    form=item.get("form", ""),
                    status=item.get("status", ""),
                    evas=backend.get("evas", ""),
                    spectre=backend.get("spectre", ""),
                    blockers=blocker_text,
                    evidence=item.get("evidence", ""),
                )
            )
    else:
        lines.append("| none | none | none | none | none | none | none |")

    lines.extend(
        [
            "",
            "## Incomplete Entries",
            "",
            "| Entry | Dual | Missing forms | Release blockers |",
            "| --- | --- | --- | --- |",
        ]
    )
    if incomplete_entries:
        for item in incomplete_entries:
            missing_forms = item.get("missing_forms", [])
            release_blockers = item.get("release_blockers", [])
            missing_text = (
                ", ".join(str(value) for value in missing_forms) if isinstance(missing_forms, list) else missing_forms
            )
            blocker_text = (
                ", ".join(str(value) for value in release_blockers)
                if isinstance(release_blockers, list)
                else release_blockers
            )
            lines.append(
                "| `{entry}` | `{dual}` | {missing} | {blockers} |".format(
                    entry=item.get("entry_id", ""),
                    dual=item.get("dual", ""),
                    missing=missing_text,
                    blockers=blocker_text,
                )
            )
    else:
        lines.append("| none | none | none | none |")

    lines.extend(["", "## Notes", ""])
    for note in report.get("notes", []):
        lines.append(f"- {note}")
    DUAL_REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_entry_certifications(updates: dict[tuple[str, str], dict[str, object]], merged_report: dict[str, object]) -> None:
    reports_by_entry: dict[str, list[dict[str, object]]] = defaultdict(list)
    reports_by_key: dict[tuple[str, str], dict[str, object]] = {}
    for report in merged_report.get("task_reports", []):
        if isinstance(report, dict):
            reports_by_entry[str(report["entry_id"])].append(report)
            reports_by_key[(str(report["entry_id"]), str(report["form"]))] = report

    for entry_path, entry in read_entries().values():
        entry_id = str(entry["release_entry_id"])
        changed = False
        for task in entry.get("release_tasks", []):
            if not isinstance(task, dict):
                continue
            key = (entry_id, str(task.get("form")))
            if key in reports_by_key:
                task_report = reports_by_key[key]
                task["evas_status"] = task_report["backend_status"]["evas"]
                task["spectre_status"] = task_report["backend_status"]["spectre"]
                task["dual_evidence"] = task_report["evidence"]
                changed = True

        task_reports = reports_by_entry.get(entry_id, [])
        dual_pass = bool(task_reports) and all(report["status"] == "pass" for report in task_reports)
        evas_cert = entry_backend_certification(task_reports, "evas")
        spectre_cert = entry_backend_certification(task_reports, "spectre")
        certification = entry.setdefault("certification", {})
        if isinstance(certification, dict):
            certification["evas"] = evas_cert
            certification["spectre"] = spectre_cert
            certification["evidence"] = rel(DUAL_REPORT_JSON)
            changed = True
        blockers = entry.get("release_blockers", [])
        if isinstance(blockers, list):
            if dual_pass:
                entry["release_blockers"] = [blocker for blocker in blockers if blocker not in DUAL_REFRESH_BLOCKERS]
            else:
                entry["release_blockers"] = entry_release_blockers(
                    blockers=blockers,
                    task_reports=task_reports,
                )
            changed = True
        if changed:
            write_json(entry_path, entry)


def build_import_report(summary_path: Path, *, write: bool) -> dict[str, object]:
    summary = read_json(summary_path)
    current = read_json(DUAL_REPORT_JSON)
    queue_count = current_queue_count()
    explicit_primary_rows = primary_result_rows(summary) if summary else []
    current_dual_complete = (
        current.get("status") == "pass"
        and int(current.get("dual_pending_release_task_count", 0) or 0) == 0
        and int(current.get("dual_failed_release_task_count", 0) or 0) == 0
        and int(current.get("evas_pass_spectre_fail_count", 0) or 0) == 0
        and current.get("simulator_rerun") is True
    )
    if queue_count == 0 and current_dual_complete and not explicit_primary_rows:
        merged = recompute_dual_report(current, {})
        if write:
            write_json(DUAL_REPORT_JSON, merged)
            write_dual_markdown(merged)
            update_entry_certifications({}, merged)
        tasks_total = summary_task_count(summary) if summary else 0
        if tasks_total is None:
            tasks_total = 0
        return {
            "date": date.today().isoformat(),
            "status": "imported",
            "reason": "No current dual rerun queue remains; dual_certification.json already reflects imported fresh rerun evidence.",
            "summary": rel(summary_path) if summary_path.is_relative_to(ROOT) else str(summary_path),
            "tasks_total": tasks_total,
            "current_queue_count": queue_count,
            "summary_tasks_total": tasks_total,
            "stale_summary": False,
            "imported_primary_result_count": 0,
            "skipped_result_count": 0,
            "imported_pass_count": 0,
            "imported_fail_count": 0,
            "merged_dual_certified_release_task_count": merged.get("dual_certified_release_task_count", 0),
            "merged_dual_pending_release_task_count": merged.get("dual_pending_release_task_count", 0),
            "merged_dual_failed_release_task_count": merged.get("dual_failed_release_task_count", 0),
            "merged_evas_pass_spectre_fail_count": merged.get("evas_pass_spectre_fail_count", 0),
            "imported_rows": [],
            "skipped_rows": [],
            "notes": [
                "The import step is idempotent once the current rerun queue is empty and dual certification is complete.",
                "Rerun timing and model-baseline claims remain separate gates.",
            ],
        }
    if not summary:
        return {
            "date": date.today().isoformat(),
            "status": "missing",
            "reason": "No dual rerun summary exists yet.",
            "summary": rel(summary_path) if summary_path.exists() else str(summary_path),
            "tasks_total": 0,
            "current_queue_count": queue_count,
            "summary_tasks_total": 0,
            "stale_summary": False,
            "imported_primary_result_count": 0,
            "skipped_result_count": 0,
            "imported_pass_count": 0,
            "imported_fail_count": 0,
            "notes": ["No dual rerun summary exists yet."],
        }
    tasks_total = summary_task_count(summary)
    primary_count = len(primary_result_rows(summary))
    stale_reason = stale_summary_reason(
        summary_tasks_total=tasks_total,
        queue_count=queue_count,
        primary_result_count=primary_count,
        original_reason=summary.get("reason", ""),
    )
    if stale_reason and not getattr(build_import_report, "allow_partial_stale", False):
        return {
            "date": date.today().isoformat(),
            "status": "blocked",
            "reason": stale_reason,
            "summary": rel(summary_path) if summary_path.is_relative_to(ROOT) else str(summary_path),
            "tasks_total": tasks_total,
            "current_queue_count": queue_count,
            "summary_tasks_total": tasks_total,
            "stale_summary": True,
            "imported_primary_result_count": 0,
            "skipped_result_count": 0,
            "imported_pass_count": 0,
            "imported_fail_count": 0,
            "notes": [
                "Fresh dual rerun results are not imported when summary task count is stale.",
                "Current dual_certification.json remains based on historical import plus pending rerun blockers.",
            ],
        }
    if summary.get("status") != "complete":
        return {
            "date": date.today().isoformat(),
            "status": str(summary.get("status", "unknown")),
            "reason": summary.get("reason", ""),
            "summary": rel(summary_path) if summary_path.is_relative_to(ROOT) else str(summary_path),
            "tasks_total": tasks_total,
            "current_queue_count": queue_count,
            "summary_tasks_total": tasks_total,
            "stale_summary": False,
            "imported_primary_result_count": 0,
            "skipped_result_count": 0,
            "imported_pass_count": 0,
            "imported_fail_count": 0,
            "notes": [
                "Fresh dual rerun results are not imported unless the rerun summary status is complete.",
                "Current dual_certification.json remains based on historical import plus pending rerun blockers.",
            ],
        }

    entries = read_entries()
    updates: dict[tuple[str, str], dict[str, object]] = {}
    imported_rows: list[dict[str, object]] = []
    skipped_rows: list[dict[str, object]] = []
    for row in primary_result_rows(summary):
        entry_id = str(row["entry_id"])
        form = str(row["form"])
        if entry_id not in entries:
            skipped_rows.append({"entry_id": entry_id, "form": form, "reason": "unknown release entry"})
            continue
        _, entry = entries[entry_id]
        task = task_by_form(entry, form)
        if task is None:
            skipped_rows.append({"entry_id": entry_id, "form": form, "reason": "release form not found"})
            continue
        task_report = write_task_evidence(entry=entry, task=task, row=row, summary_path=summary_path) if write else {
            "entry_id": entry_id,
            "form": form,
            "status": (
                "pass"
                if result_is_certified(row)
                else (
                    "pending"
                    if isinstance(row.get("raw_result", {}), dict)
                    and external_pending_blockers(row.get("raw_result", {}))
                    else "fail"
                )
            ),
            "backend_status": {
                "evas": backend_status(row.get("raw_result", {}), "evas") if isinstance(row.get("raw_result", {}), dict) else "fail",
                "spectre": backend_status(row.get("raw_result", {}), "spectre") if isinstance(row.get("raw_result", {}), dict) else "fail",
            },
            "failure_count": (
                0
                if result_is_certified(row)
                or (
                    isinstance(row.get("raw_result", {}), dict)
                    and external_pending_blockers(row.get("raw_result", {}))
                )
                else 1
            ),
            "source_equivalence_failure_count": 0,
            "blocker_count": 0 if result_is_certified(row) else 1,
            "failures": (
                []
                if result_is_certified(row)
                or (
                    isinstance(row.get("raw_result", {}), dict)
                    and external_pending_blockers(row.get("raw_result", {}))
                )
                else [f"rerun raw status is {raw_result_status(row)}"]
            ),
            "pending_blockers": (
                []
                if result_is_certified(row)
                else (
                    external_pending_blockers(row.get("raw_result", {}))
                    if isinstance(row.get("raw_result", {}), dict)
                    and external_pending_blockers(row.get("raw_result", {}))
                    else [f"rerun raw status is {raw_result_status(row)}"]
                )
            ),
            "evidence": "",
            "simulator_rerun": True,
        }
        updates[(entry_id, form)] = task_report
        imported_rows.append(task_report)

    merged = recompute_dual_report(current, updates)
    if write:
        write_json(DUAL_REPORT_JSON, merged)
        write_dual_markdown(merged)
        update_entry_certifications(updates, merged)

    imported_fail_count = sum(1 for row in imported_rows if row["status"] == "fail")
    imported_pending_count = sum(1 for row in imported_rows if row["status"] == "pending")
    return {
        "date": date.today().isoformat(),
        "status": (
            "partial_imported"
            if stale_reason and imported_fail_count == 0
            else ("imported" if imported_fail_count == 0 else "imported_with_failures")
        ),
        "reason": (
            "Fresh dual rerun imported with failing primary rows; release certification remains blocked."
            if imported_fail_count
            else (
                "Fresh dual rerun imported with external pending blockers; release certification remains pending."
                if imported_pending_count
                else (
                "Stale-count dual rerun summary was partially imported by exact entry/form match; unmatched rows remain skipped and missing rows remain pending."
                if stale_reason
                else "Fresh dual rerun imported; all primary rows passed EVAS/Spectre certification."
                )
            )
        ),
        "summary": rel(summary_path) if summary_path.is_relative_to(ROOT) else str(summary_path),
        "tasks_total": tasks_total,
        "current_queue_count": queue_count,
        "summary_tasks_total": tasks_total,
        "stale_summary": bool(stale_reason),
        "stale_reason": stale_reason or "",
        "imported_primary_result_count": len(imported_rows),
        "skipped_result_count": len(skipped_rows),
        "imported_pass_count": sum(1 for row in imported_rows if row["status"] == "pass"),
        "imported_pending_count": imported_pending_count,
        "imported_fail_count": imported_fail_count,
        "merged_dual_certified_release_task_count": merged["dual_certified_release_task_count"],
        "merged_dual_pending_release_task_count": merged["dual_pending_release_task_count"],
        "merged_dual_failed_release_task_count": merged["dual_failed_release_task_count"],
        "merged_evas_pass_spectre_fail_count": merged["evas_pass_spectre_fail_count"],
        "imported_rows": imported_rows,
        "skipped_rows": skipped_rows,
        "notes": [
            "Only primary gold/fixed pass bundles are imported into the release denominator.",
            "Bugfix buggy companion bundles remain separate badcase evidence and are not scored here.",
            "Partial stale-count import is conservative: it imports only exact current release entry/form matches.",
        ],
    }


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Dual Rerun Import",
        "",
        f"Date: {report['date']}",
        "",
        "This report records whether fresh release EVAS/Spectre rerun results",
        "were imported into release evidence. It does not import blocked, dry-run,",
        "or still-running summaries.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| stale summary | `{report.get('stale_summary', False)}` |",
        f"| summary tasks total | {report.get('summary_tasks_total', '')} |",
        f"| current queue count | {report.get('current_queue_count', '')} |",
        f"| imported primary results | {report.get('imported_primary_result_count', 0)} |",
        f"| skipped results | {report.get('skipped_result_count', 0)} |",
        f"| imported pass | {report.get('imported_pass_count', 0)} |",
        f"| imported pending | {report.get('imported_pending_count', 0)} |",
        f"| imported fail | {report.get('imported_fail_count', 0)} |",
    ]
    if report.get("reason"):
        lines.extend(["", f"Reason: {report['reason']}"])
    lines.extend(["", "## Notes", ""])
    for note in report.get("notes", []):
        lines.append(f"- {note}")
    IMPORT_REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import fresh vaBench release EVAS/Spectre rerun results.")
    parser.add_argument("--summary", default=str(DEFAULT_SUMMARY_JSON), help="Rerun summary JSON.")
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Build the import report without writing release evidence or merged dual certification.",
    )
    parser.add_argument(
        "--allow-partial-stale",
        action="store_true",
        help=(
            "When summary task count differs from the current queue, import only exact current "
            "release entry/form matches and leave all nonmatching or missing rows untouched."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    summary_path = Path(args.summary)
    if not summary_path.is_absolute():
        summary_path = ROOT / summary_path
    build_import_report.allow_partial_stale = bool(args.allow_partial_stale)  # type: ignore[attr-defined]
    report = build_import_report(summary_path, write=not args.preview)
    write_json(IMPORT_REPORT_JSON, report)
    write_markdown(report)
    print(
        "imported dual rerun results: status={status}; imported={count}".format(
            status=report["status"],
            count=report.get("imported_primary_result_count", 0),
        )
    )


if __name__ == "__main__":
    main()
