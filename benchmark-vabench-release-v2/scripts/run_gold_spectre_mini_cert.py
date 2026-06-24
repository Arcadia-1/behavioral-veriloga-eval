#!/usr/bin/env python3
"""Run EVAS plus Spectre gold mini-certification for vaBench v2 forms."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any


AHDL_INCLUDE_RE = re.compile(r'^\s*ahdl_include\s+"([^"]+)"', re.M)


def repo_root_from_v2_root(root: Path) -> Path:
    return root.resolve().parent


def ensure_runner_import(repo_root: Path) -> None:
    runners = repo_root / "runners"
    sys.path.insert(0, str(runners.resolve()))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def safe_component(value: object) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value or "case")).strip("_") or "case"


def rel_or_abs(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def spectre_backend_disabled(value: str | None) -> bool:
    key = (value or "").strip().lower().replace("-", "_")
    return key in {"none", "off", "skip", "skipped", "disabled", "evas_only"}


def form_dirs(root: Path) -> list[Path]:
    return sorted(path.parent for path in root.glob("tasks/**/task_release_card.json"))


def public_and_gold_paths(form_dir: Path, card: dict[str, Any]) -> list[Path]:
    artifacts = card.get("artifacts", {})
    raw_paths = [
        *artifacts.get("private_gold", []),
        *artifacts.get("public_support", []),
    ]
    return [form_dir / str(path) for path in raw_paths]


def choose_tb(form_dir: Path, card: dict[str, Any]) -> Path:
    candidates = [path for path in public_and_gold_paths(form_dir, card) if path.suffix == ".scs"]
    if not candidates:
        raise FileNotFoundError(f"no gold/support Spectre testbench for {form_dir}")
    preferred = [path for path in candidates if "_ref" in path.name]
    return (preferred or candidates)[0]


def include_names(tb_path: Path) -> list[str]:
    return AHDL_INCLUDE_RE.findall(tb_path.read_text(encoding="utf-8", errors="replace"))


def resolve_include_paths(form_dir: Path, card: dict[str, Any], tb_path: Path) -> list[Path]:
    search_dirs = [
        tb_path.parent,
        form_dir / "private" / "gold",
        form_dir / "public" / "support",
    ]
    resolved: list[Path] = []
    missing: list[str] = []
    for name in include_names(tb_path):
        match = next((directory / name for directory in search_dirs if (directory / name).exists()), None)
        if match is None:
            missing.append(name)
        else:
            resolved.append(match)
    if missing:
        raise FileNotFoundError(f"missing AHDL include files for {form_dir}: {', '.join(missing)}")
    return resolved


def choose_primary_dut(form_dir: Path, card: dict[str, Any], tb_path: Path) -> Path:
    include_paths = resolve_include_paths(form_dir, card, tb_path)
    if include_paths:
        return include_paths[0]
    candidates = [path for path in public_and_gold_paths(form_dir, card) if path.suffix == ".va"]
    if not candidates:
        raise FileNotFoundError(f"no gold/support Verilog-A DUT for {form_dir}")
    return candidates[0]


def run_one_form(
    *,
    root: Path,
    form_dir: Path,
    output_root: Path,
    bridge_repo: Path,
    cadence_cshrc: str | None,
    timeout_s: int,
    spectre_backend: str,
    spectre_mode: str,
    sui_host: str | None,
    sui_work_root: str | None,
) -> dict[str, Any]:
    from run_gold_dual_suite import (
        compare_waveforms,
        run_spectre_case,
        should_retry_spectre_upload,
    )
    from simulate_evas import (
        behavior_side_output_names,
        evaluate_behavior,
        load_v2_checks_config,
        run_case,
        validate_behavior_side_outputs,
    )

    card = load_json(form_dir / "task_release_card.json")
    task_id = str(card["id"])
    task_root = output_root / safe_component(task_id)
    evas_root = task_root / "evas"
    spectre_root = task_root / "spectre"
    tb_path = choose_tb(form_dir, card)
    dut_path = choose_primary_dut(form_dir, card, tb_path)
    include_paths = resolve_include_paths(form_dir, card, tb_path)
    checks_config = load_v2_checks_config(form_dir)
    checker_task_id = str(checks_config.get("checker_task_id") or task_id)
    notes = [
        f"gold_tb={tb_path.name}",
        f"primary_dut={dut_path.name}",
        f"checker_task_id={checker_task_id}",
    ]

    started_at = datetime.now().isoformat(timespec="seconds")
    case_t0 = time.perf_counter()

    evas_t0 = time.perf_counter()
    evas_result = run_case(
        form_dir,
        dut_path,
        tb_path,
        output_root=evas_root,
        timeout_s=timeout_s,
        task_id_override=task_id,
    )
    evas_wall_time_s = time.perf_counter() - evas_t0
    write_json(task_root / "evas_result.json", evas_result)

    side_outputs = behavior_side_output_names(checker_task_id)
    skip_spectre = spectre_backend_disabled(spectre_backend)
    if skip_spectre:
        notes.append("spectre_skipped_evas_only")
        spectre_wall_time_s = 0.0
        spectre_result = {
            "ok": None,
            "status": "SKIPPED",
            "backend": "none",
            "mode": spectre_mode,
            "reason": "spectre-backend=none",
        }
        spectre_behavior_score = None
        spectre_behavior_notes = ["spectre skipped for EVAS-only gold certification"]
    else:
        spectre_t0 = time.perf_counter()
        spectre_result = run_spectre_case(
            task_id=task_id,
            tb_path=tb_path,
            include_paths=include_paths,
            output_dir=spectre_root,
            bridge_repo=bridge_repo,
            cadence_cshrc=cadence_cshrc,
            timeout_s=timeout_s,
            side_output_files=side_outputs,
            spectre_backend=spectre_backend,
            sui_host=sui_host,
            sui_work_root=sui_work_root,
            spectre_mode=spectre_mode,
        )
        spectre_wall_time_s = time.perf_counter() - spectre_t0
        if should_retry_spectre_upload(spectre_result):
            notes.append("spectre_retry_after_upload_failure")
            retry_t0 = time.perf_counter()
            spectre_result = run_spectre_case(
                task_id=task_id,
                tb_path=tb_path,
                include_paths=include_paths,
                output_dir=spectre_root,
                bridge_repo=bridge_repo,
                cadence_cshrc=cadence_cshrc,
                timeout_s=timeout_s,
                side_output_files=side_outputs,
                spectre_backend=spectre_backend,
                sui_host=sui_host,
                sui_work_root=sui_work_root,
                spectre_mode=spectre_mode,
            )
            spectre_wall_time_s += time.perf_counter() - retry_t0

        spectre_csv = spectre_root / "tran_spectre.csv"
        if spectre_result.get("ok") and spectre_csv.exists():
            spectre_behavior_score, spectre_behavior_notes = evaluate_behavior(
                checker_task_id,
                spectre_csv,
                checks_config=checks_config,
            )
            side_output_result = validate_behavior_side_outputs(checker_task_id, spectre_root, spectre_csv)
            if side_output_result is not None:
                side_output_ok, side_output_note = side_output_result
                spectre_behavior_notes.append(side_output_note)
                if not side_output_ok:
                    spectre_behavior_score = 0.0
        else:
            spectre_behavior_score = 0.0
            spectre_behavior_notes = ["tran_spectre.csv missing or Spectre run failed"]

    evas_csv = evas_root / "tran.csv"
    spectre_csv = spectre_root / "tran_spectre.csv"
    if (
        not skip_spectre
        and evas_result.get("status") == "PASS"
        and isinstance(spectre_behavior_score, (float, int))
        and spectre_behavior_score >= 1.0
        and evas_csv.exists()
        and spectre_csv.exists()
    ):
        parity = compare_waveforms(checker_task_id, evas_csv, spectre_csv)
    elif skip_spectre:
        parity = {
            "status": "skipped",
            "reason": "spectre skipped for EVAS-only gold certification",
        }
    else:
        parity = {
            "status": "blocked",
            "reason": "prerequisites not met for waveform comparison",
        }

    if evas_result.get("status") != "PASS":
        status = "FAIL_EVAS"
    elif skip_spectre:
        status = "PASS"
    elif not spectre_result.get("ok"):
        status = "FAIL_SPECTRE"
    elif isinstance(spectre_behavior_score, (float, int)) and spectre_behavior_score < 1.0:
        status = "FAIL_SPECTRE_BEHAVIOR"
    else:
        status = "PASS"

    row = {
        "task_id": task_id,
        "status": status,
        "checker_task_id": checker_task_id,
        "form_dir": rel_or_abs(form_dir, root.parent),
        "gold_tb": rel_or_abs(tb_path, root.parent),
        "gold_includes": [rel_or_abs(path, root.parent) for path in include_paths],
        "primary_dut": rel_or_abs(dut_path, root.parent),
        "evas": {
            "status": evas_result.get("status"),
            "scores": evas_result.get("scores"),
            "notes": (evas_result.get("notes") or [])[:12],
            "result_json": rel_or_abs(task_root / "evas_result.json", root.parent),
            "csv_path": rel_or_abs(evas_csv, root.parent) if evas_csv.exists() else "",
        },
        "spectre": {
            **spectre_result,
            "behavior_score": spectre_behavior_score,
            "behavior_notes": spectre_behavior_notes,
        },
        "parity": parity,
        "timing": {
            "evas_wall_time_s": evas_wall_time_s,
            "spectre_wall_time_s": spectre_wall_time_s,
            "combined_wall_time_s": evas_wall_time_s + spectre_wall_time_s,
            "case_wall_time_s": time.perf_counter() - case_t0,
        },
        "notes": notes,
        "started_at": started_at,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
    }
    write_json(task_root / "mini_cert_result.json", row)
    return row


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--timeout-s", type=int, default=240)
    parser.add_argument("--task-id", action="append", default=[])
    parser.add_argument(
        "--bridge-repo",
        type=Path,
        default=Path(os.environ.get("VAEVAS_BRIDGE_REPO", Path(__file__).resolve().parents[4] / "iccad" / "virtuoso-bridge-lite")),
    )
    parser.add_argument("--cadence-cshrc", default=os.environ.get("VB_CADENCE_CSHRC", ""))
    parser.add_argument("--spectre-backend", default=os.environ.get("VAEVAS_SPECTRE_BACKEND", "bridge"))
    parser.add_argument("--spectre-mode", default=os.environ.get("VAEVAS_SPECTRE_MODE", "ax"))
    parser.add_argument(
        "--evas-engine",
        default=os.environ.get("VAEVAS_DEFAULT_EVAS_ENGINE", ""),
        help="Optional EVAS engine override, e.g. evas or evas2. Sets VAEVAS_DEFAULT_EVAS_ENGINE and EVAS_ENGINE.",
    )
    parser.add_argument("--sui-host", default=os.environ.get("VAEVAS_SUI_HOST", ""))
    parser.add_argument("--sui-work-root", default=os.environ.get("VAEVAS_SUI_WORK_ROOT", ""))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    repo_root = repo_root_from_v2_root(root)
    ensure_runner_import(repo_root)
    if args.evas_engine:
        os.environ["VAEVAS_DEFAULT_EVAS_ENGINE"] = args.evas_engine
        os.environ["EVAS_ENGINE"] = args.evas_engine

    selected_task_ids = set(args.task_id)
    candidates = form_dirs(root)
    if selected_task_ids:
        candidates = [
            form_dir
            for form_dir in candidates
            if str(load_json(form_dir / "task_release_card.json").get("id")) in selected_task_ids
        ]

    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now().isoformat(timespec="seconds")
    rows: list[dict[str, Any]] = []
    status_counts: dict[str, int] = {}
    errors: list[dict[str, str]] = []

    for form_dir in candidates:
        try:
            row = run_one_form(
                root=root,
                form_dir=form_dir,
                output_root=output_root,
                bridge_repo=args.bridge_repo.resolve(),
                cadence_cshrc=args.cadence_cshrc or None,
                timeout_s=args.timeout_s,
                spectre_backend=args.spectre_backend,
                spectre_mode=args.spectre_mode,
                sui_host=args.sui_host or None,
                sui_work_root=args.sui_work_root or None,
            )
        except Exception as exc:  # noqa: BLE001 - keep certification batch moving.
            task_id = str(load_json(form_dir / "task_release_card.json").get("id", form_dir.name))
            row = {
                "task_id": task_id,
                "status": "FAIL_INFRA",
                "form_dir": rel_or_abs(form_dir, root.parent),
                "error": f"{type(exc).__name__}: {str(exc)[:500]}",
            }
            errors.append({"task_id": task_id, "error": row["error"]})
        rows.append(row)
        status = str(row.get("status", "UNKNOWN"))
        status_counts[status] = status_counts.get(status, 0) + 1
        write_json(
            output_root / "summary.partial.json",
            {
                "status": "running",
                "started_at": started_at,
                "updated_at": datetime.now().isoformat(timespec="seconds"),
                "row_count": len(candidates),
                "rows_completed": len(rows),
                "status_counts": status_counts,
                "rows": rows,
                "errors": errors,
            },
        )

    summary = {
        "release": "vabench-release-v2",
        "run_kind": "gold_evas_only_cert" if spectre_backend_disabled(args.spectre_backend) else "gold_spectre_mini_cert",
        "status": "PASS" if rows and all(row.get("status") == "PASS" for row in rows) else "FAIL",
        "started_at": started_at,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "root": str(root),
        "output_root": str(output_root),
        "row_count": len(rows),
        "pass_count": sum(1 for row in rows if row.get("status") == "PASS"),
        "status_counts": status_counts,
        "evas_engine": os.environ.get("EVAS_ENGINE") or os.environ.get("VAEVAS_DEFAULT_EVAS_ENGINE", ""),
        "spectre_backend": args.spectre_backend,
        "spectre_mode": args.spectre_mode,
        "rows": rows,
        "errors": errors,
    }
    write_json(output_root / "summary.json", summary)
    partial = output_root / "summary.partial.json"
    if partial.exists():
        partial.unlink()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
