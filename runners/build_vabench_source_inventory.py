#!/usr/bin/env python3
"""Build source-candidate inventory for vaBench-main/heldout packs."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COVERAGE = ROOT / "analysis" / "vabench_main_coverage_table_20260508.json"
DEFAULT_OUTPUT_JSON = ROOT / "analysis" / "vabench_source_inventory_20260508.json"
DEFAULT_OUTPUT_MD = ROOT / "docs" / "VABENCH_MAIN_AUTHORING_QUEUE.md"

TASK_FORMS = ["bugfix", "spec-to-va", "end-to-end", "tb-generation"]

ALIASES: dict[str, list[str]] = {
    "offset_comparator": ["offset", "comparator", "cmp"],
    "strongarm_comparator_behavior": ["strongarm", "comparator", "reset", "priority"],
    "voltage_clamp": ["clamp", "limiter", "bounded", "saturat"],
    "precision_rectifier": ["rectifier", "diode", "absolute", "sign"],
    "peak_detector": ["peak", "detector", "hold", "maximum"],
    "track_hold_aperture": ["sample", "hold", "aperture", "track"],
    "debounce_latch": ["debounce", "latch", "threshold", "state"],
    "leaky_hold": ["leaky", "droop", "hold", "decay"],
    "edge_detector": ["edge", "pulse", "rising", "falling"],
    "one_shot_timer": ["one", "shot", "timer", "pulse"],
    "resettable_counter_divider": ["counter", "divider", "reset", "ratio"],
    "pfd_reset_race": ["pfd", "reset", "race", "lead", "lag"],
    "thermometer_dac": ["thermometer", "dac", "unit"],
    "segmented_dac": ["segmented", "dac", "glitch", "guard"],
    "sar_logic_4b": ["sar", "logic", "adc", "dac"],
    "cdac_calibration": ["cdac", "calibration", "capacitive", "dac"],
    "offset_calibration_fsm": ["offset", "calibration", "fsm", "trim"],
    "gain_trim_controller": ["gain", "trim", "calibration", "settling"],
    "lock_detector": ["lock", "detector", "pll", "streak"],
    "background_calibration_accumulator": ["background", "calibration", "accumulator"],
    "rotating_element_selector": ["rotating", "selector", "dwa", "window"],
    "barrel_pointer_window": ["barrel", "pointer", "window", "wrap"],
    "element_shuffler": ["element", "shuffle", "selector", "sequence"],
    "thermometer_decoder_guarded": ["thermometer", "decoder", "guard"],
    "first_order_lowpass": ["lowpass", "filter", "first", "order"],
    "resettable_integrator": ["integrator", "reset", "idt"],
    "slew_rate_limiter": ["slew", "rate", "limiter"],
    "vco_phase_integrator": ["vco", "phase", "integrator", "pll"],
    "settling_time_measurement_tb": ["settling", "measurement", "testbench"],
    "file_metric_writer": ["file", "metric", "fopen", "final_step"],
    "folding_adc_encoder": ["folding", "adc", "encoder"],
    "pwm_modulator": ["pwm", "modulator", "duty"],
    "phase_frequency_lock_monitor": ["phase", "frequency", "lock", "monitor"],
    "adaptive_threshold_tracker": ["adaptive", "threshold", "tracker"],
    "windowed_rms_detector": ["rms", "window", "detector"],
    "charge_pump_behavior": ["charge", "pump"],
    "sigma_delta_modulator_1st": ["sigma", "delta", "modulator"],
    "glitch_filter": ["glitch", "filter", "pulse"],
    "quadrature_phase_detector": ["quadrature", "phase", "detector"],
    "sample_rate_converter_stub": ["sample", "rate", "converter", "multi", "clock"],
    "temperature_sensor_lut": ["temperature", "sensor", "lut"],
    "noise_source_stat_tb": ["noise", "source", "stat"],
}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def _norm_tokens(text: str) -> set[str]:
    return {tok for tok in re.split(r"[^a-z0-9]+", text.lower()) if len(tok) >= 3}


def _task_records(roots: list[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for bench in roots:
        for meta_path in sorted((bench / "tasks").glob("*/meta.json")):
            task_dir = meta_path.parent
            meta = _read_json(meta_path)
            prompt = _text(task_dir / "prompt.md")
            haystack = " ".join(
                str(item)
                for item in [
                    task_dir.name,
                    meta.get("task_id"),
                    meta.get("id"),
                    meta.get("source_task_id"),
                    meta.get("core_function"),
                    meta.get("category"),
                    meta.get("mechanism_family"),
                    meta.get("source_seed"),
                    meta.get("expected_output_summary"),
                    meta.get("task_name"),
                    prompt[:4000],
                ]
                if item
            )
            records.append(
                {
                    "benchmark": bench.name,
                    "task_id": meta.get("task_id", task_dir.name),
                    "task_dir": str(task_dir.relative_to(ROOT)),
                    "task_form": meta.get("task_form") or meta.get("family") or meta.get("benchmark"),
                    "core_function": meta.get("core_function") or meta.get("category") or meta.get("mechanism_family"),
                    "source_task_id": meta.get("source_task_id") or meta.get("source_seed"),
                    "tokens": sorted(_norm_tokens(haystack)),
                }
            )
    return records


def _score(pack_id: str, record: dict[str, Any]) -> tuple[int, list[str]]:
    aliases = set(ALIASES.get(pack_id, [])) | _norm_tokens(pack_id)
    tokens = set(record["tokens"])
    hits = sorted(alias for alias in aliases if alias.lower() in tokens)
    score = len(hits)
    # Exact-ish task names are more valuable than broad prompt matches.
    joined = " ".join(tokens)
    compact_pack = pack_id.replace("_", "")
    if compact_pack in joined.replace(" ", ""):
        score += 3
        hits.append("exact_pack_compact")
    return score, hits


def _status(best_score: int) -> str:
    if best_score >= 5:
        return "source_backed"
    if best_score >= 3:
        return "adapt_existing"
    if best_score >= 1:
        return "weak_candidate"
    return "new_authoring"


def _write_md(path: Path, inventory: dict[str, Any]) -> None:
    rows = inventory["packs"]
    counts = Counter(row["source_status"] for row in rows)
    lines = [
        "# vaBench Main Authoring Queue",
        "",
        "**Date**: 2026-05-08",
        "",
        "This queue converts the coverage table into an executable authoring plan.",
        "Source candidates are heuristic matches from `benchmark-balanced` and",
        "`benchmark-v2`; they are starting points, not automatic promotion.",
        "",
        "## Summary",
        "",
        f"- Packs: `{len(rows)}`",
        f"- Planned tasks: `{sum(row['planned_tasks'] for row in rows)}`",
        f"- Source-backed: `{counts.get('source_backed', 0)}`",
        f"- Adapt existing: `{counts.get('adapt_existing', 0)}`",
        f"- Weak candidate: `{counts.get('weak_candidate', 0)}`",
        f"- New authoring: `{counts.get('new_authoring', 0)}`",
        "",
        "## Authoring Order",
        "",
        "1. Promote `source_backed` packs first, because they likely have existing gold/checker ingredients.",
        "2. Then adapt `adapt_existing` packs by rewriting prompts/checkers into four-form pack contracts.",
        "3. Treat `weak_candidate` and `new_authoring` packs as new benchmark authoring work.",
        "4. Keep all heldout packs out of skill/RAG/controller tuning.",
        "",
        "## Pack Queue",
        "",
        "| Split | Status | Pack | Mechanism | Best candidates | Next action |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    action = {
        "source_backed": "Review source contract, materialize four forms, run semantic audit.",
        "adapt_existing": "Use candidate as seed, author missing forms/checkers.",
        "weak_candidate": "Manual design required; candidate only informs mechanism.",
        "new_authoring": "Write fresh prompt/checker/gold pack from public spec.",
    }
    for row in rows:
        cand = "<br>".join(
            f"`{c['task_id']}` ({c['benchmark']}, score={c['score']}, hits={','.join(c['hits'])})"
            for c in row["candidates"][:3]
        ) or "-"
        lines.append(
            f"| `{row['split']}` | `{row['source_status']}` | `{row['pack_id']}` | {row['mechanism_family']} | {cand} | {action[row['source_status']]} |"
        )
    lines.extend([
        "",
        "## Promotion Gate",
        "",
        "Each pack must pass: four task forms, zero semantic-audit FAIL, gold strict-EVAS PASS,",
        "gold Spectre PASS, and no task-id/gold/checker-internal routing.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage-json", type=Path, default=DEFAULT_COVERAGE)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--source-bench", type=Path, action="append", default=[ROOT / "benchmark-balanced", ROOT / "benchmark-v2"])
    args = parser.parse_args()

    coverage = _read_json(args.coverage_json)
    records = _task_records([p.resolve() for p in args.source_bench])
    packs: list[dict[str, Any]] = []
    for pack in coverage["main_packs"] + coverage["heldout_packs"]:
        scored = []
        for record in records:
            score, hits = _score(pack["pack_id"], record)
            if score > 0:
                scored.append({k: v for k, v in record.items() if k != "tokens"} | {"score": score, "hits": hits})
        scored.sort(key=lambda item: (-item["score"], item["benchmark"], item["task_id"]))
        best_score = scored[0]["score"] if scored else 0
        packs.append(
            {
                **pack,
                "source_status": _status(best_score),
                "best_score": best_score,
                "candidates": scored[:8],
            }
        )

    out = {
        "date": "2026-05-08",
        "coverage_json": str(args.coverage_json),
        "source_benches": [str(p) for p in args.source_bench],
        "task_forms": TASK_FORMS,
        "packs": packs,
        "status_counts": dict(Counter(pack["source_status"] for pack in packs)),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_md(args.output_md, out)
    print(json.dumps({"packs": len(packs), "status_counts": out["status_counts"]}, indent=2))
    print(f"json={args.output_json}")
    print(f"md={args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
