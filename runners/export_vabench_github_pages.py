#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORTS_ROOT = ROOT / "benchmark-vabench-release-v1" / "reports"
MANIFEST_JSON = ROOT / "benchmark-vabench-release-v1" / "MANIFEST.json"
OVERVIEW_JSON = REPORTS_ROOT / "benchmark_overview.json"
DOCS_ROOT = ROOT / "docs"
DOCS_DATA_ROOT = DOCS_ROOT / "data"
MAX_INLINE_FILE_CHARS = 240_000


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def repo_path(path: str | None) -> Path | None:
    if not path:
        return None
    candidate = (ROOT / path).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate


def file_language(path: str | None) -> str:
    suffix = Path(path or "").suffix.lower()
    return {
        ".md": "markdown",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".json": "json",
        ".va": "verilog-a",
        ".vams": "verilog-a",
        ".scs": "spectre",
    }.get(suffix, "text")


def read_inline_text(path: str | None, *, pretty_json: bool = False) -> dict[str, Any]:
    source = repo_path(path)
    if source is None or not source.exists() or not source.is_file():
        return {
            "path": path,
            "exists": False,
            "language": file_language(path),
            "size_bytes": None,
            "truncated": False,
            "content": "",
        }
    raw = source.read_text(encoding="utf-8", errors="replace")
    content = raw
    if pretty_json:
        try:
            content = json.dumps(json.loads(raw), indent=2, sort_keys=True)
        except json.JSONDecodeError:
            content = raw
    truncated = len(content) > MAX_INLINE_FILE_CHARS
    if truncated:
        content = content[:MAX_INLINE_FILE_CHARS] + "\n\n[truncated in website export]"
    return {
        "path": path,
        "exists": True,
        "language": file_language(path),
        "size_bytes": source.stat().st_size,
        "truncated": truncated,
        "content": content,
    }


def pass_rate(pass_count: Any, total: Any) -> float | None:
    try:
        passed = int(pass_count)
        denominator = int(total)
    except (TypeError, ValueError):
        return None
    if denominator <= 0:
        return None
    return passed / denominator


def backend_pass_rows(row: dict[str, Any]) -> int:
    if isinstance(row.get("behavior_checker_pass_rows"), int):
        return int(row["behavior_checker_pass_rows"])
    if isinstance(row.get("spectre_ok_rows"), int):
        return int(row["spectre_ok_rows"])
    return int(row.get("rows") or 0)


def normalize_backend_row(row: dict[str, Any]) -> dict[str, Any]:
    total = int(row.get("total") or row.get("rows") or 0)
    passed = backend_pass_rows(row)
    return {
        "backend": row.get("backend"),
        "label": row.get("label"),
        "status": row.get("full_300_status"),
        "certification_passed": bool(row.get("certification_passed")),
        "run_completed": bool(row.get("run_completed")),
        "pass_rows": passed,
        "total_rows": total,
        "pass_rate": pass_rate(passed, total),
        "spectre_ok_rows": row.get("spectre_ok_rows"),
        "behavior_checker_pass_rows": row.get("behavior_checker_pass_rows"),
        "behavior_checker_missing_rows": row.get("behavior_checker_missing_rows", row.get("no_checker_rows")),
        "nonpass_rows": row.get("nonpass_rows", row.get("behavior_checker_nonpass_rows")),
        "evidence": row.get("evidence"),
        "notes": row.get("notes"),
    }


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() == "true"
    return bool(value)


def manifest_rows_by_key(manifest: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for row in manifest.get("forms", []):
        if not isinstance(row, dict):
            continue
        rows[(str(row.get("release_entry_id") or ""), str(row.get("form") or ""))] = row
    return rows


def normalize_task_row(row: dict[str, Any], manifest_row: dict[str, Any] | None = None) -> dict[str, Any]:
    expansion_status = str(row.get("expansion_status") or "")
    provenance = "promoted_v1.1" if "v1.1" in expansion_status else "inherited_v1"
    manifest_row = manifest_row or {}
    search_parts = [
        row.get("task_id"),
        row.get("legacy_task_id"),
        row.get("release_entry_id"),
        row.get("category"),
        row.get("base_function"),
        row.get("level"),
        row.get("form"),
        row.get("difficulty"),
        row.get("track"),
        provenance,
        manifest_row.get("prompt"),
        manifest_row.get("checks"),
    ]
    return {
        "task_id": row.get("task_id"),
        "legacy_task_id": row.get("legacy_task_id"),
        "release_entry_id": row.get("release_entry_id"),
        "form": row.get("form"),
        "level": row.get("level"),
        "track": row.get("track"),
        "difficulty": row.get("difficulty"),
        "category": row.get("category"),
        "base_function": row.get("base_function"),
        "counted_in_score": boolish(row.get("counted_in_score")),
        "content_denominator_included": boolish(row.get("content_denominator_included")),
        "static": row.get("static"),
        "evas": row.get("evas"),
        "spectre": row.get("spectre"),
        "verdict": row.get("verdict"),
        "source_equivalence_pass": boolish(row.get("source_equivalence_pass")),
        "parity_status": row.get("parity_status"),
        "parity_policy": row.get("parity_policy"),
        "signals_compared": row.get("signals_compared"),
        "samples": row.get("samples"),
        "mean_relative_rms_error": row.get("mean_relative_rms_error"),
        "max_relative_rms_error": row.get("max_relative_rms_error"),
        "max_rmse_v": row.get("max_rmse_v"),
        "max_abs_v": row.get("max_abs_v"),
        "max_digital_mismatch_ratio": row.get("max_digital_mismatch_ratio"),
        "relative_gain_delta": row.get("relative_gain_delta"),
        "expansion_status": row.get("expansion_status"),
        "gold_status": row.get("gold_status"),
        "evidence": row.get("evidence"),
        "provenance": provenance,
        "family": manifest_row.get("family"),
        "prompt": manifest_row.get("prompt"),
        "checks": manifest_row.get("checks"),
        "meta": manifest_row.get("meta"),
        "release_task_manifest": manifest_row.get("release_task_manifest"),
        "gold_count": manifest_row.get("gold_count"),
        "certification": manifest_row.get("certification"),
        "exclusion_reasons": manifest_row.get("exclusion_reasons", []),
        "content_exclusion_reasons": manifest_row.get("content_exclusion_reasons", []),
        "search_text": " ".join(str(part) for part in search_parts if part).lower(),
    }


def unique_values(rows: list[dict[str, Any]], key: str) -> list[str]:
    return sorted({str(row.get(key)) for row in rows if row.get(key) not in (None, "")})


def build_site_summary(overview: dict[str, Any]) -> dict[str, Any]:
    summary = overview.get("summary", {})
    expansion = overview.get("vabench300_expansion", {})
    metrics = overview.get("aggregate_parity_metrics", {})
    backend = overview.get("backend_coverage", {})
    return {
        "generated_at": date.today().isoformat(),
        "release": overview.get("release"),
        "status": overview.get("status"),
        "summary": summary,
        "vabench300_expansion": expansion,
        "aggregate_parity_metrics": metrics,
        "equivalence_contract": overview.get("equivalence_contract", {}),
        "claim_boundary": overview.get("claim_boundary", []),
        "source_reports": overview.get("source_reports", {}),
        "provenance": {
            "public_denominator": summary.get("form_count"),
            "inherited_v1_rows": summary.get("existing_certified_v1_task_count"),
            "promoted_v1_1_rows": summary.get("promoted_v11_task_count"),
            "explanation": expansion.get("explanation"),
        },
        "headline_cards": [
            {
                "label": "Benchmark Rows",
                "value": summary.get("form_count"),
                "detail": "single vaBench 300 management denominator",
            },
            {
                "label": "Release Entries",
                "value": summary.get("entry_count"),
                "detail": "function-level entries behind the 300 rows",
            },
            {
                "label": "Four-Backend Status",
                "value": summary.get("four_backend_status"),
                "detail": f"{backend.get('certified_backend_count', 0)} / {backend.get('required_backend_count', 0)} certified",
            },
            {
                "label": "EVAS PASS / Spectre FAIL",
                "value": summary.get("evas_pass_spectre_fail_count"),
                "detail": "audited release mismatch count",
            },
            {
                "label": "Scored Rows",
                "value": summary.get("scored_form_count"),
                "detail": "rows counted in current score surface",
            },
            {
                "label": "Parity Rows",
                "value": metrics.get("parity_passed_form_count"),
                "detail": f"of {metrics.get('parity_form_count')} parity-certified rows",
            },
        ],
    }


def build_backend_coverage(overview: dict[str, Any]) -> dict[str, Any]:
    coverage = overview.get("backend_coverage", {})
    rows = [normalize_backend_row(row) for row in coverage.get("rows", []) if isinstance(row, dict)]
    return {
        "generated_at": date.today().isoformat(),
        "status": coverage.get("status"),
        "required_backend_count": coverage.get("required_backend_count"),
        "completed_backend_count": coverage.get("completed_backend_count"),
        "certified_backend_count": coverage.get("certified_backend_count"),
        "claim_boundary": coverage.get("claim_boundary"),
        "rows": rows,
    }


def build_task_gallery(overview: dict[str, Any], manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    manifest_by_key = manifest_rows_by_key(manifest or {})
    rows = [
        normalize_task_row(row, manifest_by_key.get((str(row.get("release_entry_id") or ""), str(row.get("form") or ""))))
        for row in overview.get("form_rows", [])
        if isinstance(row, dict)
    ]
    return {
        "generated_at": date.today().isoformat(),
        "summary": {
            "row_count": len(rows),
            "promoted_v1_1_rows": sum(1 for row in rows if row["provenance"] == "promoted_v1.1"),
            "inherited_v1_rows": sum(1 for row in rows if row["provenance"] == "inherited_v1"),
            "certified_rows": sum(1 for row in rows if row.get("verdict") == "pass"),
            "scored_rows": sum(1 for row in rows if row.get("counted_in_score")),
        },
        "filters": {
            "category": unique_values(rows, "category"),
            "level": unique_values(rows, "level"),
            "form": unique_values(rows, "form"),
            "track": unique_values(rows, "track"),
            "difficulty": unique_values(rows, "difficulty"),
            "provenance": unique_values(rows, "provenance"),
        },
        "rows": rows,
    }


def release_task_artifacts(path: str | None) -> dict[str, Any]:
    source = repo_path(path)
    if source is None or not source.exists() or not source.is_file():
        return {}
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    artifacts = payload.get("artifacts", {})
    return artifacts if isinstance(artifacts, dict) else {}


def content_file(kind: str, label: str, path: str | None, *, pretty_json: bool = False) -> dict[str, Any]:
    file_payload = read_inline_text(path, pretty_json=pretty_json)
    return {
        "kind": kind,
        "label": label,
        **file_payload,
    }


def build_task_details(manifest: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    prompt_count = checks_count = meta_count = release_task_count = gold_file_count = truncated_count = 0
    for row in manifest.get("forms", []):
        if not isinstance(row, dict):
            continue
        release_task_path = row.get("release_task_manifest")
        artifacts = release_task_artifacts(release_task_path)
        files = [
            content_file("prompt", "Prompt", row.get("prompt"), pretty_json=False),
            content_file("checks", "Checker", row.get("checks"), pretty_json=False),
            content_file("meta", "Metadata", row.get("meta"), pretty_json=True),
            content_file("release_task", "Release task manifest", release_task_path, pretty_json=True),
        ]
        gold_paths = artifacts.get("gold", [])
        if isinstance(gold_paths, str):
            gold_paths = [gold_paths]
        if isinstance(gold_paths, list):
            for index, gold_path in enumerate(gold_paths, start=1):
                files.append(content_file("gold", f"Gold artifact {index}", str(gold_path), pretty_json=False))
        prompt_count += int(bool(files[0].get("exists")))
        checks_count += int(bool(files[1].get("exists")))
        meta_count += int(bool(files[2].get("exists")))
        release_task_count += int(bool(files[3].get("exists")))
        gold_file_count += sum(1 for file in files if file.get("kind") == "gold" and file.get("exists"))
        truncated_count += sum(1 for file in files if file.get("truncated"))
        rows.append(
            {
                "release_entry_id": row.get("release_entry_id"),
                "form": row.get("form"),
                "task_id": row.get("task_id"),
                "base_function": row.get("base_function"),
                "files": files,
            }
        )
    return {
        "generated_at": date.today().isoformat(),
        "summary": {
            "row_count": len(rows),
            "prompt_count": prompt_count,
            "checks_count": checks_count,
            "meta_count": meta_count,
            "release_task_count": release_task_count,
            "gold_file_count": gold_file_count,
            "truncated_file_count": truncated_count,
            "max_inline_file_chars": MAX_INLINE_FILE_CHARS,
        },
        "rows": rows,
    }


def build_category_coverage(overview: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": date.today().isoformat(),
        "rows": overview.get("category_rows", []),
    }


def export_site(output_dir: Path = DOCS_DATA_ROOT) -> dict[str, Path]:
    overview = read_json(OVERVIEW_JSON)
    manifest = read_json(MANIFEST_JSON)
    payloads = {
        "site_summary.json": build_site_summary(overview),
        "backend_coverage.json": build_backend_coverage(overview),
        "task_gallery.json": build_task_gallery(overview, manifest),
        "task_details.json": build_task_details(manifest),
        "category_coverage.json": build_category_coverage(overview),
    }
    written: dict[str, Path] = {}
    for filename, payload in payloads.items():
        path = output_dir / filename
        write_json(path, payload)
        written[filename] = path
    return written


def main() -> None:
    written = export_site()
    for name, path in written.items():
        print(f"{name}: {path.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
