#!/usr/bin/env python3
"""Extract a structured repair trace index from Main120 C/S1/S2/T1 artifacts.

The extractor is intentionally permissive: it indexes whatever metadata is
available and records warnings instead of failing on missing runs or partial
schemas. Output is a JSON object plus an optional JSONL rows file.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

RUN_CONFIGS = {
    "C": {
        "label": "main120-C",
        "summary": "analysis/main120_C_compile_loop_mimo_v25_pro_20260509.json",
        "strategy": "compile_loop",
        "tool": "adaptive-evas-repair-v0",
        "kind": "summary_rows",
    },
    "S1": {
        "label": "main120-S1",
        "summary": "analysis/main120_S1_compile_skill_prompt_mimo_v25_pro_20260509.json",
        "strategy": "compile_skill_prompt",
        "tool": "adaptive-evas-repair-v0+compile_skills",
        "kind": "summary_rows",
    },
    "S2": {
        "label": "main120-S2",
        "manifest": "generated-main120-S2-compile-skill-accept-mimo-v2.5-pro-20260509/cultra_manifest.json",
        "strategy": "compile_skill_accept",
        "tool": "C-ULTRA acceptor",
        "kind": "cultra_manifest",
    },
    "T1": {
        "label": "main120-T1",
        "summary": "analysis/main120_T1_llm_tool_controller_smoke_mimo_v25_pro_20260509.json",
        "strategy": "llm_tool_controller_smoke",
        "tool": "adaptive-evas-repair-v0+tool_controller",
        "kind": "summary_rows",
    },
}

RESULT_ROOTS = {
    "C": {
        "evas": "results/main120-C-maintained-evas-mimo-v2.5-pro-20260509/summary.json",
        "spectre": "results/main120-C-spectre-mimo-v2.5-pro-20260509/summary.json",
    },
    "S1": {
        "evas": "results/main120-S1-maintained-evas-mimo-v2.5-pro-20260509/summary.json",
        "spectre": "results/main120-S1-spectre-mimo-v2.5-pro-20260509/summary.json",
    },
    "S2": {
        "evas": "results/main120-S2-maintained-evas-mimo-v2.5-pro-20260509/summary.json",
        "spectre": "results/main120-S2-spectre-mimo-v2.5-pro-20260509/summary.json",
    },
    "T1": {
        "spectre": "results/main120-T1-smoke-spectre-mimo-v2.5-pro-20260509/summary.json",
    },
}

STATUS_TO_FAMILY = {
    "PASS": "pass",
    "FAIL_DUT_COMPILE": "dut_compile",
    "FAIL_TB_COMPILE": "tb_compile",
    "FAIL_SIM_CORRECTNESS": "behavior",
    "FAIL_INFRA": "infra",
}


def load_json(path: Path, warnings: list[str]) -> Any | None:
    if not path.exists():
        warnings.append(f"missing_json:{path}")
        return None
    try:
        with path.open() as fh:
            return json.load(fh)
    except Exception as exc:  # pragma: no cover - defensive diagnostics path
        warnings.append(f"bad_json:{path}:{type(exc).__name__}:{exc}")
        return None


def rel(path: Any, root: Path) -> str | None:
    if not path:
        return None
    try:
        p = Path(path)
        if not p.is_absolute():
            p = root / p
        return str(p.relative_to(root))
    except Exception:
        return str(path)


def num(value: Any) -> int | float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    return None


def short_text(value: Any, limit: int = 240) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return text if len(text) <= limit else text[: limit - 3] + "..."


def status_family(status: Any) -> str | None:
    if not status:
        return None
    return STATUS_TO_FAMILY.get(str(status), str(status).lower())


def score_delta(before: dict[str, Any] | None, after: dict[str, Any] | None) -> dict[str, Any]:
    out: dict[str, Any] = {}
    before = before or {}
    after = after or {}
    for key in sorted(set(before) | set(after)):
        b = num(before.get(key))
        a = num(after.get(key))
        if b is not None or a is not None:
            out[key] = {"before": b, "after": a, "delta": (a - b) if a is not None and b is not None else None}
    return out


def summary_status_map(summary: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(summary, dict):
        return {}
    backend = summary.get("backend")
    payload = summary.get(backend) if backend else None
    if not isinstance(payload, dict):
        payload = summary.get("evas") or summary.get("spectre") or summary
    out: dict[str, dict[str, Any]] = {}
    for task_id in payload.get("pass_tasks", []) if isinstance(payload, dict) else []:
        out[str(task_id)] = {"status": "PASS", "notes": []}
    for item in payload.get("fail_tasks", []) if isinstance(payload, dict) else []:
        if isinstance(item, dict) and item.get("task_id"):
            out[str(item["task_id"])] = {"status": item.get("status"), "notes": item.get("notes", [])}
    return out


def load_result_maps(root: Path, warnings: list[str]) -> dict[str, dict[str, dict[str, Any]]]:
    result_maps: dict[str, dict[str, dict[str, Any]]] = {}
    for run, backends in RESULT_ROOTS.items():
        result_maps[run] = {}
        for backend, summary_rel in backends.items():
            summary = load_json(root / summary_rel, warnings)
            result_maps[run][backend] = summary_status_map(summary)
    return result_maps


def result_enrichment(run: str, task_id: str, result_maps: dict[str, dict[str, dict[str, Any]]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for backend in ("evas", "spectre"):
        item = result_maps.get(run, {}).get(backend, {}).get(task_id)
        if item:
            out[f"{backend}_status"] = item.get("status")
            out[f"{backend}_failure_family"] = status_family(item.get("status"))
            out[f"{backend}_notes"] = item.get("notes", [])[:8] if isinstance(item.get("notes"), list) else []
    evas = out.get("evas_status")
    spectre = out.get("spectre_status")
    if evas or spectre:
        out["evas_spectre_delta"] = {
            "status_match": bool(evas and spectre and evas == spectre) if evas and spectre else None,
            "evas_status": evas,
            "spectre_status": spectre,
            "pass_delta": (spectre == "PASS") - (evas == "PASS") if evas and spectre else None,
        }
    return out


def task_meta(row: dict[str, Any] | None, task_id: str) -> dict[str, Any]:
    row = row or {}
    return {
        "task_id": task_id,
        "family": row.get("family") or row.get("task_form"),
        "task_form": row.get("task_form"),
        "core_function": row.get("core_function"),
        "source_collection": row.get("source_collection"),
        "benchmark_split": row.get("benchmark_split"),
        "sample_idx": row.get("sample_idx"),
        "model": row.get("model") or row.get("model_id") or row.get("model_slug"),
        "provider": row.get("provider"),
        "reasoning_mode": row.get("reasoning_mode"),
    }


def token_time(meta: dict[str, Any], row: dict[str, Any] | None = None) -> dict[str, Any]:
    row = row or {}
    keys = [
        "input_tokens",
        "output_tokens",
        "reasoning_tokens",
        "cached_input_tokens",
        "api_elapsed_s",
        "task_elapsed_s",
        "api_call_count",
        "repair_input_tokens",
        "repair_output_tokens",
        "repair_api_elapsed_s",
        "plan_input_tokens",
        "plan_output_tokens",
        "plan_api_elapsed_s",
    ]
    return {k: meta.get(k, row.get(k)) for k in keys if meta.get(k, row.get(k)) is not None}


def infer_edit_summary(meta: dict[str, Any], round_meta: dict[str, Any] | None = None) -> dict[str, Any]:
    source = round_meta or meta
    plan = source.get("compile_plan") if isinstance(source.get("compile_plan"), dict) else {}
    step = plan.get("current_step") if isinstance(plan.get("current_step"), dict) else {}
    return {
        "root_cause": short_text(plan.get("root_cause")),
        "strategy": step.get("strategy"),
        "goal": short_text(step.get("goal")),
        "edit_scope": step.get("edit_scope") if isinstance(step.get("edit_scope"), list) else [],
        "expected_validation_delta": step.get("expected_validation_delta") if isinstance(step.get("expected_validation_delta"), list) else [],
        "saved_files": source.get("saved_files", []) if isinstance(source.get("saved_files"), list) else [],
        "materialized_syntax_edits": meta.get("materialized_syntax_edits", []) if isinstance(meta.get("materialized_syntax_edits"), list) else [],
        "materialized_vector_unroll_edits": meta.get("materialized_vector_unroll_edits", []) if isinstance(meta.get("materialized_vector_unroll_edits"), list) else [],
        "vector_unroll_guard_edits": source.get("vector_unroll_guard_edits", []) if isinstance(source.get("vector_unroll_guard_edits"), list) else [],
    }


def round_meta_for(root: Path, meta: dict[str, Any], round_no: Any, warnings: list[str]) -> dict[str, Any] | None:
    files = meta.get("repair_round_meta_files")
    if not isinstance(files, list):
        return None
    for item in files:
        if f"adaptive_round{round_no}/" in str(item):
            data = load_json(root / str(item), warnings)
            return data if isinstance(data, dict) else None
    return None


def read_meta(root: Path, path: Any, warnings: list[str]) -> dict[str, Any]:
    if not path:
        return {}
    p = Path(str(path))
    if not p.is_absolute():
        p = root / p
    data = load_json(p, warnings)
    return data if isinstance(data, dict) else {}


def initial_candidate(meta: dict[str, Any]) -> dict[str, Any]:
    candidates = meta.get("initial_candidates")
    if isinstance(candidates, list) and candidates:
        first = candidates[0] if isinstance(candidates[0], dict) else {}
        return first
    return {}


def accepted_label(before_status: Any, after_status: Any, before_scores: Any, after_scores: Any, progress: Any = None) -> str | None:
    if progress == "improved":
        return "accepted"
    if progress == "regressed":
        return "rejected"
    if after_status == "PASS" and before_status != "PASS":
        return "accepted"
    bd = score_delta(before_scores if isinstance(before_scores, dict) else {}, after_scores if isinstance(after_scores, dict) else {})
    weighted = bd.get("weighted_total", {}).get("delta") if isinstance(bd.get("weighted_total"), dict) else None
    if weighted is not None:
        if weighted > 0:
            return "accepted"
        if weighted < 0:
            return "rejected"
    return None


def extract_summary_run(root: Path, run: str, config: dict[str, Any], result_maps: dict[str, Any], warnings: list[str]) -> list[dict[str, Any]]:
    summary = load_json(root / str(config["summary"]), warnings)
    if not isinstance(summary, dict):
        return []
    rows = summary.get("rows", [])
    if not isinstance(rows, list):
        warnings.append(f"bad_rows:{config['summary']}")
        return []
    out: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict) or not row.get("task_id"):
            continue
        task_id = str(row["task_id"])
        meta = read_meta(root, row.get("meta_path"), warnings)
        initial = initial_candidate(meta)
        history = meta.get("history") if isinstance(meta.get("history"), list) else []
        after_status = meta.get("best_status") or row.get("status")
        before_status = initial.get("status")
        before_scores = initial.get("scores") if isinstance(initial.get("scores"), dict) else {}
        after_scores = meta.get("best_scores") if isinstance(meta.get("best_scores"), dict) else {}
        if history:
            last = history[-1] if isinstance(history[-1], dict) else {}
            after_status = last.get("status", after_status)
            after_scores = last.get("scores", after_scores)
        base = {
            **task_meta(row, task_id),
            "source_run": run,
            "source_run_label": config["label"],
            "tool": config["tool"],
            "strategy": config["strategy"],
            "trace_type": "adaptive_repair" if history else "selected_or_generated",
            "status_before": before_status,
            "failure_family_before": status_family(before_status),
            "status_after": after_status,
            "failure_family_after": status_family(after_status),
            "accepted_rejected": accepted_label(before_status, after_status, before_scores, after_scores),
            "score_delta": score_delta(before_scores, after_scores),
            "repair_round_count": meta.get("repair_round_count", len(history)),
            "selected_sample": meta.get("selected_sample"),
            "meta_path": rel(row.get("meta_path"), root),
            "rounds": [],
            "token_time": token_time(meta, row),
            "edit_summary": infer_edit_summary(meta),
        }
        base.update(result_enrichment(run, task_id, result_maps))
        round_rows = []
        prior_status = before_status
        prior_scores = before_scores
        for h in history:
            if not isinstance(h, dict):
                continue
            rno = h.get("round")
            rmeta = round_meta_for(root, meta, rno, warnings)
            rscores = h.get("scores") if isinstance(h.get("scores"), dict) else {}
            round_rows.append(
                {
                    "round": rno,
                    "repair_layer": h.get("repair_layer"),
                    "result_layer": h.get("result_layer"),
                    "status_before": prior_status,
                    "status_after": h.get("status"),
                    "failure_family_after": status_family(h.get("status")),
                    "failure_subtype": h.get("failure_subtype"),
                    "progress_label": h.get("progress_label"),
                    "progress_summary": h.get("progress_summary"),
                    "accepted_rejected": accepted_label(prior_status, h.get("status"), prior_scores, rscores, h.get("progress_label")),
                    "score_delta": score_delta(prior_scores, rscores),
                    "compile_plan_parse_status": h.get("compile_plan_parse_status"),
                    "concrete_diagnostics": h.get("concrete_diagnostics", [])[:8] if isinstance(h.get("concrete_diagnostics"), list) else [],
                    "evas_notes": h.get("evas_notes", [])[:10] if isinstance(h.get("evas_notes"), list) else [],
                    "metrics": h.get("metrics", {}) if isinstance(h.get("metrics"), dict) else {},
                    "edit_summary": infer_edit_summary(meta, rmeta or h),
                    "token_time": token_time(rmeta or {}, {}),
                }
            )
            prior_status = h.get("status", prior_status)
            prior_scores = rscores or prior_scores
        base["rounds"] = round_rows
        out.append(base)
    return out


def extract_s2(root: Path, config: dict[str, Any], result_maps: dict[str, Any], warnings: list[str]) -> list[dict[str, Any]]:
    manifest = load_json(root / str(config["manifest"]), warnings)
    if not isinstance(manifest, dict):
        return []
    tasks = manifest.get("tasks")
    if not isinstance(tasks, dict):
        warnings.append(f"bad_tasks:{config['manifest']}")
        return []
    generated_dir = Path(manifest.get("output_generated_dir") or root / "generated-main120-S2-compile-skill-accept-mimo-v2.5-pro-20260509")
    out: list[dict[str, Any]] = []
    for task_id, item in sorted(tasks.items()):
        if not isinstance(item, dict):
            continue
        meta_path = generated_dir / str(manifest.get("model", "mimo-v2.5-pro")) / task_id / f"sample_{manifest.get('sample_idx', 0)}" / "generation_meta.json"
        meta = read_meta(root, meta_path, warnings)
        actions = item.get("actions") if isinstance(item.get("actions"), list) else []
        before_status = item.get("source_status")
        after_status = item.get("final_status") or meta.get("best_status")
        before_scores = {}
        after_scores = {}
        round_rows = []
        for idx, action in enumerate(actions, 1):
            if not isinstance(action, dict):
                continue
            accepted = action.get("accepted")
            label = "accepted" if accepted is True else "rejected" if accepted is False else None
            round_rows.append(
                {
                    "round": action.get("round", idx),
                    "repair_layer": action.get("repair_layer") or action.get("layer"),
                    "status_before": action.get("source_status", before_status),
                    "status_after": action.get("status") or action.get("final_status"),
                    "accepted_rejected": label,
                    "action": action,
                }
            )
        row = {
            "task_id": task_id,
            "family": None,
            "task_form": None,
            "core_function": None,
            "source_collection": None,
            "benchmark_split": "benchmark-vabench-main-v1",
            "sample_idx": manifest.get("sample_idx"),
            "model": manifest.get("model"),
            "provider": None,
            "reasoning_mode": None,
            "source_run": "S2",
            "source_run_label": config["label"],
            "tool": config["tool"],
            "strategy": config["strategy"],
            "trace_type": "accepted_action_manifest",
            "status_before": before_status,
            "failure_family_before": status_family(before_status),
            "status_after": after_status,
            "failure_family_after": status_family(after_status),
            "accepted_rejected": "accepted" if actions else None,
            "score_delta": score_delta(before_scores, after_scores),
            "repair_round_count": len(actions) or meta.get("repair_round_count"),
            "selected_sample": meta.get("selected_sample"),
            "meta_path": rel(meta_path, root),
            "rounds": round_rows,
            "token_time": token_time(meta),
            "edit_summary": infer_edit_summary(meta),
            "manifest_entry": item,
        }
        row.update(result_enrichment("S2", task_id, result_maps))
        out.append(row)
    return out


def flatten_rows(entries: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    flat = []
    for entry in entries:
        shallow = {k: v for k, v in entry.items() if k not in {"rounds", "manifest_entry"}}
        flat.append({**shallow, "record_type": "trace"})
        for round_row in entry.get("rounds", []):
            flat.append(
                {
                    "record_type": "round",
                    "task_id": entry.get("task_id"),
                    "source_run": entry.get("source_run"),
                    "source_run_label": entry.get("source_run_label"),
                    **round_row,
                }
            )
    return flat


def build_counts(entries: list[dict[str, Any]], warnings: list[str]) -> dict[str, Any]:
    by_run = Counter(e.get("source_run") for e in entries)
    by_after = Counter(e.get("status_after") or "UNKNOWN" for e in entries)
    by_before_after = Counter(f"{e.get('status_before') or 'UNKNOWN'}->{e.get('status_after') or 'UNKNOWN'}" for e in entries)
    accepted = Counter(e.get("accepted_rejected") or "unknown" for e in entries)
    rounds_by_run = Counter()
    for e in entries:
        rounds_by_run[e.get("source_run")] += len(e.get("rounds", []))
    return {
        "trace_entries": len(entries),
        "tasks": len({e.get("task_id") for e in entries}),
        "by_run": dict(sorted(by_run.items())),
        "rounds_by_run": dict(sorted(rounds_by_run.items())),
        "status_after": dict(sorted(by_after.items())),
        "status_transition": dict(sorted(by_before_after.items())),
        "accepted_rejected": dict(sorted(accepted.items())),
        "warnings": len(warnings),
    }


def default_output(root: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    return root / "analysis" / f"main120_repair_trace_index_{stamp}.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="behavioral-veriloga-eval root")
    parser.add_argument("--runs", default="C,S1,S2,T1", help="comma-separated run keys to index")
    parser.add_argument("--output", type=Path, default=None, help="JSON output path")
    parser.add_argument("--jsonl-output", type=Path, default=None, help="optional flattened JSONL output path")
    parser.add_argument("--no-jsonl", action="store_true", help="do not write flattened JSONL")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    warnings: list[str] = []
    result_maps = load_result_maps(root, warnings)
    requested = [r.strip() for r in args.runs.split(",") if r.strip()]
    entries: list[dict[str, Any]] = []
    for run in requested:
        config = RUN_CONFIGS.get(run)
        if not config:
            warnings.append(f"unknown_run:{run}")
            continue
        if config["kind"] == "cultra_manifest":
            entries.extend(extract_s2(root, config, result_maps, warnings))
        else:
            entries.extend(extract_summary_run(root, run, config, result_maps, warnings))
    entries.sort(key=lambda e: (str(e.get("task_id")), str(e.get("source_run"))))
    output = (args.output or default_output(root)).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    artifact = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "runs": requested,
        "counts": build_counts(entries, warnings),
        "warnings": warnings,
        "entries": entries,
    }
    with output.open("w") as fh:
        json.dump(artifact, fh, indent=2, sort_keys=True)
        fh.write("\n")
    jsonl_output = args.jsonl_output
    if jsonl_output is None and not args.no_jsonl:
        jsonl_output = output.with_suffix(".jsonl")
    if jsonl_output and not args.no_jsonl:
        jsonl_output = jsonl_output.resolve()
        jsonl_output.parent.mkdir(parents=True, exist_ok=True)
        with jsonl_output.open("w") as fh:
            for row in flatten_rows(entries):
                fh.write(json.dumps(row, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), "jsonl_output": str(jsonl_output) if jsonl_output and not args.no_jsonl else None, "counts": artifact["counts"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
