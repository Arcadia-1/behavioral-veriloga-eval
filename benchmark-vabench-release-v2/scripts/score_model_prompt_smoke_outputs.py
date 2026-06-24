#!/usr/bin/env python3
"""Score vaBench v2 model-smoke responses with EVAS/checker."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any


FENCE_RE = re.compile(r"```(?:[A-Za-z0-9_.+-]+)?\s*\n(.*?)\n```", re.S)
FILENAME_RE = re.compile(r"`?([A-Za-z0-9_.+-]+\.(?:va|scs))`?")
AHDL_INCLUDE_RE = re.compile(r'^\s*ahdl_include\s+"([^"]+)"', re.M)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def ensure_runner_import(repo_root: Path) -> None:
    runners = repo_root / "runners"
    sys.path.insert(0, str(runners.resolve()))


def target_files(form_dir: Path) -> list[str]:
    card = load_json(form_dir / "task_release_card.json")
    manifest_path = form_dir / card.get("artifacts", {}).get("agent_visible_files", "agent_visible_files.json")
    manifest = load_json(manifest_path)
    return [str(item) for item in manifest.get("agent_visible", {}).get("target_files", [])]


def public_support_paths(form_dir: Path) -> list[Path]:
    card = load_json(form_dir / "task_release_card.json")
    return [form_dir / str(item) for item in card.get("artifacts", {}).get("public_support", [])]


def extract_code_blocks(response_text: str) -> list[str]:
    blocks = [match.group(1).strip() for match in FENCE_RE.finditer(response_text)]
    if blocks:
        return blocks
    stripped = response_text.strip()
    return [stripped] if stripped else []


def line_before(text: str, start: int) -> str:
    prefix = text[:start].rstrip()
    if not prefix:
        return ""
    return prefix.splitlines()[-1].strip()


def extract_named_blocks(response_text: str) -> dict[str, str]:
    named: dict[str, str] = {}
    for match in FENCE_RE.finditer(response_text):
        preceding = line_before(response_text, match.start())
        filename_match = FILENAME_RE.search(preceding)
        if filename_match:
            named[filename_match.group(1)] = match.group(1).strip()
    return named


def fallback_name_for_block(block: str, target: str) -> str:
    if target.endswith(".scs"):
        return target
    module_match = re.search(r"\bmodule\s+([A-Za-z_][A-Za-z0-9_]*)", block)
    if module_match and target.endswith(".va"):
        return target
    return target


def materialize_candidate(response_text: str, targets: list[str], sample_dir: Path) -> dict[str, Any]:
    sample_dir.mkdir(parents=True, exist_ok=True)
    named = extract_named_blocks(response_text)
    blocks = extract_code_blocks(response_text)
    saved: dict[str, str] = {}
    used_blocks: set[int] = set()

    for target in targets:
        if target in named:
            path = sample_dir / Path(target).name
            path.write_text(named[target].strip() + "\n", encoding="utf-8")
            saved[Path(target).name] = str(path)

    for target in targets:
        name = Path(target).name
        if name in saved:
            continue
        for idx, block in enumerate(blocks):
            if idx in used_blocks:
                continue
            looks_like_scs = "simulator lang=spectre" in block.lower() or re.search(r"(?m)^\s*tran\s+", block)
            looks_like_va = re.search(r"\bmodule\s+[A-Za-z_][A-Za-z0-9_]*", block) is not None
            if (target.endswith(".scs") and looks_like_scs) or (target.endswith(".va") and looks_like_va):
                path = sample_dir / fallback_name_for_block(block, target)
                path.write_text(block.strip() + "\n", encoding="utf-8")
                saved[name] = str(path)
                used_blocks.add(idx)
                break

    missing = [Path(target).name for target in targets if Path(target).name not in saved]
    return {"saved": saved, "missing": missing, "block_count": len(blocks), "named_count": len(named)}


def copy_public_support(form_dir: Path, sample_dir: Path, saved: dict[str, str]) -> None:
    for source in public_support_paths(form_dir):
        if not source.exists():
            continue
        destination = sample_dir / source.name
        if destination.name in saved:
            continue
        shutil.copy2(source, destination)


def choose_tb(sample_dir: Path, form_dir: Path, targets: list[str]) -> Path | None:
    for target in targets:
        if target.endswith(".scs") and (sample_dir / Path(target).name).exists():
            return sample_dir / Path(target).name
    for source in public_support_paths(form_dir):
        if source.suffix == ".scs" and source.exists():
            return source
    return None


def choose_dut(sample_dir: Path, form_dir: Path, tb_path: Path, targets: list[str]) -> Path | None:
    includes = AHDL_INCLUDE_RE.findall(tb_path.read_text(encoding="utf-8", errors="ignore"))
    for include in includes:
        name = Path(include).name
        candidate = sample_dir / name
        if candidate.exists():
            return candidate
        for support in public_support_paths(form_dir):
            if support.name == name and support.exists():
                return support
    for target in targets:
        candidate = sample_dir / Path(target).name
        if candidate.suffix == ".va" and candidate.exists():
            return candidate
    return None


def resolve_candidate_include_paths(sample_dir: Path, form_dir: Path, tb_path: Path) -> list[Path]:
    search_dirs = [
        sample_dir,
        tb_path.parent,
        form_dir / "public" / "support",
    ]
    resolved: list[Path] = []
    missing: list[str] = []
    for include in AHDL_INCLUDE_RE.findall(tb_path.read_text(encoding="utf-8", errors="replace")):
        match = next((directory / Path(include).name for directory in search_dirs if (directory / Path(include).name).exists()), None)
        if match is None:
            missing.append(include)
        else:
            resolved.append(match)
    if missing:
        raise FileNotFoundError(f"missing candidate AHDL includes: {', '.join(missing)}")
    return resolved


def run_spectre_judge(
    *,
    repo_root: Path,
    form_dir: Path,
    task_id: str,
    sample_dir: Path,
    tb_path: Path,
    output_root: Path,
    bridge_repo: Path,
    cadence_cshrc: str | None,
    timeout_s: int,
    spectre_backend: str,
    spectre_mode: str,
    sui_host: str | None,
    sui_work_root: str | None,
) -> dict[str, Any]:
    ensure_runner_import(repo_root)
    from run_gold_dual_suite import run_spectre_case, should_retry_spectre_upload  # noqa: PLC0415
    from simulate_evas import (  # noqa: PLC0415
        behavior_side_output_names,
        evaluate_behavior,
        load_v2_checks_config,
        validate_behavior_side_outputs,
    )

    checks_config = load_v2_checks_config(form_dir)
    checker_task_id = str(checks_config.get("checker_task_id") or task_id)
    include_paths = resolve_candidate_include_paths(sample_dir, form_dir, tb_path)
    side_outputs = behavior_side_output_names(checker_task_id)
    started = time.perf_counter()
    spectre_result = run_spectre_case(
        task_id=task_id,
        tb_path=tb_path,
        include_paths=include_paths,
        output_dir=output_root,
        bridge_repo=bridge_repo,
        cadence_cshrc=cadence_cshrc,
        timeout_s=timeout_s,
        side_output_files=side_outputs,
        spectre_backend=spectre_backend,
        sui_host=sui_host,
        sui_work_root=sui_work_root,
        spectre_mode=spectre_mode,
    )
    if should_retry_spectre_upload(spectre_result):
        spectre_result = run_spectre_case(
            task_id=task_id,
            tb_path=tb_path,
            include_paths=include_paths,
            output_dir=output_root,
            bridge_repo=bridge_repo,
            cadence_cshrc=cadence_cshrc,
            timeout_s=timeout_s,
            side_output_files=side_outputs,
            spectre_backend=spectre_backend,
            sui_host=sui_host,
            sui_work_root=sui_work_root,
            spectre_mode=spectre_mode,
        )
    spectre_csv = output_root / "tran_spectre.csv"
    if spectre_result.get("ok") and spectre_csv.exists():
        behavior_score, behavior_notes = evaluate_behavior(
            checker_task_id,
            spectre_csv,
            checks_config=checks_config,
        )
        side_output_result = validate_behavior_side_outputs(checker_task_id, output_root, spectre_csv)
        if side_output_result is not None:
            side_output_ok, side_output_note = side_output_result
            behavior_notes.append(side_output_note)
            if not side_output_ok:
                behavior_score = 0.0
    else:
        behavior_score = 0.0
        behavior_notes = ["tran_spectre.csv missing or Spectre run failed"]
    return {
        "status": "PASS" if spectre_result.get("ok") and behavior_score >= 1.0 else "FAIL",
        "checker_task_id": checker_task_id,
        "include_paths": [str(path) for path in include_paths],
        "spectre": spectre_result,
        "behavior_score": behavior_score,
        "behavior_notes": behavior_notes,
        "wall_time_s": time.perf_counter() - started,
    }


def score_row(
    root: Path,
    repo_root: Path,
    row: dict[str, Any],
    input_root: Path,
    output_root: Path,
    *,
    spectre: bool,
    bridge_repo: Path,
    cadence_cshrc: str | None,
    timeout_s: int,
    spectre_backend: str,
    spectre_mode: str,
    sui_host: str | None,
    sui_work_root: str | None,
) -> dict[str, Any]:
    ensure_runner_import(repo_root)
    from simulate_evas import run_case  # noqa: PLC0415

    task_id = str(row["task_id"])
    manifest_path = root / row["manifest"]
    form_dir = manifest_path.parent
    response_path = Path(row.get("response_path", ""))
    if not response_path.exists():
        return {**row, "score_status": "FAIL_EXTRACTION", "score_notes": ["missing_response_path"]}

    task_output = output_root / task_id.replace(":", "__")
    sample_dir = task_output / "candidate"
    targets = target_files(form_dir)
    extraction = materialize_candidate(response_path.read_text(encoding="utf-8"), targets, sample_dir)
    copy_public_support(form_dir, sample_dir, extraction["saved"])

    if extraction["missing"]:
        return {
            **row,
            "score_status": "FAIL_EXTRACTION",
            "target_files": targets,
            "extraction": extraction,
            "score_notes": [f"missing_targets={','.join(extraction['missing'])}"],
        }

    tb_path = choose_tb(sample_dir, form_dir, targets)
    if tb_path is None:
        return {
            **row,
            "score_status": "FAIL_EXTRACTION",
            "target_files": targets,
            "extraction": extraction,
            "score_notes": ["no_testbench_available"],
        }

    dut_path = choose_dut(sample_dir, form_dir, tb_path, targets)
    if dut_path is None:
        return {
            **row,
            "score_status": "FAIL_EXTRACTION",
            "target_files": targets,
            "extraction": extraction,
            "score_notes": ["no_dut_available"],
        }

    result = run_case(
        form_dir,
        dut_path,
        tb_path,
        output_root=task_output / "evas",
        timeout_s=timeout_s,
        task_id_override=task_id,
    )
    write_json(task_output / "evas_result.json", result)
    notes = result.get("notes") or result.get("evas_notes") or []
    scored = {
        **row,
        "score_status": result.get("status"),
        "final_status": result.get("status"),
        "checker_task_id": result.get("checker_task_id"),
        "scores": result.get("scores"),
        "target_files": targets,
        "extraction": extraction,
        "candidate_dir": str(sample_dir),
        "score_artifact": str(task_output / "evas_result.json"),
        "score_notes": notes[:12],
        "stdout_tail": (result.get("stdout_tail") or "")[-1600:],
    }
    if not spectre:
        return scored

    try:
        spectre_result = run_spectre_judge(
            repo_root=repo_root,
            form_dir=form_dir,
            task_id=task_id,
            sample_dir=sample_dir,
            tb_path=tb_path,
            output_root=task_output / "spectre",
            bridge_repo=bridge_repo,
            cadence_cshrc=cadence_cshrc,
            timeout_s=timeout_s,
            spectre_backend=spectre_backend,
            spectre_mode=spectre_mode,
            sui_host=sui_host,
            sui_work_root=sui_work_root,
        )
    except Exception as exc:  # noqa: BLE001 - keep model scoring batch moving.
        spectre_result = {
            "status": "FAIL_INFRA",
            "error": f"{type(exc).__name__}: {str(exc)[:500]}",
            "behavior_score": 0.0,
            "behavior_notes": ["spectre_judge_exception"],
        }
    write_json(task_output / "spectre_result.json", spectre_result)
    final_status = "PASS" if result.get("status") == "PASS" and spectre_result.get("status") == "PASS" else "FAIL"
    scored.update(
        {
            "final_status": final_status,
            "spectre_status": spectre_result.get("status"),
            "spectre_behavior_score": spectre_result.get("behavior_score"),
            "spectre_artifact": str(task_output / "spectre_result.json"),
            "spectre_notes": spectre_result.get("behavior_notes", [])[:12],
        }
    )
    return scored


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--timeout-s", type=int, default=180)
    parser.add_argument("--spectre", action="store_true", help="also run Spectre final judge on materialized candidates")
    parser.add_argument(
        "--bridge-repo",
        type=Path,
        default=Path(os.environ.get("VAEVAS_BRIDGE_REPO", Path(__file__).resolve().parents[4] / "iccad" / "virtuoso-bridge-lite")),
    )
    parser.add_argument("--cadence-cshrc", default=os.environ.get("VB_CADENCE_CSHRC", ""))
    parser.add_argument("--spectre-backend", default=os.environ.get("VAEVAS_SPECTRE_BACKEND", "bridge"))
    parser.add_argument("--spectre-mode", default=os.environ.get("VAEVAS_SPECTRE_MODE", "ax"))
    parser.add_argument("--sui-host", default=os.environ.get("VAEVAS_SUI_HOST", ""))
    parser.add_argument("--sui-work-root", default=os.environ.get("VAEVAS_SUI_WORK_ROOT", ""))
    args = parser.parse_args()

    summary = load_json(args.input_root / "summary.json")
    repo_root = args.root.resolve().parent
    rows = [
        score_row(
            args.root,
            repo_root,
            row,
            args.input_root,
            args.output_root,
            spectre=args.spectre,
            bridge_repo=args.bridge_repo.resolve(),
            cadence_cshrc=args.cadence_cshrc or None,
            timeout_s=args.timeout_s,
            spectre_backend=args.spectre_backend,
            spectre_mode=args.spectre_mode,
            sui_host=args.sui_host or None,
            sui_work_root=args.sui_work_root or None,
        )
        for row in summary.get("rows", [])
    ]
    payload = {
        "release": "vabench-release-v2",
        "model": summary.get("model"),
        "input_root": str(args.input_root),
        "output_root": str(args.output_root),
        "spectre_enabled": args.spectre,
        "spectre_backend": args.spectre_backend if args.spectre else "",
        "spectre_mode": args.spectre_mode if args.spectre else "",
        "row_count": len(rows),
        "pass_count": sum(1 for row in rows if row.get("final_status") == "PASS"),
        "status_counts": {},
        "rows": rows,
    }
    for row in rows:
        status = str(row.get("final_status") or row.get("score_status"))
        payload["status_counts"][status] = payload["status_counts"].get(status, 0) + 1
    payload["status"] = "PASS" if payload["pass_count"] == len(rows) else "FAIL"
    write_json(args.output_root / "summary.json", payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
