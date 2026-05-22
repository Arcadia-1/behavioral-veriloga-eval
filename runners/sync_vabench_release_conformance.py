#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "conformance" / "evas-spectre"
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
DEST_ROOT = PACKAGE_ROOT / "conformance" / "evas-spectre"
REPORT_JSON = PACKAGE_ROOT / "reports" / "conformance_manifest.json"
REPORT_MD = PACKAGE_ROOT / "reports" / "conformance_manifest.md"
REPORT_CSV = PACKAGE_ROOT / "reports" / "conformance_manifest.csv"

MANIFEST_FIELDS = [
    "id",
    "suite",
    "conformance_axis",
    "expected_relation",
    "source_path",
    "package_path",
    "model_capability",
    "benchmark_coverage",
    "bugfix_claim",
    "broad_parity_denominator",
    "runner_hook_required",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def source_cases() -> list[Path]:
    return sorted(path for path in SOURCE_ROOT.iterdir() if path.is_dir())


def validate_meta(meta: dict[str, object], path: Path) -> None:
    if meta.get("asset_type") != "evas_spectre_conformance":
        raise RuntimeError(f"{path}: asset_type must be evas_spectre_conformance")
    if meta.get("suite") != "evas-spectre":
        raise RuntimeError(f"{path}: suite must be evas-spectre")
    counts = meta.get("counts")
    if not isinstance(counts, dict):
        raise RuntimeError(f"{path}: counts must be an object")
    for key in ("model_capability", "benchmark_coverage", "bugfix_claim", "broad_parity_denominator"):
        if counts.get(key) is not False:
            raise RuntimeError(f"{path}: counts.{key} must be false")


def copy_case(case_dir: Path) -> dict[str, str]:
    meta_path = case_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    validate_meta(meta, meta_path)

    dest_dir = DEST_ROOT / case_dir.name
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    shutil.copytree(case_dir, dest_dir)

    counts = meta["counts"]
    runner_hook = meta.get("runner_hook", {})
    return {
        "id": str(meta.get("id", case_dir.name)),
        "suite": str(meta["suite"]),
        "conformance_axis": str(meta["conformance_axis"]),
        "expected_relation": str(meta["expected_relation"]),
        "source_path": rel(case_dir),
        "package_path": rel(dest_dir),
        "model_capability": str(counts["model_capability"]).lower(),
        "benchmark_coverage": str(counts["benchmark_coverage"]).lower(),
        "bugfix_claim": str(counts["bugfix_claim"]).lower(),
        "broad_parity_denominator": str(counts["broad_parity_denominator"]).lower(),
        "runner_hook_required": str(isinstance(runner_hook, dict) and runner_hook.get("required") is True).lower(),
    }


def write_reports(rows: list[dict[str, str]]) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    report = {
        "date": date.today().isoformat(),
        "suite": "evas-spectre",
        "conformance_case_count": len(rows),
        "model_capability_count": sum(1 for row in rows if row["model_capability"] == "true"),
        "benchmark_coverage_count": sum(1 for row in rows if row["benchmark_coverage"] == "true"),
        "bugfix_claim_count": sum(1 for row in rows if row["bugfix_claim"] == "true"),
        "broad_parity_denominator_count": sum(1 for row in rows if row["broad_parity_denominator"] == "true"),
        "runner_hook_required_count": sum(1 for row in rows if row["runner_hook_required"] == "true"),
        "cases": rows,
        "notes": [
            "L0 conformance cases are copied into the release package as simulator diagnostics.",
            "They are excluded from L1/L2 benchmark coverage, model capability, bugfix, and broad parity denominators.",
        ],
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# vaBench Release L0 Conformance Manifest",
        "",
        f"Date: {report['date']}",
        "",
        "These cases are EVAS/Spectre diagnostics. They are intentionally outside",
        "the scored L1/L2 vaBench benchmark denominator.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| conformance cases | {report['conformance_case_count']} |",
        f"| model capability count | {report['model_capability_count']} |",
        f"| benchmark coverage count | {report['benchmark_coverage_count']} |",
        f"| bugfix claim count | {report['bugfix_claim_count']} |",
        f"| broad parity denominator count | {report['broad_parity_denominator_count']} |",
        f"| runner hooks required | {report['runner_hook_required_count']} |",
        "",
        "## Cases",
        "",
        "| ID | Axis | Expected relation | Package path |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['id']}` | `{row['conformance_axis']}` | `{row['expected_relation']}` | `{row['package_path']}` |"
        )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    DEST_ROOT.mkdir(parents=True, exist_ok=True)
    rows = [copy_case(case_dir) for case_dir in source_cases()]
    write_reports(rows)
    print(f"synced {len(rows)} L0 EVAS/Spectre conformance cases")


if __name__ == "__main__":
    main()
