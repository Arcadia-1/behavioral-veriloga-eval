#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
EVIDENCE_ROOT = PACKAGE_ROOT / "evidence" / "dual"
REPORT_JSON = PACKAGE_ROOT / "reports" / "dual_certification.json"
REPORT_MD = PACKAGE_ROOT / "reports" / "dual_certification.md"
EVAS_ROOT = ROOT / "results" / "vabench-main-v1-main120-gold-evas-2026-05-08"
SPECTRE_ROOT = ROOT / "results" / "vabench-main-v1-main120-gold-spectre-jin-2026-05-08"
D004_DUAL_SUMMARIES = [
    ROOT / "results" / "d004-b1-batch-dual-fixed-2026-05-15" / "summary.json",
    ROOT / "results" / "d004-batch2-dual-2026-05-14" / "summary.json",
    ROOT / "results" / "d004-batch3-dual-2026-05-14" / "summary.json",
    ROOT / "results" / "d004-pilot-dual-2026-05-14" / "summary.json",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_entries() -> list[tuple[Path, dict[str, object]]]:
    entries: list[tuple[Path, dict[str, object]]] = []
    for path in sorted(TASKS_ROOT.glob("CT*/vbr1_*/release_entry.json")):
        entries.append((path, json.loads(path.read_text(encoding="utf-8"))))
    return entries


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_veriloga(text: str) -> str:
    """Return a token stream that ignores formatting but preserves source tokens."""
    tokens: list[str] = []
    index = 0
    length = len(text)
    while index < length:
        char = text[index]
        if char.isspace():
            index += 1
            continue
        if char == "/" and index + 1 < length and text[index + 1] == "/":
            index += 2
            while index < length and text[index] not in "\r\n":
                index += 1
            continue
        if char == "/" and index + 1 < length and text[index + 1] == "*":
            index += 2
            while index + 1 < length and not (text[index] == "*" and text[index + 1] == "/"):
                index += 1
            index = min(index + 2, length)
            continue
        if char == '"':
            start = index
            index += 1
            while index < length:
                if text[index] == "\\":
                    index += 2
                    continue
                if text[index] == '"':
                    index += 1
                    break
                index += 1
            tokens.append(text[start:index])
            continue
        if char.isalpha() or char in "_`$":
            start = index
            index += 1
            while index < length and (text[index].isalnum() or text[index] in "_`$"):
                index += 1
            tokens.append(text[start:index])
            continue
        if char.isdigit() or (char == "." and index + 1 < length and text[index + 1].isdigit()):
            start = index
            index += 1
            while index < length and (
                text[index].isalnum() or text[index] in "._+-"
            ):
                index += 1
            tokens.append(text[start:index])
            continue
        tokens.append(char)
        index += 1
    return "\n".join(tokens) + "\n"


def normalize_scs(text: str) -> str:
    text = re.sub(r'ahdl_include\s+"[^"]+"', 'ahdl_include "__AHDL__.va"', text)
    return "\n".join(line.rstrip() for line in text.splitlines()).strip() + "\n"


def staged_dir(result: dict[str, object]) -> Path:
    artifacts = result.get("artifacts", {})
    if not isinstance(artifacts, dict) or "staged_dir" not in artifacts:
        raise RuntimeError(f"result for {result.get('task_id')} has no staged_dir artifact")
    path = Path(str(artifacts["staged_dir"]))
    if not path.is_absolute():
        path = ROOT / path
    if not path.is_dir():
        raise RuntimeError(f"staged_dir does not exist: {path}")
    return path


def file_hash_sets(paths: list[Path]) -> dict[str, set[str]]:
    raw_va: set[str] = set()
    normalized_scs: set[str] = set()
    for path in paths:
        if path.suffix == ".va":
            raw_va.add(sha256_text(normalize_veriloga(path.read_text(encoding="utf-8", errors="ignore"))))
        elif path.suffix == ".scs":
            normalized_scs.add(sha256_text(normalize_scs(path.read_text(encoding="utf-8", errors="ignore"))))
    return {"va": raw_va, "scs": normalized_scs}


def release_gold_paths(task: dict[str, object]) -> list[Path]:
    return [ROOT / str(path) for path in task.get("gold", [])]


def staged_source_paths(result: dict[str, object]) -> list[Path]:
    directory = staged_dir(result)
    return sorted(path for path in directory.iterdir() if path.suffix in {".va", ".scs"})


def source_equivalence(evas_result: dict[str, object], spectre_result: dict[str, object], task: dict[str, object]) -> dict[str, object]:
    release_paths = release_gold_paths(task)
    release_hashes = file_hash_sets(release_paths)
    evas_paths = staged_source_paths(evas_result)
    spectre_paths = staged_source_paths(spectre_result)
    evas_hashes = file_hash_sets(evas_paths)
    spectre_hashes = file_hash_sets(spectre_paths)

    failures: list[str] = []
    for backend, hashes in (("evas", evas_hashes), ("spectre", spectre_hashes)):
        missing_va = sorted(hashes["va"] - release_hashes["va"])
        missing_scs = sorted(hashes["scs"] - release_hashes["scs"])
        if missing_va:
            failures.append(f"{backend} staged Verilog-A token hash not found in release gold")
        if missing_scs:
            failures.append(f"{backend} staged Spectre testbench hash not found in normalized release gold")

    return {
        "pass": not failures,
        "source": "main120_staged_sources",
        "normalization": "Verilog-A token stream; Spectre ahdl_include path plus trailing whitespace",
        "failures": failures,
        "release_gold": [rel(path) for path in release_paths],
        "evas_staged_sources": [rel(path) if path.is_relative_to(ROOT) else str(path) for path in evas_paths],
        "spectre_staged_sources": [rel(path) if path.is_relative_to(ROOT) else str(path) for path in spectre_paths],
        "release_va_hash_count": len(release_hashes["va"]),
        "release_scs_hash_count": len(release_hashes["scs"]),
        "evas_va_hash_count": len(evas_hashes["va"]),
        "evas_scs_hash_count": len(evas_hashes["scs"]),
        "spectre_va_hash_count": len(spectre_hashes["va"]),
        "spectre_scs_hash_count": len(spectre_hashes["scs"]),
    }


def d004_dual_index() -> dict[str, tuple[Path, dict[str, object]]]:
    index: dict[str, tuple[Path, dict[str, object]]] = {}
    for summary_path in D004_DUAL_SUMMARIES:
        if not summary_path.exists():
            continue
        payload = read_json(summary_path)
        results = payload.get("results", [])
        if not isinstance(results, list):
            continue
        for item in results:
            if isinstance(item, dict) and isinstance(item.get("task_id"), str):
                index[str(item["task_id"])] = (summary_path, item)
    return index


D004_INDEX = d004_dual_index()


def d004_status_pass(item: dict[str, object]) -> bool:
    evas = item.get("evas", {})
    spectre = item.get("spectre", {})
    return (
        item.get("status") == "PASS"
        and isinstance(evas, dict)
        and evas.get("status") == "PASS"
        and isinstance(spectre, dict)
        and spectre.get("ok") is True
        and float(spectre.get("behavior_score", 0.0)) >= 1.0
    )


def d004_source_equivalence(source_task_id: str, task: dict[str, object]) -> dict[str, object]:
    if source_task_id not in D004_INDEX:
        return {"pass": False, "source": "d004_fixed_dual", "failures": ["no D004 fixed dual result"]}
    summary_path, item = D004_INDEX[source_task_id]
    if not d004_status_pass(item):
        return {"pass": False, "source": "d004_fixed_dual", "failures": ["D004 fixed dual result is not PASS"]}

    gold_dir_value = item.get("gold_dir")
    if not isinstance(gold_dir_value, str):
        return {"pass": False, "source": "d004_fixed_dual", "failures": ["D004 result has no gold_dir"]}
    gold_dir = Path(gold_dir_value)
    if not gold_dir.is_absolute():
        gold_dir = ROOT / gold_dir
    if not gold_dir.is_dir():
        return {"pass": False, "source": "d004_fixed_dual", "failures": [f"D004 gold_dir does not exist: {gold_dir}"]}

    release_paths = release_gold_paths(task)
    release_hashes = file_hash_sets(release_paths)
    d004_paths = sorted(path for path in gold_dir.iterdir() if path.suffix in {".va", ".scs"})
    d004_hashes = file_hash_sets(d004_paths)
    failures: list[str] = []
    if not d004_hashes["va"] <= release_hashes["va"]:
        failures.append("D004 Verilog-A gold hash not found in release gold")
    if not d004_hashes["scs"] <= release_hashes["scs"]:
        failures.append("D004 Spectre testbench hash not found in normalized release gold")

    spectre_csv = ""
    spectre = item.get("spectre", {})
    if isinstance(spectre, dict) and isinstance(spectre.get("csv_path"), str):
        spectre_csv = spectre["csv_path"]

    return {
        "pass": not failures,
        "source": "d004_fixed_dual",
        "failures": failures,
        "release_gold": [rel(path) for path in release_paths],
        "d004_summary": rel(summary_path),
        "d004_gold_dir": rel(gold_dir) if gold_dir.is_relative_to(ROOT) else str(gold_dir),
        "d004_gold_sources": [rel(path) if path.is_relative_to(ROOT) else str(path) for path in d004_paths],
        "d004_spectre_csv": rel(Path(spectre_csv)) if spectre_csv and Path(spectre_csv).is_relative_to(ROOT) else spectre_csv,
        "release_va_hash_count": len(release_hashes["va"]),
        "release_scs_hash_count": len(release_hashes["scs"]),
        "d004_va_hash_count": len(d004_hashes["va"]),
        "d004_scs_hash_count": len(d004_hashes["scs"]),
        "evidence_artifacts": [
            rel(summary_path),
            *(
                [rel(Path(spectre_csv))]
                if spectre_csv and Path(spectre_csv).is_relative_to(ROOT) and Path(spectre_csv).exists()
                else []
            ),
        ],
    }


def status_pass(result: dict[str, object]) -> bool:
    scores = result.get("scores", {})
    weighted = scores.get("weighted_total") if isinstance(scores, dict) else None
    return result.get("status") == "PASS" and (weighted is None or float(weighted) >= 1.0)


def write_backend_result(
    *,
    path: Path,
    backend: str,
    form: str,
    task_id: str,
    entry_id: str,
    historical_result_path: Path,
    historical_result: dict[str, object],
    evidence_path: Path,
    backend_failures: list[str],
    source_equivalence_failures: list[str],
) -> None:
    backend_pass = not backend_failures and status_pass(historical_result)
    status = "PASS"
    if backend_failures or not status_pass(historical_result):
        status = "FAIL_SIM_CORRECTNESS" if historical_result else "FAIL_INFRA"
    elif source_equivalence_failures:
        status = "FAIL_INFRA"

    result = {
        "task_id": f"{entry_id}:{form}",
        "release_entry_id": entry_id,
        "source_task_id": task_id,
        "backend": backend,
        "status": status,
        "scores": {
            "historical_weighted_total": historical_result.get("scores", {}).get("weighted_total", None),
            "historical_backend_pass": backend_pass,
            "source_equivalence_failure_count": len(source_equivalence_failures),
        },
        "artifacts": [rel(historical_result_path), rel(evidence_path)],
        "notes": [
            "Imported from main120 gold historical result; no simulator rerun was performed in this release step.",
            *backend_failures,
            *source_equivalence_failures,
        ],
    }
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


def write_pending_backend_result(
    *,
    path: Path,
    backend: str,
    form: str,
    task_id: str,
    entry_id: str,
    evidence_path: Path,
    pending_blockers: list[str],
) -> None:
    result = {
        "task_id": f"{entry_id}:{form}",
        "release_entry_id": entry_id,
        "source_task_id": task_id,
        "backend": backend,
        "status": "PENDING",
        "scores": {
            "historical_weighted_total": None,
            "historical_backend_pass": False,
            "source_equivalence_failure_count": 0,
        },
        "artifacts": [rel(evidence_path)],
        "notes": pending_blockers,
    }
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


def certify_task(entry: dict[str, object], task: dict[str, object]) -> dict[str, object]:
    entry_id = str(entry["release_entry_id"])
    form = str(task["form"])
    meta = read_json(ROOT / str(task["meta"]))
    release_source_task_id = str(meta.get("task_id") or meta.get("id"))
    source_task_id = str(meta.get("source_main120_id") or release_source_task_id)
    historical_dual_expected = task.get("historical_dual_expected", True) is not False
    evidence_dir = EVIDENCE_ROOT / entry_id / form
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = evidence_dir / "evidence.json"
    evas_result_path = evidence_dir / "evas_result.json"
    spectre_result_path = evidence_dir / "spectre_result.json"

    if not historical_dual_expected:
        pending_blockers = ["no imported dual evidence; EVAS/Spectre rerun required for this selected release task"]
        equivalence = {
            "pass": False,
            "source": "pending_simulator_rerun",
            "failures": [],
            "release_gold": task.get("gold", []),
        }
        evidence = {
            "release_entry_id": entry_id,
            "task_id": f"{entry_id}:{form}",
            "source_task_id": source_task_id,
            "release_source_task_id": release_source_task_id,
            "task_form": form,
            "taxonomy": {
                "level": entry["level"],
                "category": entry["category"],
                "base_function": entry["base_function"],
            },
            "static": task.get("static_status", "pending"),
            "evas": "pending",
            "spectre": "pending",
            "verdict": "not_certified",
            "artifacts": [rel(evidence_path), *task.get("gold", [])],
            "historical_evidence": {
                "evas_result": "",
                "spectre_result": "",
                "source": "none; selected release task awaits EVAS/Spectre rerun",
                "source_equivalence_source": "pending_simulator_rerun",
                "simulator_rerun": False,
            },
            "source_equivalence": equivalence,
            "failures": [],
            "pending_blockers": pending_blockers,
            "notes": "Selected release task was materialized from source assets but has no imported historical dual evidence.",
        }
        evidence_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
        write_pending_backend_result(
            path=evas_result_path,
            backend="evas",
            form=form,
            task_id=source_task_id,
            entry_id=entry_id,
            evidence_path=evidence_path,
            pending_blockers=pending_blockers,
        )
        write_pending_backend_result(
            path=spectre_result_path,
            backend="spectre",
            form=form,
            task_id=source_task_id,
            entry_id=entry_id,
            evidence_path=evidence_path,
            pending_blockers=pending_blockers,
        )
        task["evas_status"] = "pending"
        task["spectre_status"] = "pending"
        task["dual_evidence"] = rel(evidence_path)
        task["evas_result"] = rel(evas_result_path)
        task["spectre_result"] = rel(spectre_result_path)
        task["release_source_task_id"] = release_source_task_id
        task["historical_source_task_id"] = source_task_id

        return {
            "entry_id": entry_id,
            "form": form,
            "source_task_id": source_task_id,
            "release_source_task_id": release_source_task_id,
            "status": "pending",
            "backend_status": {
                "evas": "pending",
                "spectre": "pending",
            },
            "failure_count": 0,
            "source_equivalence_failure_count": 0,
            "blocker_count": len(pending_blockers),
            "failures": [],
            "pending_blockers": pending_blockers,
            "evidence": rel(evidence_path),
        }

    evas_path = EVAS_ROOT / source_task_id / "evas_result.json"
    spectre_path = SPECTRE_ROOT / source_task_id / "spectre_result.json"
    infra_failures: list[str] = []
    simulator_failures: list[str] = []

    if not evas_path.exists():
        infra_failures.append(f"missing EVAS historical result: {rel(evas_path)}")
        evas_result: dict[str, object] = {}
    else:
        evas_result = read_json(evas_path)
    if not spectre_path.exists():
        infra_failures.append(f"missing Spectre historical result: {rel(spectre_path)}")
        spectre_result: dict[str, object] = {}
    else:
        spectre_result = read_json(spectre_path)

    if evas_result and evas_result.get("task_id") != source_task_id:
        infra_failures.append("EVAS result task_id mismatch")
    if spectre_result and spectre_result.get("task_id") != source_task_id:
        infra_failures.append("Spectre result task_id mismatch")
    if evas_result and not status_pass(evas_result):
        simulator_failures.append(f"EVAS historical status is {evas_result.get('status')}")
    if spectre_result and not status_pass(spectre_result):
        simulator_failures.append(f"Spectre historical status is {spectre_result.get('status')}")

    equivalence: dict[str, object] = {"pass": False, "failures": ["not_checked"]}
    source_equivalence_failures: list[str] = []
    if evas_result and spectre_result:
        try:
            equivalence = source_equivalence(evas_result, spectre_result, task)
            source_equivalence_failures = [str(failure) for failure in equivalence["failures"]]
        except RuntimeError as exc:
            equivalence = {"pass": False, "failures": [str(exc)]}
            source_equivalence_failures = [str(exc)]
        if source_equivalence_failures and form == "bugfix":
            fallback_equivalence = d004_source_equivalence(source_task_id, task)
            if fallback_equivalence["pass"]:
                equivalence = fallback_equivalence
                source_equivalence_failures = []

    hard_failures = infra_failures + simulator_failures
    if hard_failures:
        status = "fail"
        evidence_backend_status = {"evas": "fail", "spectre": "fail"}
    elif source_equivalence_failures:
        status = "pending"
        evidence_backend_status = {"evas": "pending", "spectre": "pending"}
    else:
        status = "pass"
        evidence_backend_status = {"evas": "pass", "spectre": "pass"}

    evas_backend_status = "pass" if evas_result and status_pass(evas_result) else "fail"
    spectre_backend_status = "pass" if spectre_result and status_pass(spectre_result) else "fail"
    evidence = {
        "release_entry_id": entry_id,
        "task_id": f"{entry_id}:{form}",
            "source_task_id": source_task_id,
            "release_source_task_id": release_source_task_id,
        "task_form": form,
        "taxonomy": {
            "level": entry["level"],
            "category": entry["category"],
            "base_function": entry["base_function"],
        },
        "static": task.get("static_status", "pending"),
        "evas": evidence_backend_status["evas"],
        "spectre": evidence_backend_status["spectre"],
        "verdict": "certified" if status == "pass" and task.get("static_status") == "pass" else "not_certified",
        "artifacts": [
            rel(evas_path),
            rel(spectre_path),
            rel(evas_result_path),
            rel(spectre_result_path),
            *task.get("gold", []),
            *equivalence.get("evidence_artifacts", []),
        ],
        "historical_evidence": {
            "evas_result": rel(evas_path),
            "spectre_result": rel(spectre_path),
            "source": "main120 gold dual evidence from 2026-05-08",
            "source_equivalence_source": equivalence.get("source", "main120_staged_sources"),
            "simulator_rerun": False,
        },
        "source_equivalence": equivalence,
        "failures": hard_failures,
        "pending_blockers": source_equivalence_failures,
        "notes": "EVAS/Spectre evidence imported from historical main120 gold run and linked to release gold by source hash equivalence.",
    }
    evidence_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    write_backend_result(
        path=evas_result_path,
        backend="evas",
        form=form,
        task_id=source_task_id,
        entry_id=entry_id,
        historical_result_path=evas_path,
        historical_result=evas_result,
        evidence_path=evidence_path,
        backend_failures=[
            failure for failure in hard_failures if "EVAS" in failure or not failure.startswith("Spectre")
        ],
        source_equivalence_failures=source_equivalence_failures,
    )
    write_backend_result(
        path=spectre_result_path,
        backend="spectre",
        form=form,
        task_id=source_task_id,
        entry_id=entry_id,
        historical_result_path=spectre_path,
        historical_result=spectre_result,
        evidence_path=evidence_path,
        backend_failures=[
            failure for failure in hard_failures if "Spectre" in failure or not failure.startswith("EVAS")
        ],
        source_equivalence_failures=source_equivalence_failures,
    )

    task["evas_status"] = evidence_backend_status["evas"]
    task["spectre_status"] = evidence_backend_status["spectre"]
    task["dual_evidence"] = rel(evidence_path)
    task["evas_result"] = rel(evas_result_path)
    task["spectre_result"] = rel(spectre_result_path)
    task["release_source_task_id"] = release_source_task_id
    task["historical_source_task_id"] = source_task_id

    return {
        "entry_id": entry_id,
        "form": form,
        "source_task_id": source_task_id,
        "release_source_task_id": release_source_task_id,
        "status": status,
        "backend_status": {
            "evas": evas_backend_status,
            "spectre": spectre_backend_status,
        },
        "failure_count": len(hard_failures),
        "source_equivalence_failure_count": len(source_equivalence_failures),
        "blocker_count": len(hard_failures) + len(source_equivalence_failures),
        "failures": hard_failures,
        "pending_blockers": source_equivalence_failures,
        "evidence": rel(evidence_path),
    }


def update_entry(path: Path, entry: dict[str, object], task_reports: list[dict[str, object]]) -> None:
    dual_pass = bool(task_reports) and all(report["status"] == "pass" for report in task_reports)
    dual_fail = any(report["status"] == "fail" for report in task_reports)
    certification = entry.setdefault("certification", {})
    if isinstance(certification, dict):
        certification["evas"] = "pass" if dual_pass else ("fail" if dual_fail else "pending")
        certification["spectre"] = "pass" if dual_pass else ("fail" if dual_fail else "pending")
        certification["evidence"] = rel(REPORT_JSON)
    blockers = entry.get("release_blockers", [])
    if isinstance(blockers, list):
        if dual_pass:
            entry["release_blockers"] = [
                blocker for blocker in blockers if blocker not in {"evas_certification", "spectre_certification"}
            ]
        else:
            retained = list(blockers)
            for blocker in ("evas_certification", "spectre_certification"):
                if blocker not in retained:
                    retained.append(blocker)
            entry["release_blockers"] = retained
    path.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")


def build_report() -> dict[str, object]:
    task_reports: list[dict[str, object]] = []
    entry_reports: list[dict[str, object]] = []
    for path, entry in read_entries():
        per_entry: list[dict[str, object]] = []
        for task in entry.get("release_tasks", []):
            if isinstance(task, dict):
                per_entry.append(certify_task(entry, task))
        update_entry(path, entry, per_entry)
        task_reports.extend(per_entry)
        missing_forms = entry.get("missing_forms", [])
        blockers = entry.get("release_blockers", [])
        dual_pass = bool(per_entry) and all(report["status"] == "pass" for report in per_entry)
        dual_fail = any(report["status"] == "fail" for report in per_entry)
        dual_status = "pass" if dual_pass else ("fail" if dual_fail else "pending")
        fully_certified = (
            dual_pass
            and entry.get("certification", {}).get("static") == "pass"
            and not missing_forms
            and not blockers
        )
        entry_reports.append(
            {
                "entry_id": entry["release_entry_id"],
                "release_task_count": len(per_entry),
                "dual": dual_status,
                "fully_certified": fully_certified,
                "missing_forms": missing_forms,
                "release_blockers": blockers,
            }
        )

    issue_count = sum(int(report["failure_count"]) for report in task_reports)
    source_equivalence_failure_count = sum(
        int(report["source_equivalence_failure_count"]) for report in task_reports
    )
    source_equivalence_blocked_release_task_count = sum(
        1
        for report in task_reports
        if report["status"] == "pending" and int(report["source_equivalence_failure_count"]) > 0
    )
    pending_count = sum(1 for report in task_reports if report["status"] == "pending")
    backend_mismatch_count = sum(
        1
        for report in task_reports
        if report["backend_status"]["evas"] == "pass" and report["backend_status"]["spectre"] == "fail"
    )
    status = "pass" if issue_count == 0 and pending_count == 0 else ("fail" if issue_count else "partial")
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "source": "main120 gold dual evidence from 2026-05-08",
        "simulator_rerun": False,
        "dual_certified_release_task_count": sum(1 for report in task_reports if report["status"] == "pass"),
        "dual_failed_release_task_count": sum(1 for report in task_reports if report["status"] == "fail"),
        "dual_pending_release_task_count": pending_count,
        "dual_pass_materialized_entry_count": sum(1 for report in entry_reports if report["dual"] == "pass"),
        "dual_pending_materialized_entry_count": sum(1 for report in entry_reports if report["dual"] == "pending"),
        "dual_failed_materialized_entry_count": sum(1 for report in entry_reports if report["dual"] == "fail"),
        "fully_certified_entry_count": sum(1 for report in entry_reports if report["fully_certified"]),
        "entry_count": len(entry_reports),
        "issue_count": issue_count,
        "source_equivalence_failure_count": source_equivalence_failure_count,
        "source_equivalence_blocked_release_task_count": source_equivalence_blocked_release_task_count,
        "evas_pass_spectre_fail_count": backend_mismatch_count,
        "task_reports": task_reports,
        "entry_reports": entry_reports,
        "notes": [
            "This imports historical EVAS/Spectre main120 gold evidence; it does not rerun simulators.",
            "A release form is linked only when historical staged source hashes match release gold source hashes.",
            "Entries with missing required forms remain not fully certified even if all materialized forms pass.",
        ],
    }


def write_markdown(report: dict[str, object]) -> None:
    failures = [task for task in report["task_reports"] if task["status"] != "pass"]
    incomplete = [entry for entry in report["entry_reports"] if not entry["fully_certified"]]
    lines = [
        "# vaBench Release EVAS/Spectre Certification Import",
        "",
        f"Date: {report['date']}",
        "",
        "This report links materialized release forms to historical main120 gold",
        "EVAS/Spectre evidence. It is a traceable evidence import, not a simulator",
        "rerun.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| dual-certified release forms | {report['dual_certified_release_task_count']} |",
        f"| dual-failed release forms | {report['dual_failed_release_task_count']} |",
        f"| dual-pending release forms | {report['dual_pending_release_task_count']} |",
        f"| dual-pass materialized entries | {report['dual_pass_materialized_entry_count']} |",
        f"| dual-pending materialized entries | {report['dual_pending_materialized_entry_count']} |",
        f"| dual-failed materialized entries | {report['dual_failed_materialized_entry_count']} |",
        f"| fully certified entries | {report['fully_certified_entry_count']} |",
        f"| entries with materialized assets | {report['entry_count']} |",
        f"| hard simulator/import issues | {report['issue_count']} |",
        f"| source-equivalence blocked forms | {report['source_equivalence_blocked_release_task_count']} |",
        f"| source-equivalence blocker details | {report['source_equivalence_failure_count']} |",
        f"| EVAS PASS / Spectre FAIL count | {report['evas_pass_spectre_fail_count']} |",
        f"| simulator rerun | `{report['simulator_rerun']}` |",
        "",
        "## Pending Or Failed Forms",
        "",
        "| Entry | Form | Status | Failures | Pending blockers |",
        "| --- | --- | --- | --- | --- |",
    ]
    if failures:
        for task in failures:
            lines.append(
                f"| `{task['entry_id']}` | `{task['form']}` | `{task['status']}` | "
                f"{'; '.join(task['failures'])} | {'; '.join(task['pending_blockers'])} |"
            )
    else:
        lines.append("| none | none | none |")

    lines.extend(["", "## Incomplete Entries", "", "| Entry | Missing forms | Blockers |", "| --- | --- | --- |"])
    if incomplete:
        for entry in incomplete:
            missing = "|".join(entry["missing_forms"]) if entry["missing_forms"] else ""
            blockers = "|".join(entry["release_blockers"]) if entry["release_blockers"] else ""
            lines.append(f"| `{entry['entry_id']}` | `{missing}` | `{blockers}` |")
    else:
        lines.append("| none | none | none |")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "imported dual evidence for {forms} release forms; {entries} fully certified entries; {issues} issues".format(
            forms=report["dual_certified_release_task_count"],
            entries=report["fully_certified_entry_count"],
            issues=report["issue_count"],
        )
    )


if __name__ == "__main__":
    main()
