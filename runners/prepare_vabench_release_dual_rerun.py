#!/usr/bin/env python3
from __future__ import annotations

import csv
import argparse
import json
import re
import shutil
from collections import Counter
from datetime import date
from pathlib import Path

from simulate_evas import has_behavior_check
from vabench_release_paths import release_entry_dir, release_entry_path, release_form_dir


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
QUEUE_JSON = PACKAGE_ROOT / "reports" / "dual_rerun_queue.json"
STAGING_ROOT = PACKAGE_ROOT / "rerun_staging"
MANIFEST_JSON = PACKAGE_ROOT / "reports" / "dual_rerun_staging_manifest.json"
MANIFEST_CSV = PACKAGE_ROOT / "reports" / "dual_rerun_staging_manifest.csv"
MANIFEST_MD = PACKAGE_ROOT / "reports" / "dual_rerun_staging_manifest.md"


INCLUDE_RE = re.compile(r'^\s*ahdl_include\s+"([^"]+)"', flags=re.MULTILINE)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def form_dir(entry_id: str, form: str) -> Path:
    return release_form_dir(TASKS_ROOT, entry_id, form)


def read_queue_rows(queue_json: Path = QUEUE_JSON) -> list[dict[str, object]]:
    report = read_json(queue_json)
    rows = report.get("rows", [])
    if not isinstance(rows, list):
        raise ValueError(f"invalid queue rows in {queue_json}")
    return [row for row in rows if isinstance(row, dict)]


def release_entry(entry_id: str) -> dict[str, object]:
    path = release_entry_path(TASKS_ROOT, entry_id)
    if not path.exists():
        return {}
    return read_json(path)


def release_task(entry_id: str, form: str) -> dict[str, object]:
    entry = release_entry(entry_id)
    for task in entry.get("release_tasks", []):
        if isinstance(task, dict) and task.get("form") == form:
            return task
    return {}


def normalized_checker_candidates(value: object) -> list[str]:
    text = str(value or "").strip()
    if not text:
        return []
    if ":" in text and not text.startswith("tasks/"):
        text = text.split(":", 1)[1].strip()
    if "/" in text:
        text = Path(text).name
    if text.endswith((".va", ".scs", ".vams")):
        text = Path(text).stem

    candidates = [text]
    for suffix in ("_fixed", "_buggy", "_gold"):
        if text.endswith(suffix):
            candidates.append(text[: -len(suffix)])
    if text.endswith("_ref"):
        candidates.append(text[:-4])
    if text.startswith("dut_"):
        candidates.append(text[4:])
    return list(dict.fromkeys(candidate for candidate in candidates if candidate))


def resolve_checker_task_id(row: dict[str, object]) -> tuple[str, bool, list[str]]:
    entry_id = str(row["entry_id"])
    form = str(row["form"])
    task = release_task(entry_id, form)
    candidates: list[str] = [f"{entry_id}_{form}", entry_id]
    for value in (
        row.get("source_task_id"),
        task.get("source_task_id"),
        task.get("historical_source_task_id"),
        task.get("source_path"),
    ):
        candidates.extend(normalized_checker_candidates(value))

    # Companion tasks often point to a generated release id. Use the original
    # source path when it is machine-readable, e.g. tb_companion_from_e2e:foo.
    source_path = str(task.get("source_path", ""))
    if ":" in source_path:
        candidates.extend(normalized_checker_candidates(source_path.split(":", 1)[1]))

    for candidate in dict.fromkeys(candidates):
        if has_behavior_check(candidate):
            return candidate, True, candidates
    fallback = next(iter(dict.fromkeys(candidates)), str(row.get("source_task_id") or f"{entry_id}_{form}"))
    return fallback, False, candidates


def choose_tb(paths: list[Path]) -> Path | None:
    preferred = sorted(path for path in paths if path.name.startswith("tb") and path.name.endswith("_ref.scs"))
    if preferred:
        return preferred[0]
    fallback = sorted(path for path in paths if path.name.startswith("tb") and path.suffix == ".scs")
    if fallback:
        return fallback[0]
    any_scs = sorted(path for path in paths if path.suffix == ".scs")
    return any_scs[0] if any_scs else None


def ahdl_includes(path: Path) -> list[str]:
    return INCLUDE_RE.findall(path.read_text(encoding="utf-8"))


def sibling_gold_files(entry_id: str) -> list[Path]:
    entry_root = release_entry_dir(TASKS_ROOT, entry_id) / "forms"
    if not entry_root.exists():
        return []
    files: list[Path] = []
    for gold_dir in sorted(entry_root.glob("*/gold")):
        files.extend(sorted(path for path in gold_dir.iterdir() if path.is_file()))
    return files


def source_gold_files(entry_id: str, form: str) -> list[Path]:
    gold_dir = form_dir(entry_id, form) / "gold"
    if not gold_dir.exists():
        return []
    return sorted(path for path in gold_dir.iterdir() if path.is_file())


def files_by_name(files: list[Path]) -> dict[str, list[Path]]:
    by_name: dict[str, list[Path]] = {}
    for path in files:
        by_name.setdefault(path.name, []).append(path)
    return by_name


def resolve_tb(entry_id: str, form: str) -> tuple[Path | None, str | None]:
    source_files = source_gold_files(entry_id, form)
    source_tb = choose_tb([path for path in source_files if path.suffix == ".scs"])
    if source_tb is not None:
        return source_tb, None

    entry_root = release_entry_dir(TASKS_ROOT, entry_id) / "forms"
    for sibling_form in ("e2e", "tb", "dut", "bugfix"):
        if sibling_form == form:
            continue
        sibling_dir = entry_root / sibling_form / "gold"
        if not sibling_dir.exists():
            continue
        tb = choose_tb([path for path in sibling_dir.iterdir() if path.is_file() and path.suffix == ".scs"])
        if tb is not None:
            return tb, f"borrowed_testbench_from_{sibling_form}"
    return None, "no_resolved_testbench"


def resolve_include_sources(
    *,
    entry_id: str,
    form: str,
    includes: list[str],
    variant: str,
) -> tuple[dict[str, Path], list[str]]:
    source_files = source_gold_files(entry_id, form)
    source_by_name = files_by_name(source_files)
    all_by_name = files_by_name(sibling_gold_files(entry_id))
    source_va = sorted(path for path in source_files if path.suffix == ".va")
    fixed = [path for path in source_va if path.name == "dut_fixed.va"]
    buggy = [path for path in source_va if path.name == "dut_buggy.va"]
    single_source_va = source_va[0] if len(source_va) == 1 else None

    resolved: dict[str, Path] = {}
    blockers: list[str] = []
    for idx, include_name in enumerate(includes):
        candidates = source_by_name.get(include_name) or all_by_name.get(include_name) or []
        chosen = candidates[0] if candidates else None
        if form == "bugfix" and idx == 0:
            if variant == "fixed" and fixed:
                chosen = fixed[0]
            elif variant == "buggy" and buggy:
                chosen = buggy[0]
        elif chosen is None and idx == 0 and single_source_va is not None:
            chosen = single_source_va

        if chosen is None:
            blockers.append(f"missing_include_source:{include_name}")
            continue
        resolved[include_name] = chosen
    return resolved, blockers


def copy_form_context(
    src_form_dir: Path,
    dst_task_dir: Path,
    *,
    task_id_suffix: str | None,
    checker_task_id: str,
) -> None:
    for name in ("prompt.md", "checks.yaml"):
        src = src_form_dir / name
        if src.exists():
            shutil.copy2(src, dst_task_dir / name)

    meta_src = src_form_dir / "meta.json"
    meta = read_json(meta_src)
    if task_id_suffix:
        old_id = str(meta.get("task_id") or meta.get("id") or src_form_dir.parent.parent.name)
        meta["task_id"] = f"{old_id}_{task_id_suffix}"
        meta["id"] = f"{old_id}_{task_id_suffix}"
        meta["rerun_variant"] = task_id_suffix
    meta["checker_task_id"] = checker_task_id
    write_json(dst_task_dir / "meta.json", meta)


def stage_bundle(
    *,
    row: dict[str, object],
    variant: str,
    expected_result: str,
    staging_root: Path = STAGING_ROOT,
) -> dict[str, object]:
    entry_id = str(row["entry_id"])
    form = str(row["form"])
    src_form_dir = form_dir(entry_id, form)
    task_id_suffix = None if variant == "gold" else variant
    checker_task_id, checker_available, checker_candidates = resolve_checker_task_id(row)
    dst_task_dir = staging_root / entry_id / form / variant
    dst_gold_dir = dst_task_dir / "gold"
    record: dict[str, object] = {
        "entry_id": entry_id,
        "form": form,
        "variant": variant,
        "expected_result": expected_result,
        "source_task_id": row.get("source_task_id"),
        "checker_task_id": checker_task_id,
        "checker_available": checker_available,
        "checker_candidates": checker_candidates,
        "queue_reason": row.get("queue_reason"),
        "status": "blocked",
        "blockers": [],
        "staged_task_dir": rel(dst_task_dir),
        "staged_gold_dir": rel(dst_gold_dir),
        "source_testbench": "",
        "source_includes": [],
        "source_include_origins": {},
        "staged_testbench": "",
        "staged_includes": [],
        "notes": [],
    }

    if not src_form_dir.exists():
        record["blockers"] = ["missing_release_form_dir"]
        return record

    tb, tb_note = resolve_tb(entry_id, form)
    if tb is None:
        record["blockers"] = [tb_note or "no_resolved_testbench"]
        return record
    if tb_note:
        record["notes"] = [tb_note]

    includes = ahdl_includes(tb)
    if not includes:
        record["blockers"] = [f"no_ahdl_include:{rel(tb)}"]
        return record

    include_sources, blockers = resolve_include_sources(
        entry_id=entry_id,
        form=form,
        includes=includes,
        variant=variant,
    )
    if blockers:
        record["blockers"] = blockers
        record["source_testbench"] = rel(tb)
        record["source_includes"] = includes
        record["source_include_origins"] = {
            name: rel(path) for name, path in include_sources.items()
        }
        return record

    dst_gold_dir.mkdir(parents=True, exist_ok=True)
    copy_form_context(
        src_form_dir,
        dst_task_dir,
        task_id_suffix=task_id_suffix,
        checker_task_id=checker_task_id,
    )
    shutil.copy2(tb, dst_gold_dir / tb.name)
    for include_name, source_path in include_sources.items():
        shutil.copy2(source_path, dst_gold_dir / include_name)

    source_marker = {
        "entry_id": entry_id,
        "form": form,
        "variant": variant,
        "expected_result": expected_result,
        "source_form_dir": rel(src_form_dir),
        "source_testbench": rel(tb),
        "include_sources": {name: rel(path) for name, path in include_sources.items()},
        "queue_reason": row.get("queue_reason"),
        "checker_task_id": checker_task_id,
        "checker_available": checker_available,
    }
    write_json(dst_task_dir / "SOURCE_RERUN_BUNDLE.json", source_marker)

    record.update(
        {
            "status": "ready",
            "source_testbench": rel(tb),
            "source_includes": includes,
            "source_include_origins": {
                name: rel(path) for name, path in include_sources.items()
            },
            "staged_testbench": rel(dst_gold_dir / tb.name),
            "staged_includes": [rel(dst_gold_dir / name) for name in includes],
            "blockers": [],
        }
    )
    return record


def build_manifest(
    *,
    queue_json: Path = QUEUE_JSON,
    staging_root: Path = STAGING_ROOT,
) -> dict[str, object]:
    rows = read_queue_rows(queue_json)
    if staging_root.exists():
        shutil.rmtree(staging_root)
    staging_root.mkdir(parents=True, exist_ok=True)

    bundle_records: list[dict[str, object]] = []
    for row in rows:
        form = str(row["form"])
        if form == "bugfix":
            bundle_records.append(
                stage_bundle(row=row, variant="fixed", expected_result="pass", staging_root=staging_root)
            )
            source_files = source_gold_files(str(row["entry_id"]), form)
            if any(path.name == "dut_buggy.va" for path in source_files):
                bundle_records.append(
                    stage_bundle(row=row, variant="buggy", expected_result="fail", staging_root=staging_root)
                )
        else:
            bundle_records.append(
                stage_bundle(row=row, variant="gold", expected_result="pass", staging_root=staging_root)
            )

    ready_records = [record for record in bundle_records if record["status"] == "ready"]
    blocked_records = [record for record in bundle_records if record["status"] != "ready"]
    queue_ready_forms = {
        (str(record["entry_id"]), str(record["form"]))
        for record in ready_records
        if record["variant"] in {"gold", "fixed"}
    }
    queue_rows_ready = sum(1 for row in rows if (str(row["entry_id"]), str(row["form"])) in queue_ready_forms)
    status = (
        "complete"
        if not rows
        else ("ready" if not blocked_records and queue_rows_ready == len(rows) else "blocked")
    )
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "queue_row_count": len(rows),
        "queue_rows_with_ready_primary_bundle": queue_rows_ready,
        "bundle_count": len(bundle_records),
        "ready_bundle_count": len(ready_records),
        "blocked_bundle_count": len(blocked_records),
        "form_counts": dict(sorted(Counter(str(record["form"]) for record in bundle_records).items())),
        "variant_counts": dict(sorted(Counter(str(record["variant"]) for record in bundle_records).items())),
        "blocker_counts": dict(
            sorted(Counter(blocker for record in blocked_records for blocker in record["blockers"]).items())
        ),
        "queue_json": rel(queue_json) if queue_json.is_relative_to(ROOT) else str(queue_json),
        "staging_root": rel(staging_root) if staging_root.is_relative_to(ROOT) else str(staging_root),
        "bundles": bundle_records,
        "notes": [
            "A primary bundle is the gold/fixed runnable task_dir used to turn a pending release form into fresh EVAS/Spectre evidence.",
            "Bugfix rows also get a buggy companion bundle when dut_buggy.va exists; those bundles are expected to fail the behavioral contract.",
            "This manifest prepares execution inputs only; it is not EVAS/Spectre pass evidence.",
        ],
    }


def write_csv(manifest: dict[str, object], report_csv: Path = MANIFEST_CSV) -> None:
    fields = [
        "entry_id",
        "form",
        "variant",
        "expected_result",
        "status",
        "queue_reason",
        "source_task_id",
        "checker_task_id",
        "checker_available",
        "staged_task_dir",
        "staged_testbench",
        "source_testbench",
        "source_include_origins",
        "blockers",
    ]
    with report_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for record in manifest["bundles"]:
            writer.writerow(
                {
                    field: (
                        ";".join(record[field])
                        if field == "blockers"
                        else json.dumps(record.get(field, {}), sort_keys=True)
                        if field == "source_include_origins"
                        else record.get(field, "")
                    )
                    for field in fields
                }
            )


def write_markdown(manifest: dict[str, object], report_md: Path = MANIFEST_MD) -> None:
    lines = [
        "# vaBench Release Dual Rerun Staging Manifest",
        "",
        f"Date: {manifest['date']}",
        "",
        "This manifest lists runnable staging bundles prepared from",
        "`dual_rerun_queue.json`. It is an execution input, not simulator pass evidence.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| queue rows | {manifest['queue_row_count']} |",
        f"| queue rows with ready primary bundle | {manifest['queue_rows_with_ready_primary_bundle']} |",
        f"| staged bundles | {manifest['bundle_count']} |",
        f"| ready bundles | {manifest['ready_bundle_count']} |",
        f"| blocked bundles | {manifest['blocked_bundle_count']} |",
        "",
        "## Variant Counts",
        "",
        "| Variant | Count |",
        "| --- | ---: |",
    ]
    for variant, count in dict(manifest["variant_counts"]).items():
        lines.append(f"| `{variant}` | {count} |")
    lines.extend(["", "## Bundles", "", "| Entry | Form | Variant | Status | Staged task |", "| --- | --- | --- | --- | --- |"])
    for record in manifest["bundles"]:
        lines.append(
            f"| `{record['entry_id']}` | `{record['form']}` | `{record['variant']}` | "
            f"`{record['status']}` | `{record['staged_task_dir']}` |"
        )
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def path_arg(text: str, *, default_root: Path = ROOT) -> Path:
    path = Path(text)
    return path if path.is_absolute() else default_root / path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Prepare runnable vaBench release dual-rerun bundles.")
    ap.add_argument("--queue-json", default=str(QUEUE_JSON), help="Queue JSON to stage.")
    ap.add_argument("--staging-root", default=str(STAGING_ROOT), help="Directory for staged runnable bundles.")
    ap.add_argument("--manifest-json", default=str(MANIFEST_JSON), help="Output staging manifest JSON.")
    ap.add_argument("--manifest-csv", default=str(MANIFEST_CSV), help="Output staging manifest CSV.")
    ap.add_argument("--manifest-md", default=str(MANIFEST_MD), help="Output staging manifest Markdown.")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    queue_json = path_arg(args.queue_json)
    staging_root = path_arg(args.staging_root)
    manifest_json = path_arg(args.manifest_json)
    manifest_csv = path_arg(args.manifest_csv)
    manifest_md = path_arg(args.manifest_md)
    manifest = build_manifest(queue_json=queue_json, staging_root=staging_root)
    write_json(manifest_json, manifest)
    write_csv(manifest, manifest_csv)
    write_markdown(manifest, manifest_md)
    print(
        "prepared dual rerun staging: {ready}/{total} bundles ready; {rows}/{queue} queue rows runnable".format(
            ready=manifest["ready_bundle_count"],
            total=manifest["bundle_count"],
            rows=manifest["queue_rows_with_ready_primary_bundle"],
            queue=manifest["queue_row_count"],
        )
    )


if __name__ == "__main__":
    main()
