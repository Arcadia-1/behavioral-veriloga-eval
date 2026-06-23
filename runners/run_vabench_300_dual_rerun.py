#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
from collections import Counter
from pathlib import Path

from bridge_preflight import bridge_preflight, resolve_cadence_cshrc
from run_gold_dual_suite import (
    ahdl_includes,
    choose_gold_tb,
    default_bridge_repo,
    default_sui_cadence_cshrc,
    default_sui_host,
    default_sui_work_root,
    normalize_spectre_backend,
    normalize_spectre_mode,
)
from run_vabench_release_dual_rerun import (
    normalize_output_root,
    run_bundles,
    write_summary,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
DEFAULT_MANIFEST = PACKAGE_ROOT / "vabench-300-expansion" / "VABENCH_300_MANIFEST.json"
DEFAULT_OUTPUT_ROOT = ROOT / "results" / "vabench-300-dual-rerun"
PRIMARY_FORMS = {"dut", "tb", "bugfix", "e2e"}
CERTIFIED_EXPANSION_STATUSES = {"existing_certified_v1", "certified_v1.1_promoted"}


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def rel_or_abs(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def normalize_manifest_path(path_text: str) -> Path:
    path = Path(path_text)
    if not path.is_absolute():
        path = ROOT / path
    return path


def task_dir_from_manifest_row(row: dict[str, object]) -> Path:
    meta = row.get("meta")
    if not isinstance(meta, str) or not meta:
        raise ValueError(f"manifest row lacks meta path: {row.get('task_id')}")
    task_dir = ROOT / meta
    return task_dir.parent


def safe_stage_component(value: object) -> str:
    return "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in str(value))


def materialize_runtime_aliases(
    bundles: list[dict[str, object]],
    *,
    output_root: Path,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Stage bugfix forms whose testbench includes the semantic DUT filename.

    The release bugfix assets often store the corrected implementation as
    gold/dut_fixed.va while their Spectre testbench includes the original DUT
    module filename. The historical release staging runner resolves that
    indirection; the direct vaBench-300 manifest runner needs the same runtime
    alias without modifying source benchmark files.
    """

    staged_bundles: list[dict[str, object]] = []
    aliases: list[dict[str, object]] = []
    stage_root = output_root / "_staged_task_dirs"

    for record in bundles:
        staged_record = dict(record)
        if str(record.get("form", "")) != "bugfix":
            staged_bundles.append(staged_record)
            continue

        task_dir = ROOT / str(record["staged_task_dir"])
        gold_dir = task_dir / "gold"
        tb_path = choose_gold_tb(gold_dir)
        if tb_path is None:
            staged_bundles.append(staged_record)
            continue

        missing = [name for name in ahdl_includes(tb_path) if not (gold_dir / name).exists()]
        fixed_dut = gold_dir / "dut_fixed.va"
        if not missing or not fixed_dut.exists():
            staged_bundles.append(staged_record)
            continue

        stage_dir = stage_root / safe_stage_component(record.get("task_id") or record.get("entry_id"))
        shutil.copytree(task_dir, stage_dir, dirs_exist_ok=True)
        stage_gold = stage_dir / "gold"
        for include_name in missing:
            include_path = stage_gold / include_name
            include_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(stage_gold / "dut_fixed.va", include_path)

        staged_record["source_staged_task_dir"] = staged_record["staged_task_dir"]
        staged_record["staged_task_dir"] = rel_or_abs(stage_dir)
        staged_record["runtime_alias_files"] = missing
        aliases.append(
            {
                "task_id": record.get("task_id"),
                "entry_id": record.get("entry_id"),
                "form": record.get("form"),
                "source_staged_task_dir": record.get("staged_task_dir"),
                "runtime_staged_task_dir": staged_record["staged_task_dir"],
                "aliased_files": missing,
            }
        )
        staged_bundles.append(staged_record)

    return staged_bundles, aliases


def row_matches(
    row: dict[str, object],
    *,
    task_ids: set[str] | None,
    legacy_entries: set[str] | None,
    topics: set[str] | None,
    forms: set[str] | None,
    expansion_statuses: set[str] | None,
    include_pending: bool,
) -> bool:
    if task_ids and str(row.get("task_id", "")) not in task_ids:
        return False
    if legacy_entries and str(row.get("legacy_entry_id", "")) not in legacy_entries:
        return False
    if topics and str(row.get("topic_id", "")) not in topics:
        return False
    if forms and str(row.get("form", "")) not in forms:
        return False
    status = str(row.get("expansion_status", ""))
    if expansion_statuses is not None:
        return status in expansion_statuses
    if not include_pending and status not in CERTIFIED_EXPANSION_STATUSES:
        return False
    return True


def make_bundle(row: dict[str, object]) -> dict[str, object]:
    task_dir = task_dir_from_manifest_row(row)
    if not task_dir.exists():
        raise FileNotFoundError(f"task dir missing for {row.get('task_id')}: {task_dir}")

    form = str(row.get("form") or task_dir.name)
    if form not in PRIMARY_FORMS:
        raise ValueError(f"unsupported form for 300 dual rerun: {form!r}")

    return {
        "entry_id": row.get("legacy_entry_id") or row.get("topic_id") or row.get("task_id"),
        "form": form,
        "variant": "gold",
        "expected_result": "pass",
        "staged_task_dir": rel_or_abs(task_dir),
        "source_task_id": row.get("task_id"),
        "task_id": row.get("task_id"),
        "topic_id": row.get("topic_id"),
        "expansion_status": row.get("expansion_status"),
        "certification": row.get("certification"),
        "manifest_spectre": row.get("spectre"),
        "manifest_evas": row.get("evas"),
    }


def select_bundles(
    manifest: dict[str, object],
    *,
    task_ids: set[str] | None,
    legacy_entries: set[str] | None,
    topics: set[str] | None,
    forms: set[str] | None,
    expansion_statuses: set[str] | None,
    include_pending: bool,
    limit: int | None,
) -> list[dict[str, object]]:
    bundles: list[dict[str, object]] = []
    for row in manifest.get("tasks", []):
        if not isinstance(row, dict):
            continue
        if not row_matches(
            row,
            task_ids=task_ids,
            legacy_entries=legacy_entries,
            topics=topics,
            forms=forms,
            expansion_statuses=expansion_statuses,
            include_pending=include_pending,
        ):
            continue
        bundles.append(make_bundle(row))
    bundles.sort(key=lambda item: (str(item["entry_id"]), str(item["form"])))
    if limit is not None:
        bundles = bundles[:limit]
    return bundles


def add_vabench_300_summary_fields(
    summary: dict[str, object],
    *,
    manifest_path: Path,
    manifest: dict[str, object],
    bundles: list[dict[str, object]],
    selection: dict[str, object],
) -> dict[str, object]:
    raw_status_counts: Counter[str] = Counter()
    expansion_counts: Counter[str] = Counter(str(item.get("expansion_status", "")) for item in bundles)
    form_counts: Counter[str] = Counter(str(item.get("form", "")) for item in bundles)
    bundle_by_task_id = {
        str(item.get("task_id", "")): item
        for item in bundles
        if item.get("task_id")
    }
    bundle_by_staged_dir = {
        str(item.get("staged_task_dir", "")): item
        for item in bundles
        if item.get("staged_task_dir")
    }
    bundle_by_entry_form = {
        (str(item.get("entry_id", "")), str(item.get("form", ""))): item
        for item in bundles
    }

    results: list[object] = list(summary.get("results", []))
    for result in results:
        if not isinstance(result, dict):
            continue
        raw = result.get("raw_result")
        raw_task_id = str(raw.get("source_task_id") or raw.get("task_id") or "") if isinstance(raw, dict) else ""
        bundle = (
            bundle_by_task_id.get(str(result.get("source_task_id", "")))
            or bundle_by_task_id.get(str(result.get("task_id", "")))
            or bundle_by_task_id.get(raw_task_id)
            or bundle_by_staged_dir.get(str(result.get("staged_task_dir", "")))
            or bundle_by_entry_form.get((str(result.get("entry_id", "")), str(result.get("form", ""))))
        )
        if bundle is not None:
            result["vabench_300"] = {
                "task_id": bundle.get("task_id"),
                "topic_id": bundle.get("topic_id"),
                "expansion_status": bundle.get("expansion_status"),
                "certification": bundle.get("certification"),
                "manifest_spectre": bundle.get("manifest_spectre"),
                "manifest_evas": bundle.get("manifest_evas"),
            }
        if isinstance(raw, dict):
            raw_status_counts[str(raw.get("status", "UNKNOWN"))] += 1

    enriched = dict(summary)
    enriched["results"] = results
    enriched["vabench_300_manifest"] = rel_or_abs(manifest_path)
    enriched["vabench_300_release"] = manifest.get("release")
    enriched["vabench_300_manifest_status"] = manifest.get("status")
    enriched["selection"] = selection
    enriched["selected_expansion_status_counts"] = dict(sorted(expansion_counts.items()))
    enriched["selected_form_counts"] = dict(sorted(form_counts.items()))
    enriched["raw_status_counts"] = dict(sorted(raw_status_counts.items()))
    return enriched


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Run EVAS/Spectre dual rerun over the vaBench 300 expansion manifest.")
    ap.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="VABENCH_300_MANIFEST.json path.")
    ap.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="Output directory for rerun results.")
    ap.add_argument(
        "--bridge-repo",
        default=os.environ.get("VAEVAS_BRIDGE_REPO", str(default_bridge_repo())),
        help="Path to virtuoso-bridge-lite.",
    )
    ap.add_argument(
        "--spectre-backend",
        default=os.environ.get("VAEVAS_SPECTRE_BACKEND", "bridge"),
        help="Spectre execution backend: bridge (default) or sui-direct.",
    )
    ap.add_argument(
        "--spectre-mode",
        default=os.environ.get("VAEVAS_SPECTRE_MODE", "ax"),
        help="Spectre invocation mode: ax (default, +preset=ax +mt) or reference (plain spectre).",
    )
    ap.add_argument("--sui-host", default=default_sui_host(), help="SSH host used by --spectre-backend=sui-direct.")
    ap.add_argument(
        "--sui-work-root",
        default=default_sui_work_root(),
        help="Remote scratch root used by --spectre-backend=sui-direct.",
    )
    ap.add_argument(
        "--cadence-cshrc",
        default=os.environ.get("VB_CADENCE_CSHRC", ""),
        help="Remote Cadence cshrc path used to expose spectre on PATH.",
    )
    ap.add_argument("--timeout-s", type=int, default=240, help="Per-task simulator timeout.")
    ap.add_argument(
        "--spectre-license-wait-s",
        type=int,
        default=None,
        help="Override Spectre +lqtimeout for license checkout, capped by --timeout-s.",
    )
    ap.add_argument("--limit", type=int, default=None, help="Optional maximum number of tasks to run.")
    ap.add_argument("--task", action="append", help="Restrict to one normalized 300 task_id; may be repeated.")
    ap.add_argument("--entry", action="append", help="Restrict to one legacy_entry_id; may be repeated.")
    ap.add_argument("--topic", action="append", help="Restrict to one normalized topic_id; may be repeated.")
    ap.add_argument("--form", action="append", choices=sorted(PRIMARY_FORMS), help="Restrict by form.")
    ap.add_argument(
        "--expansion-status",
        action="append",
        choices=[
            "existing_certified_v1",
            "certified_v1.1_promoted",
            "proposed_v1.1_pending_certification",
            "provisional_v1.1_management",
        ],
        help="Restrict by expansion status.",
    )
    ap.add_argument(
        "--include-pending",
        action="store_true",
        help=(
            "Compatibility switch for older manifests that still contain pending/provisional rows. "
            "Current vaBench 300 manifests select inherited certified v1 rows by default."
        ),
    )
    ap.add_argument("--workers", type=int, default=1, help="Number of tasks to run concurrently.")
    ap.add_argument("--dry-run", action="store_true", help="Check selection and output shape without simulator calls.")
    ap.add_argument("--skip-bridge-preflight", action="store_true", help="Skip bridge health checks.")
    ap.add_argument("--require-virtuoso-daemon", action="store_true", help="Treat CIW daemon disconnect as a hard blocker.")
    ap.add_argument("--allow-direct-run", action="store_true", help="Allow direct execution outside scripts/run_with_bridge.sh.")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    if args.spectre_license_wait_s is not None:
        os.environ["VAEVAS_SPECTRE_LQTIMEOUT_S"] = str(args.spectre_license_wait_s)

    manifest_path = normalize_manifest_path(args.manifest)
    manifest = read_json(manifest_path)
    spectre_backend = normalize_spectre_backend(args.spectre_backend)
    spectre_mode = normalize_spectre_mode(args.spectre_mode)
    bundles = select_bundles(
        manifest,
        task_ids=set(args.task) if args.task else None,
        legacy_entries=set(args.entry) if args.entry else None,
        topics=set(args.topic) if args.topic else None,
        forms=set(args.form) if args.form else None,
        expansion_statuses=set(args.expansion_status) if args.expansion_status else None,
        include_pending=args.include_pending,
        limit=args.limit,
    )
    output_root = normalize_output_root(args.output_root)
    selection = {
        "task": args.task or [],
        "entry": args.entry or [],
        "topic": args.topic or [],
        "form": args.form or [],
        "expansion_status": args.expansion_status or [],
        "include_pending": bool(args.include_pending),
        "limit": args.limit,
        "spectre_backend": spectre_backend,
        "spectre_mode": spectre_mode,
    }
    runtime_aliases: list[dict[str, object]] = []

    if args.dry_run:
        summary = run_bundles(
            bundles=bundles,
            output_root=output_root,
            bridge_repo=Path(args.bridge_repo),
            cadence_cshrc=args.cadence_cshrc or None,
            timeout_s=args.timeout_s,
            dry_run=True,
            workers=args.workers,
            spectre_backend=spectre_backend,
            spectre_mode=spectre_mode,
            sui_host=args.sui_host if spectre_backend == "sui-direct" else None,
            sui_work_root=args.sui_work_root if spectre_backend == "sui-direct" else None,
        )
        summary = add_vabench_300_summary_fields(
            summary,
            manifest_path=manifest_path,
            manifest=manifest,
            bundles=bundles,
            selection=selection,
        )
        write_summary(output_root / "summary.json", summary)
        print(json.dumps(summary, indent=2))
        return 0

    bundles, runtime_aliases = materialize_runtime_aliases(bundles, output_root=output_root)
    selection["runtime_alias_count"] = len(runtime_aliases)
    selection["runtime_aliases"] = runtime_aliases

    via_wrapper = os.environ.get("VAEVAS_BRIDGE_WRAPPER") == "1"
    if spectre_backend == "bridge" and not via_wrapper and not args.allow_direct_run:
        summary = {
            "status": "blocked",
            "reason": "direct invocation blocked; use scripts/run_with_bridge.sh",
            "tasks_total": len(bundles),
            "vabench_300_manifest": rel_or_abs(manifest_path),
            "selection": selection,
            "spectre_mode": spectre_mode,
            "remediation": [
                "./scripts/run_with_bridge.sh python3 runners/run_vabench_300_dual_rerun.py",
                "or add --allow-direct-run if this is an intentional local smoke run",
            ],
        }
        write_summary(output_root / "summary.json", summary)
        print(json.dumps(summary, indent=2))
        return 2

    bridge_repo = Path(args.bridge_repo).resolve()
    if spectre_backend == "bridge" and not bridge_repo.exists():
        summary = {"status": "blocked", "reason": f"bridge repo not found: {bridge_repo}", "tasks_total": len(bundles)}
        write_summary(output_root / "summary.json", summary)
        print(json.dumps(summary, indent=2))
        return 2

    bridge_profile = os.environ.get("VAEVAS_BRIDGE_PROFILE") or os.environ.get("BRIDGE_PROFILE", "")
    if spectre_backend == "bridge":
        effective_cshrc = resolve_cadence_cshrc(bridge_repo, args.cadence_cshrc, bridge_profile or None)
    else:
        effective_cshrc = args.cadence_cshrc or default_sui_cadence_cshrc()

    if spectre_backend == "sui-direct":
        preflight = {
            "status": "skipped",
            "reason": "direct SUI backend selected; bridge preflight is not required",
            "spectre_backend": spectre_backend,
            "spectre_mode": spectre_mode,
            "sui_host": args.sui_host,
            "sui_work_root": args.sui_work_root,
            "cadence_cshrc": effective_cshrc,
        }
    elif args.skip_bridge_preflight:
        preflight = {"status": "skipped", "bridge_repo": str(bridge_repo), "cadence_cshrc": effective_cshrc}
    else:
        preflight = bridge_preflight(
            bridge_repo,
            cadence_cshrc=effective_cshrc,
            require_daemon=args.require_virtuoso_daemon,
            profile=bridge_profile or None,
        )
        if preflight.get("status") == "blocked":
            summary = {
                "status": "blocked",
                "reason": preflight.get("reason", "bridge preflight failed"),
                "tasks_total": len(bundles),
                "vabench_300_manifest": rel_or_abs(manifest_path),
                "selection": selection,
                "bridge_repo": str(bridge_repo),
                "bridge_profile": bridge_profile,
                "cadence_cshrc": effective_cshrc,
                "spectre_mode": spectre_mode,
                "bridge_preflight": preflight,
            }
            write_summary(output_root / "summary.json", summary)
            print(json.dumps(summary, indent=2))
            return 2

    summary = run_bundles(
        bundles=bundles,
        output_root=output_root,
        bridge_repo=bridge_repo,
        cadence_cshrc=effective_cshrc or None,
        timeout_s=args.timeout_s,
        dry_run=False,
        workers=args.workers,
        spectre_backend=spectre_backend,
        spectre_mode=spectre_mode,
        sui_host=args.sui_host if spectre_backend == "sui-direct" else None,
        sui_work_root=args.sui_work_root if spectre_backend == "sui-direct" else None,
    )
    summary["bridge_preflight"] = preflight
    summary = add_vabench_300_summary_fields(
        summary,
        manifest_path=manifest_path,
        manifest=manifest,
        bundles=bundles,
        selection=selection,
    )
    write_summary(output_root / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    return 0 if summary.get("nonpass_count") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
