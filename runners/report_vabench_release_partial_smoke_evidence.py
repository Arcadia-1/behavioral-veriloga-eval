#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
REPORT_JSON = REPORTS_ROOT / "partial_smoke_evidence.json"
REPORT_MD = REPORTS_ROOT / "partial_smoke_evidence.md"

SMOKE_SUMMARIES = [
    ROOT / "results" / "vabench-release-v1-dual-rerun-smoke-20260516-contract-charge-pump" / "summary.json",
    ROOT / "results" / "vabench-release-v1-dual-rerun-smoke-20260516-contract-representative-bugfix" / "summary.json",
]


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def smoke_row(summary_path: Path) -> dict[str, Any]:
    summary = read_json(summary_path)
    results = summary.get("results", [])
    if not isinstance(results, list):
        results = []
    expected_met = sum(1 for item in results if isinstance(item, dict) and item.get("expected_result_met") is True)
    expected_miss = sum(1 for item in results if isinstance(item, dict) and item.get("expected_result_met") is False)
    entries = sorted({str(item.get("entry_id")) for item in results if isinstance(item, dict) and item.get("entry_id")})
    return {
        "summary": rel(summary_path),
        "exists": summary_path.exists(),
        "status": summary.get("status", "missing"),
        "entries": entries,
        "tasks_total": int(summary.get("tasks_total", len(results)) or 0),
        "expected_met_count": expected_met,
        "expected_miss_count": expected_miss,
        "certification_role": "partial_smoke_pass" if summary_path.exists() and expected_miss == 0 and expected_met > 0 else "not_certification",
        "counts_as_release_certification": False,
    }


def build_report() -> dict[str, Any]:
    rows = [smoke_row(path) for path in SMOKE_SUMMARIES]
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "ready" if all(row["exists"] for row in rows) else "incomplete",
        "counts_as_release_certification": False,
        "rows": rows,
        "notes": [
            "This report records representative EVAS/Spectre dual smoke runs only.",
            "partial_smoke_pass is not full release certification and must not enable benchmark scoring.",
            "Full certification remains controlled by dual_certification.json and score_denominator_manifest.json.",
        ],
    }


def write_markdown(report: dict[str, Any]) -> None:
    lines = [
        "# vaBench Release Partial Smoke Evidence",
        "",
        f"Date: {report['date']}",
        "",
        "This report documents representative EVAS/Spectre dual smoke evidence.",
        "It is intentionally non-certifying.",
        "",
        "| Summary | Entries | Expected met | Expected miss | Role |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for row in report["rows"]:
        lines.append(
            "| `{summary}` | `{entries}` | {met} | {miss} | `{role}` |".format(
                summary=row["summary"],
                entries=", ".join(row["entries"]),
                met=row["expected_met_count"],
                miss=row["expected_miss_count"],
                role=row["certification_role"],
            )
        )
    lines.extend(
        [
            "",
            "Claim boundary: these smoke runs are useful debugging evidence but do not",
            "mark any release entry or form as certified.",
        ]
    )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "partial smoke evidence: status={status}; rows={rows}; certifying=false".format(
            status=report["status"],
            rows=len(report["rows"]),
        )
    )


if __name__ == "__main__":
    main()
