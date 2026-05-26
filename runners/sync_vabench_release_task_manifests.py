#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
REPORT_JSON = REPORTS_ROOT / "release_task_manifest_sync.json"
REPORT_MD = REPORTS_ROOT / "release_task_manifest_sync.md"
FORM_TO_FAMILY = {
    "dut": "spec-to-va",
    "tb": "tb-generation",
    "bugfix": "bugfix",
    "e2e": "end-to-end",
}


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def release_task_payload(entry: dict[str, object], task: dict[str, object]) -> dict[str, object]:
    form = str(task["form"])
    release_path = ROOT / str(task["release_path"])
    counts = entry.get(
        "counts",
        {
            "benchmark_score": False,
            "model_capability": False,
            "l0_conformance": False,
        },
    )
    score_enabled = isinstance(counts, dict) and bool(counts.get("benchmark_score", False))
    certification = {
        "static": task.get("static_status", entry.get("certification", {}).get("static", "pending")),
        "evas": task.get("evas_status", "pending"),
        "spectre": task.get("spectre_status", "pending"),
        "evidence": task.get("dual_evidence") or task.get("static_evidence") or entry.get("certification", {}).get("evidence", ""),
    }
    artifacts = {
        "prompt": task["prompt"],
        "meta": task["meta"],
        "checks": task["checks"],
        "gold": task.get("gold", []),
    }
    for optional_key in ("public_inputs", "submission_artifacts", "private_reference_artifacts"):
        if optional_key in task:
            artifacts[optional_key] = task[optional_key]
    return {
        "id": f"{entry['release_entry_id']}:{form}",
        "benchmark": "vabench-release-v1",
        "release_entry_id": entry["release_entry_id"],
        "level": entry["level"],
        "track": entry.get("track", "core"),
        "difficulty": entry.get("difficulty", "D2"),
        "category": entry["category"],
        "base_function": entry["base_function"],
        "family": FORM_TO_FAMILY[form],
        "domain": "voltage",
        "score_surface": entry["score_surface"],
        "artifacts": artifacts,
        "certification": certification,
        "counts": counts,
        "source": {
            "source_base_id": entry.get("source_base_id", ""),
            "source_task_id": task.get("release_source_task_id") or task.get("historical_source_task_id", ""),
            "historical_source_task_id": task.get("historical_source_task_id", ""),
            "release_path": rel(release_path),
        },
        "notes": [
            "Generated from release_entry.json so each materialized form has a schema-valid release task manifest.",
            (
                "benchmark_score is enabled because this release entry is in the frozen score denominator."
                if score_enabled
                else "benchmark_score remains disabled because this release entry is outside the frozen score denominator."
            ),
        ],
    }


def build_report() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for entry_path in sorted(TASKS_ROOT.glob("*/vbr1_*/release_entry.json")):
        entry = read_json(entry_path)
        for task in entry.get("release_tasks", []):
            if not isinstance(task, dict):
                continue
            release_path = ROOT / str(task["release_path"])
            manifest_path = release_path / "release_task.json"
            payload = release_task_payload(entry, task)
            write_json(manifest_path, payload)
            rows.append(
                {
                    "release_entry_id": entry["release_entry_id"],
                    "form": task["form"],
                    "track": entry.get("track", "core"),
                    "difficulty": entry.get("difficulty", "D2"),
                    "manifest": rel(manifest_path),
                    "static": payload["certification"]["static"],
                    "evas": payload["certification"]["evas"],
                    "spectre": payload["certification"]["spectre"],
                }
            )
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "pass",
        "release_task_manifest_count": len(rows),
        "rows": rows,
        "notes": [
            "release_task.json manifests are generated from release_entry.json and are checked by schema_validation.json.",
        ],
    }


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Task Manifest Sync",
        "",
        f"Date: {report['date']}",
        "",
        "This report records generated per-form `release_task.json` manifests.",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| release task manifests | {report['release_task_manifest_count']} |",
    ]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    write_json(REPORT_JSON, report)
    write_markdown(report)
    print(
        "synced release task manifests: count={count}".format(
            count=report["release_task_manifest_count"],
        )
    )


if __name__ == "__main__":
    main()
