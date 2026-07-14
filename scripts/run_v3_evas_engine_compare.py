#!/usr/bin/env python3
"""Compare EVAS engine coverage and timing on a sampled v3 gold slice."""

from __future__ import annotations

import argparse
import json
import os
import random
import statistics
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNERS_DIR = REPO_ROOT / "runners"
if str(RUNNERS_DIR) not in sys.path:
    sys.path.insert(0, str(RUNNERS_DIR))

import simulate_evas  # noqa: E402

read_task_artifact_targets = simulate_evas.read_task_artifact_targets
read_task_index_id = simulate_evas.read_task_index_id
run_case = simulate_evas.run_case


def task_number(task_dir: Path) -> int | None:
    try:
        return int(task_dir.name[:3])
    except ValueError:
        return None


def resolve_case(task_dir: Path) -> tuple[Path, Path] | None:
    targets = read_task_artifact_targets(task_dir)
    if not targets:
        return None
    dut_root = task_dir / "solution"
    dut = dut_root / targets[0]
    if not dut.exists():
        fallback_candidates = sorted(dut_root.glob("*.va"))
        if len(fallback_candidates) == 1:
            dut = fallback_candidates[0]
        else:
            return None
    tb = task_dir / "test_hidden" / "hidden.scs"
    if not tb.exists():
        tb_candidates = sorted((task_dir / "test_hidden" / "tests").glob("*.scs"))
        if len(tb_candidates) == 1:
            tb = tb_candidates[0]
        else:
            return None
    return dut, tb


def eligible_tasks(root: Path) -> list[Path]:
    tasks: list[Path] = []
    for task_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        if task_number(task_dir) is None:
            continue
        if resolve_case(task_dir) is None:
            continue
        tasks.append(task_dir)
    return tasks


def select_tasks(root: Path, *, count: int, seed: int) -> list[Path]:
    tasks = eligible_tasks(root)
    if count > len(tasks):
        raise SystemExit(f"requested {count} tasks but only {len(tasks)} eligible tasks are available")
    return sorted(random.Random(seed).sample(tasks, count), key=lambda path: task_number(path) or 0)


def engine_env(label: str, main_evas_repo: Path, skeleton_repo: Path) -> dict[str, str]:
    if label == "python":
        return {
            "VAEVAS_EVAS_REPO": str(main_evas_repo),
            "VAEVAS_DEFAULT_EVAS_ENGINE": "python",
            "EVAS_ENGINE": "python",
        }
    if label == "python_rust":
        return {
            "VAEVAS_EVAS_REPO": str(main_evas_repo),
            "VAEVAS_DEFAULT_EVAS_ENGINE": "evas2",
            "EVAS_ENGINE": "evas2",
        }
    if label == "pure_rust_skeleton":
        return {
            "VAEVAS_EVAS_REPO": str(skeleton_repo),
            "VAEVAS_DEFAULT_EVAS_ENGINE": "evas2",
            "EVAS_ENGINE": "evas2",
        }
    raise SystemExit(f"unknown engine label: {label}")


def status_bucket(status: str) -> str:
    if status == "PASS":
        return "CHECKER_PASS"
    if status == "FAIL_SIM_CORRECTNESS":
        return "SIM_OK_CHECKER_FAIL"
    if status == "FAIL_DUT_COMPILE":
        return "DUT_OR_FRONTEND_FAIL"
    if status == "FAIL_TB_COMPILE":
        return "SIM_FAIL"
    return status or "UNKNOWN"


def note_brief(notes: object) -> str:
    if not isinstance(notes, list):
        return ""
    useful = []
    for item in notes:
        text = str(item)
        if text.startswith(("returncode=", "evas_engine=", "checker_config=")):
            continue
        useful.append(text)
        if len(useful) >= 3:
            break
    return "; ".join(useful)


def run_engine(label: str, tasks: list[Path], args: argparse.Namespace) -> dict[str, object]:
    # The persistent worker captures EVAS_ENGINE and VAEVAS_EVAS_REPO when it is
    # spawned, so each engine lane must get a fresh worker process.
    simulate_evas._close_persistent_evas_worker()
    os.environ.update(engine_env(label, args.main_evas_repo, args.skeleton_repo))
    if args.no_persistent_worker:
        os.environ["VAEVAS_EVAS_PERSISTENT_WORKER"] = "0"
    else:
        os.environ.pop("VAEVAS_EVAS_PERSISTENT_WORKER", None)

    rows: list[dict[str, object]] = []
    engine_start = time.perf_counter()
    for index, task_dir in enumerate(tasks, start=1):
        resolved = resolve_case(task_dir)
        if resolved is None:
            row = {
                "task": task_dir.name,
                "task_id": read_task_index_id(task_dir) or task_dir.name,
                "status": "FAIL_NO_CASE",
                "bucket": "NO_CASE",
                "wall_s": 0.0,
                "notes": ["missing solution DUT or hidden testbench"],
            }
            rows.append(row)
            print(f"[{label}] {index:02d}/{len(tasks):02d} {task_dir.name} FAIL_NO_CASE", flush=True)
            continue

        dut, tb = resolved
        start = time.perf_counter()
        result = run_case(
            task_dir,
            dut,
            tb,
            timeout_s=args.timeout,
            keep_run_dir=False,
            task_id_override=read_task_index_id(task_dir),
        )
        wall_s = time.perf_counter() - start
        status = str(result.get("status", "UNKNOWN"))
        row = {
            "task": task_dir.name,
            "task_id": result.get("task_id") or read_task_index_id(task_dir) or task_dir.name,
            "checker_task_id": result.get("checker_task_id"),
            "status": status,
            "bucket": status_bucket(status),
            "wall_s": wall_s,
            "sim_wall_s": result.get("timing_split", {}).get("evas_subprocess_wall_s"),
            "checker_wall_s": result.get("timing_split", {}).get("behavior_checker_s"),
            "scores": result.get("scores", {}),
            "notes": result.get("notes", []),
            "stdout_tail": str(result.get("stdout_tail", ""))[-1200:],
        }
        rows.append(row)
        print(
            f"[{label}] {index:02d}/{len(tasks):02d} {task_dir.name} "
            f"{status} {wall_s:.2f}s {note_brief(row['notes'])}",
            flush=True,
        )

    total_wall_s = time.perf_counter() - engine_start
    pass_count = sum(1 for row in rows if row.get("status") == "PASS")
    sim_ok_count = sum(
        1
        for row in rows
        if row.get("status") in {"PASS", "FAIL_SIM_CORRECTNESS"}
    )
    walls = [float(row["wall_s"]) for row in rows]
    result = {
        "label": label,
        "total_wall_s": total_wall_s,
        "tasks": len(rows),
        "checker_pass": pass_count,
        "sim_ok": sim_ok_count,
        "status_counts": {
            status: sum(1 for row in rows if row.get("status") == status)
            for status in sorted({str(row.get("status")) for row in rows})
        },
        "bucket_counts": {
            bucket: sum(1 for row in rows if row.get("bucket") == bucket)
            for bucket in sorted({str(row.get("bucket")) for row in rows})
        },
        "median_wall_s": statistics.median(walls) if walls else 0.0,
        "mean_wall_s": statistics.mean(walls) if walls else 0.0,
        "rows": rows,
    }
    simulate_evas._close_persistent_evas_worker()
    return result


def write_markdown(report: dict[str, object], path: Path) -> None:
    engines = report["engines"]
    assert isinstance(engines, list)
    lines = [
        "# EVAS v3 Engine Compare",
        "",
        f"- seed: `{report['seed']}`",
        f"- task_count: `{report['task_count']}`",
        f"- timeout_s: `{report['timeout_s']}`",
        f"- sample_policy: `{report['sample_policy']}`",
        "",
        "## Summary",
        "",
        "| engine | checker pass | sim ok | total wall s | median row s | status counts |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for engine in engines:
        assert isinstance(engine, dict)
        lines.append(
            "| {label} | {checker_pass}/{tasks} | {sim_ok}/{tasks} | {total:.2f} | {median:.2f} | `{counts}` |".format(
                label=engine["label"],
                checker_pass=engine["checker_pass"],
                sim_ok=engine["sim_ok"],
                tasks=engine["tasks"],
                total=float(engine["total_wall_s"]),
                median=float(engine["median_wall_s"]),
                counts=json.dumps(engine["status_counts"], sort_keys=True),
            )
        )
    lines.extend(
        [
            "",
            "## Per Task",
            "",
            "| task | python | python s | python+rust | python+rust s | pure-rust skeleton | skeleton s |",
            "| --- | --- | ---: | --- | ---: | --- | ---: |",
        ]
    )
    by_engine: dict[str, dict[str, dict[str, object]]] = {}
    for engine in engines:
        assert isinstance(engine, dict)
        by_engine[str(engine["label"])] = {
            str(row["task"]): row for row in engine["rows"] if isinstance(row, dict)
        }
    for task in report["tasks"]:
        task_name = str(task)
        py = by_engine.get("python", {}).get(task_name, {})
        pyr = by_engine.get("python_rust", {}).get(task_name, {})
        sk = by_engine.get("pure_rust_skeleton", {}).get(task_name, {})
        lines.append(
            "| {task} | {py_status} | {py_s:.2f} | {pyr_status} | {pyr_s:.2f} | {sk_status} | {sk_s:.2f} |".format(
                task=task_name,
                py_status=py.get("status", "-"),
                py_s=float(py.get("wall_s", 0.0)),
                pyr_status=pyr.get("status", "-"),
                pyr_s=float(pyr.get("wall_s", 0.0)),
                sk_status=sk.get("status", "-"),
                sk_s=float(sk.get("wall_s", 0.0)),
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=REPO_ROOT / "benchmark-vabench-release-v3" / "tasks")
    parser.add_argument("--count", type=int, default=50)
    parser.add_argument("--seed", type=int, default=20260709)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--main-evas-repo", type=Path, default=REPO_ROOT.parent / "EVAS")
    parser.add_argument(
        "--skeleton-repo",
        type=Path,
        default=REPO_ROOT.parent / "_worktrees" / "evas-pure-rust-skeleton",
    )
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument(
        "--engines",
        nargs="+",
        default=["python", "python_rust", "pure_rust_skeleton"],
        choices=["python", "python_rust", "pure_rust_skeleton"],
    )
    parser.add_argument("--no-persistent-worker", action="store_true")
    args = parser.parse_args()

    tasks = select_tasks(args.root, count=args.count, seed=args.seed)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    print("SAMPLE", " ".join(task.name for task in tasks), flush=True)

    engines = [run_engine(label, tasks, args) for label in args.engines]
    report = {
        "seed": args.seed,
        "task_count": len(tasks),
        "timeout_s": args.timeout,
        "sample_policy": "uniform random over v3 tasks with solution DUT and hidden testbench",
        "tasks": [task.name for task in tasks],
        "engines": engines,
    }
    json_path = args.out_dir / "evas_v3_engine_compare.json"
    md_path = args.out_dir / "evas_v3_engine_compare.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_markdown(report, md_path)
    print("JSON", json_path)
    print("MARKDOWN", md_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
