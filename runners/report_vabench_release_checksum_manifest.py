#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
REPORT_JSON = REPORTS_ROOT / "checksum_manifest.json"
REPORT_MD = REPORTS_ROOT / "checksum_manifest.md"
INCLUDED_ROOTS = [
    PACKAGE_ROOT / "README.md",
    PACKAGE_ROOT / "EVALUATOR.json",
    PACKAGE_ROOT / "EVALUATOR.md",
    PACKAGE_ROOT / "MANIFEST.json",
    PACKAGE_ROOT / "MANIFEST.csv",
    PACKAGE_ROOT / "MANIFEST.md",
    PACKAGE_ROOT / "tasks",
    PACKAGE_ROOT / "conformance",
    PACKAGE_ROOT / "evidence",
    PACKAGE_ROOT / "reports",
    ROOT / "schemas",
    ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv",
    ROOT / "docs" / "VABENCH_RELEASE_TRACKER.md",
    ROOT / "docs" / "VABENCH_LONGRUN_GOAL.md",
]
EXCLUDED_NAMES = {
    "checksum_manifest.json",
    "checksum_manifest.md",
}
EXCLUDED_PATHS = {
    REPORT_JSON,
    REPORT_MD,
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_files() -> list[Path]:
    files: list[Path] = []
    for root in INCLUDED_ROOTS:
        if not root.exists():
            continue
        if root.is_file():
            if root not in EXCLUDED_PATHS:
                files.append(root)
            continue
        for path in root.rglob("*"):
            if path.is_file() and path not in EXCLUDED_PATHS:
                files.append(path)
    return sorted(set(files), key=rel)


def category_for(path: Path) -> str:
    relative = rel(path)
    if relative.startswith("benchmark-vabench-release-v1/tasks/"):
        return "release_tasks"
    if relative.startswith("benchmark-vabench-release-v1/evidence/"):
        return "release_evidence"
    if relative.startswith("benchmark-vabench-release-v1/conformance/"):
        return "l0_conformance"
    if relative.startswith("benchmark-vabench-release-v1/reports/"):
        return "release_reports"
    if relative.startswith("schemas/"):
        return "schemas"
    if relative.startswith("docs/"):
        return "release_docs"
    return "other"


def build_report() -> dict[str, object]:
    files = iter_files()
    rows = [
        {
            "path": rel(path),
            "category": category_for(path),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in files
    ]
    category_counts = dict(sorted(Counter(row["category"] for row in rows).items()))
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "pass",
        "algorithm": "sha256",
        "file_count": len(rows),
        "total_bytes": sum(int(row["bytes"]) for row in rows),
        "category_counts": category_counts,
        "excluded_files": sorted(EXCLUDED_NAMES),
        "files": rows,
        "notes": [
            "This manifest hashes release package, release docs, and schema files for reproducibility.",
            "The checksum manifest excludes itself to avoid self-referential hash instability.",
            "Checksums support artifact traceability; they are not simulator certification evidence.",
        ],
    }


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Checksum Manifest",
        "",
        f"Date: {report['date']}",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| files | {report['file_count']} |",
        f"| total bytes | {report['total_bytes']} |",
        "",
        "## Category Counts",
        "",
        "| Category | Files |",
        "| --- | ---: |",
    ]
    for category, count in report["category_counts"].items():
        lines.append(f"| `{category}` | {count} |")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "wrote checksum manifest: status={status}; files={files}; bytes={bytes}".format(
            status=report["status"],
            files=report["file_count"],
            bytes=report["total_bytes"],
        )
    )


if __name__ == "__main__":
    main()
