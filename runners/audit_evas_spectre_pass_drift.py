#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from main120_stable_checks import evaluate_main120_stable_check


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVAS_ROOT = ROOT / "results/vabench-main-v1-main120-gold-evas-2026-05-08"
DEFAULT_SPECTRE_ROOT = ROOT / "results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08"
FORM_RE = re.compile(r"_(dut|tb|bugfix|e2e)$")
NUM_RE = re.compile(r"[-+]?(?:\d+\.\d+|\d+|\.\d+)(?:[eE][-+]?\d+)?")


CLASS_OVERRIDES: dict[str, dict[str, str]] = {
    "vbm1_vco_phase_integrator": {
        "class": "resolved_evas_startup_semantics",
        "priority": "P0-resolved",
        "action": "keep EVAS timer(0)+transition regression; regenerate gold EVAS evidence",
        "reason": "EVAS historically saved an artificial t=0 transition ramp; fixed by initial-condition transition semantics.",
    },
    "vbm1_strongarm_comparator_behavior": {
        "class": "stop_time_source_edge_boundary",
        "priority": "P1-benchmark",
        "action": "move the benchmark stop time away from the clock falling edge or add an explicit final-boundary regression",
        "reason": "The final saved point lands on a source transition boundary; EVAS and Spectre expose different endpoint samples while the behavior windows pass.",
    },
    "vbm1_barrel_pointer_window": {
        "class": "sample_count_checker_drift",
        "priority": "P1-checker",
        "action": "replace raw sample-count checks with time-weighted fractions or edge/state sequence checks",
        "reason": "The logical state sequence matches, but row-count-sensitive checker summaries differ across simulator sampling grids.",
    },
    "vbm1_element_shuffler": {
        "class": "sample_count_checker_drift",
        "priority": "P1-checker",
        "action": "replace raw high-sample counts with time-weighted fractions or edge/state sequence checks",
        "reason": "The selected-output sequence is the same shape, but high counts depend on accepted-point density.",
    },
    "vbm1_rotating_element_selector": {
        "class": "sample_count_checker_drift",
        "priority": "P1-checker",
        "action": "replace raw high-sample counts with time-weighted fractions or edge/state sequence checks",
        "reason": "The selected-output sequence is the same shape, but high counts depend on accepted-point density.",
    },
    "vbm1_edge_detector": {
        "class": "time_fraction_sampling_drift",
        "priority": "P2-checker",
        "action": "prefer time-weighted pulse width over row-fraction summaries",
        "reason": "Pulse count matches; high fraction differs because EVAS and Spectre save different points around transitions.",
    },
    "vbm1_one_shot_timer": {
        "class": "time_fraction_sampling_drift",
        "priority": "P2-checker",
        "action": "prefer time-weighted pulse width over row-fraction summaries",
        "reason": "Trigger and pulse edge counts match; only sampled high fraction differs slightly.",
    },
    "vbm1_pfd_reset_race": {
        "class": "event_timing_quantization_drift",
        "priority": "P2-tolerance",
        "action": "keep tolerance-based timing checks; add atomic regression only if pulse counts diverge",
        "reason": "Pulse counts and overlap classification match; timing fractions differ at the fourth decimal place.",
    },
    "vbm1_lock_detector": {
        "class": "time_fraction_sampling_drift",
        "priority": "P2-checker",
        "action": "use time-weighted late-lock duration or lock edge time instead of row fraction",
        "reason": "Lock assertion behavior matches; late_high differs with accepted-point density.",
    },
    "vbm1_first_order_lowpass": {
        "class": "continuous_response_numeric_drift",
        "priority": "P2-tolerance",
        "action": "keep analog-value tolerances; no EVAS fix unless drift grows across more analog kernels",
        "reason": "Lowpass sample values differ by about 1 mV, consistent with solver/sample-grid differences.",
    },
    "vbm1_leaky_hold": {
        "class": "continuous_decay_numeric_drift",
        "priority": "P2-watch",
        "action": "keep tolerance checks and reuse the $abstime/decay conformance regression for sharper coverage",
        "reason": "Hold/decay values differ by a few mV; related to continuous decay sampling but not a binary mismatch here.",
    },
    "vbm1_resettable_integrator": {
        "class": "continuous_integration_numeric_drift",
        "priority": "P2-tolerance",
        "action": "keep analog-value tolerances; consider a dedicated integrator regression if future candidates flip pass/fail",
        "reason": "Windowed analog means differ by a few mV while reset and trend semantics agree.",
    },
    "vbm1_thermometer_dac": {
        "class": "float_format_only",
        "priority": "P3-noop",
        "action": "normalize numeric formatting in reports if desired",
        "reason": "The only difference is Python/Spectre float rendering such as 0.72 vs 0.7200000000000001.",
    },
}

STABLE_REPAIRED_CHECKERS = {
    "vbm1_barrel_pointer_window",
    "vbm1_element_shuffler",
    "vbm1_rotating_element_selector",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def checker_notes(result: dict[str, Any]) -> list[str]:
    return [str(note) for note in result.get("checker_result", {}).get("notes") or []]


def strip_form(task_id: str) -> str:
    return FORM_RE.sub("", task_id)


def task_form(task_id: str) -> str:
    match = FORM_RE.search(task_id)
    return match.group(1) if match else "-"


def numbers(notes: list[str]) -> list[float]:
    vals: list[float] = []
    for note in notes:
        for raw in NUM_RE.findall(note):
            try:
                vals.append(float(raw))
            except ValueError:
                pass
    return vals


def max_numeric_delta(left: list[str], right: list[str]) -> float:
    lhs = numbers(left)
    rhs = numbers(right)
    if not lhs or not rhs:
        return 0.0
    return max(abs(a - b) for a, b in zip(lhs, rhs))


def normalized_note_signature(left: list[str], right: list[str]) -> str:
    def norm(notes: list[str]) -> str:
        return " ; ".join(NUM_RE.sub("#", note) for note in notes)

    return norm(left) + " || " + norm(right)


def resolve_artifact_path(raw: str | None) -> Path | None:
    if not raw:
        return None
    path = Path(raw)
    if path.exists():
        return path
    if not path.is_absolute():
        candidate = ROOT / path
        if candidate.exists():
            return candidate
    return None


def read_csv_rows(path: Path | None, max_rows: int = 200_000) -> list[dict[str, float]]:
    if path is None or not path.exists():
        return []
    rows: list[dict[str, float]] = []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for idx, row in enumerate(reader):
            if idx >= max_rows:
                break
            parsed: dict[str, float] = {}
            for key, value in row.items():
                if value in (None, ""):
                    continue
                try:
                    parsed[key] = float(value)
                except ValueError:
                    pass
            if parsed:
                rows.append(parsed)
    return rows


def signal_summary(rows: list[dict[str, float]], signal: str) -> dict[str, float | int] | None:
    vals = [row[signal] for row in rows if signal in row]
    if not vals:
        return None
    lo = min(vals)
    hi = max(vals)
    span = hi - lo
    threshold = 0.5 * (lo + hi)
    rises = sum(1 for idx in range(1, len(vals)) if vals[idx - 1] < threshold <= vals[idx])
    high_frac = sum(1 for val in vals if val > threshold) / max(len(vals), 1)
    return {
        "rows": len(vals),
        "min": lo,
        "max": hi,
        "span": span,
        "final": vals[-1],
        "rises": rises,
        "high_frac": high_frac,
    }


def waveform_flags(evas_result: dict[str, Any], spectre_result: dict[str, Any]) -> tuple[str, str]:
    e_csv = resolve_artifact_path(evas_result.get("artifacts", {}).get("tran_csv"))
    s_csv = resolve_artifact_path(spectre_result.get("artifacts", {}).get("tran_csv"))
    e_rows = read_csv_rows(e_csv)
    s_rows = read_csv_rows(s_csv)
    if not e_rows or not s_rows:
        return "", ""

    common = [
        sig
        for sig in e_rows[0]
        if sig != "time" and sig in s_rows[0]
    ]
    flags: list[str] = []
    max_signal_delta = 0.0
    for sig in common:
        e = signal_summary(e_rows, sig)
        s = signal_summary(s_rows, sig)
        if e is None or s is None:
            continue
        final_delta = abs(float(e["final"]) - float(s["final"]))
        span_delta = abs(float(e["span"]) - float(s["span"]))
        high_frac_delta = abs(float(e["high_frac"]) - float(s["high_frac"]))
        rise_delta = int(e["rises"]) - int(s["rises"])
        max_signal_delta = max(max_signal_delta, final_delta, span_delta, high_frac_delta)
        if rise_delta or final_delta > 0.05 or span_delta > 0.05 or high_frac_delta > 0.03:
            parts = [sig]
            if rise_delta:
                parts.append(f"rises {e['rises']} vs {s['rises']}")
            if final_delta > 0.05:
                parts.append(f"final {float(e['final']):.3g} vs {float(s['final']):.3g}")
            if span_delta > 0.05:
                parts.append(f"span {float(e['span']):.3g} vs {float(s['span']):.3g}")
            if high_frac_delta > 0.03:
                parts.append(f"hi_frac {float(e['high_frac']):.3f} vs {float(s['high_frac']):.3f}")
            flags.append(" ".join(parts))

    row_info = f"rows {len(e_rows)} vs {len(s_rows)}"
    if e_rows and s_rows and "time" in e_rows[-1] and "time" in s_rows[-1]:
        row_info += f"; stop {e_rows[-1]['time']:.12g} vs {s_rows[-1]['time']:.12g}"
    if max_signal_delta:
        row_info += f"; max_feature_delta={max_signal_delta:.4g}"
    return row_info, "; ".join(flags[:4])


def stable_check_pair(
    task_id: str,
    evas_result: dict[str, Any],
    spectre_result: dict[str, Any],
) -> dict[str, Any]:
    e_csv = resolve_artifact_path(evas_result.get("artifacts", {}).get("tran_csv"))
    s_csv = resolve_artifact_path(spectre_result.get("artifacts", {}).get("tran_csv"))
    if e_csv is None or s_csv is None:
        return {"available": False}
    e_result = evaluate_main120_stable_check(task_id, e_csv)
    s_result = evaluate_main120_stable_check(task_id, s_csv)
    if e_result is None or s_result is None:
        return {"available": False}
    e_pass, e_note = e_result
    s_pass, s_note = s_result
    return {
        "available": True,
        "evas_pass": e_pass,
        "spectre_pass": s_pass,
        "evas_note": e_note,
        "spectre_note": s_note,
        "match": e_pass and s_pass and e_note == s_note,
    }


def classify(
    base_id: str,
    evas_notes: list[str],
    spectre_notes: list[str],
    *,
    stable_match: bool = False,
) -> dict[str, str]:
    joined = " ".join(evas_notes + spectre_notes).lower()
    if base_id == "vbm1_strongarm_comparator_behavior" and "reset_outp_max" in joined:
        return {
            "class": "comparator_reset_window_numeric_drift",
            "priority": "P2-tolerance",
            "action": "keep reset-window numeric tolerance; no EVAS fix unless reset/decision classification changes",
            "reason": "The bugfix-form reset and decision windows agree; only low-level analog maxima differ by about 1 mV.",
        }
    if stable_match and base_id in STABLE_REPAIRED_CHECKERS:
        return {
            "class": "stable_sequence_checker_repair",
            "priority": "P1-resolved-checker",
            "action": "materialize checks.yaml with fixed-time state-sequence checks instead of raw sample counts",
            "reason": "The repaired stable checker gives identical EVAS/Spectre state sequences; only the historical row-count notes drift.",
        }
    if stable_match and base_id == "vbm1_strongarm_comparator_behavior":
        return {
            "class": "stable_decision_checker_and_stop_time_repair",
            "priority": "P1-resolved-benchmark",
            "action": "use fixed decision sample points and keep the source testbench stop time away from source edges",
            "reason": "The repaired stable checker gives identical EVAS/Spectre decisions; the source-controlled testbench now avoids ending on the 4 ns source boundary.",
        }
    override = CLASS_OVERRIDES.get(base_id)
    if override:
        return override

    if "frac" in joined:
        return {
            "class": "time_fraction_sampling_drift",
            "priority": "P2-checker",
            "action": "inspect checker normalization",
            "reason": "Fraction-like checker notes differ across sampling grids.",
        }
    if "highs=" in joined or "count_range" in joined:
        return {
            "class": "sample_count_checker_drift",
            "priority": "P1-checker",
            "action": "replace sample counts with time-weighted or event-count checks",
            "reason": "Raw sample counts are simulator-grid dependent.",
        }
    if max_numeric_delta(evas_notes, spectre_notes) <= 1e-9:
        return {
            "class": "float_format_only",
            "priority": "P3-noop",
            "action": "normalize report formatting if desired",
            "reason": "Numeric values are equivalent within formatting precision.",
        }
    return {
        "class": "unclassified_pass_drift",
        "priority": "P1-inspect",
        "action": "inspect waveform and checker semantics",
        "reason": "PASS/PASS checker notes differ but no specific class rule matched.",
    }


def collect(evas_root: Path, spectre_root: Path) -> list[dict[str, Any]]:
    by_group: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for e_dir in sorted(path for path in evas_root.iterdir() if path.is_dir()):
        task_id = e_dir.name
        e_path = e_dir / "evas_result.json"
        s_path = spectre_root / task_id / "spectre_result.json"
        if not e_path.exists() or not s_path.exists():
            continue
        evas = read_json(e_path)
        spectre = read_json(s_path)
        if evas.get("status") != "PASS" or spectre.get("status") != "PASS":
            continue
        e_notes = checker_notes(evas)
        s_notes = checker_notes(spectre)
        if e_notes == s_notes:
            continue
        base_id = strip_form(task_id)
        row_info, flags = waveform_flags(evas, spectre)
        stable = stable_check_pair(task_id, evas, spectre)
        signature = normalized_note_signature(e_notes, s_notes)
        by_group[(base_id, signature)].append(
            {
                "task_id": task_id,
                "form": task_form(task_id),
                "evas_notes": e_notes,
                "spectre_notes": s_notes,
                "max_numeric_delta": max_numeric_delta(e_notes, s_notes),
                "row_info": row_info,
                "waveform_flags": flags,
                "stable_available": stable.get("available", False),
                "stable_match": stable.get("match", False),
                "stable_evas_note": stable.get("evas_note", ""),
                "stable_spectre_note": stable.get("spectre_note", ""),
            }
        )

    rows: list[dict[str, Any]] = []
    for (base_id, _signature), items in sorted(by_group.items()):
        representative = items[0]
        stable_items = [item for item in items if item.get("stable_available")]
        stable_match = bool(stable_items) and all(item.get("stable_match") for item in stable_items)
        cls = classify(
            base_id,
            representative["evas_notes"],
            representative["spectre_notes"],
            stable_match=stable_match,
        )
        rows.append(
            {
                "base_id": base_id,
                "forms": ",".join(sorted(item["form"] for item in items)),
                "task_count": len(items),
                "class": cls["class"],
                "priority": cls["priority"],
                "action": cls["action"],
                "reason": cls["reason"],
                "max_numeric_delta": max(item["max_numeric_delta"] for item in items),
                "evas_note": " ; ".join(representative["evas_notes"]),
                "spectre_note": " ; ".join(representative["spectre_notes"]),
                "row_info": representative["row_info"],
                "waveform_flags": representative["waveform_flags"],
                "stable_check": "match" if stable_match else ("diff" if stable_items else "-"),
                "stable_evas_note": representative.get("stable_evas_note", ""),
                "stable_spectre_note": representative.get("stable_spectre_note", ""),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "base_id",
        "forms",
        "task_count",
        "priority",
        "class",
        "max_numeric_delta",
        "action",
        "reason",
        "evas_note",
        "spectre_note",
        "row_info",
        "waveform_flags",
        "stable_check",
        "stable_evas_note",
        "stable_spectre_note",
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(text: Any) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def write_markdown(path: Path, rows: list[dict[str, Any]], evas_root: Path, spectre_root: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    total_tasks = sum(int(row["task_count"]) for row in rows)
    class_counts: dict[str, int] = defaultdict(int)
    priority_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        class_counts[str(row["class"])] += int(row["task_count"])
        priority_counts[str(row["priority"])] += int(row["task_count"])

    lines = [
        "# EVAS/Spectre PASS Drift Audit",
        "",
        "Date: 2026-05-14",
        "",
        "## Scope",
        "",
        f"- EVAS root: `{evas_root}`",
        f"- Spectre root: `{spectre_root}`",
        "- Only tasks where both backends report `PASS` are included.",
        "- Drift means the public checker passed on both backends, but `checker_result.notes` differ.",
        "",
        "## Summary",
        "",
        f"- Drifted task forms: {total_tasks}",
        f"- Deduplicated circuit groups: {len(rows)}",
        f"- Priority counts by task form: {dict(sorted(priority_counts.items()))}",
        f"- Class counts by task form: {dict(sorted(class_counts.items()))}",
        "",
        "## Deduplicated Drift Table",
        "",
        "| Base ID | Forms | Priority | Class | Stable check | EVAS note | Spectre note | Action |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                md_escape(row[key])
                for key in [
                    "base_id",
                    "forms",
                    "priority",
                    "class",
                    "stable_check",
                    "evas_note",
                    "spectre_note",
                    "action",
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Root-Cause Notes",
            "",
        ]
    )
    for row in rows:
        lines.extend(
            [
                f"### `{row['base_id']}`",
                "",
                f"- Priority/class: `{row['priority']}` / `{row['class']}`",
                f"- Cause: {row['reason']}",
                f"- Action: {row['action']}",
                f"- Numeric delta: `{row['max_numeric_delta']}`",
                f"- CSV summary: {row['row_info'] or '-'}",
                f"- Waveform flags: {row['waveform_flags'] or '-'}",
                f"- Stable checker: `{row['stable_check']}`",
                f"- Stable EVAS note: {row['stable_evas_note'] or '-'}",
                f"- Stable Spectre note: {row['stable_spectre_note'] or '-'}",
                "",
            ]
        )

    lines.extend(
        [
            "## Interpretation",
            "",
            "- `P0-resolved` means the drift exposed an EVAS conformance bug that has already been fixed and should remain covered by an atomic regression.",
            "- `P1-checker` or `P1-benchmark` means the historical benchmark/checker can still pass while measuring a simulator-grid artifact. These should be corrected before publishing main120 as audited benchmark material.",
            "- `P1-resolved-checker` means a source-controlled stable checker now exists for materialization; regenerate result evidence when those tasks are promoted.",
            "- `P1-resolved-benchmark` means the source-controlled benchmark/checker path has been hardened; regenerate result evidence when the task is rerun.",
            "- `P2-*` means the current evidence looks like tolerable sampling or analog numeric drift, but the checker should encode explicit tolerances rather than exact note strings.",
            "- `P3-noop` is formatting-only drift.",
            "",
            "## P2 Handling Examples",
            "",
            "| Class | Examples | Why this is not an EVAS-kernel fix by default | Checker policy |",
            "| --- | --- | --- | --- |",
            "| `time_fraction_sampling_drift` | `edge_detector`, `one_shot_timer`, `lock_detector` | Edge counts and qualitative states match; row fractions move because the two simulators save different transient points. | Prefer edge counts, edge times, or time-weighted high duration over `high rows / total rows`. |",
            "| `event_timing_quantization_drift` | `pfd_reset_race` | UP/DN pulse counts and no-overlap classification match; only small timing fractions differ at accepted-step precision. | Keep explicit timing tolerances and add an atomic regression only if pulse counts or overlap classification diverge. |",
            "| `continuous_response_numeric_drift` | `first_order_lowpass` | Values differ by about 1 mV while trend and final behavior agree; forcing EVAS to match Spectre point-for-point would overfit solver sampling. | Score sampled windows with voltage tolerances and monotonic/trend assertions. |",
            "| `continuous_decay_numeric_drift` | `leaky_hold` | Decay values differ by a few mV; the important behavior is hold, exponential decay direction, and reset recovery. | Keep value tolerances and cover `$abstime` decay with a separate conformance regression. |",
            "| `continuous_integration_numeric_drift` | `resettable_integrator` | Reset and integration trend agree; window means differ by a few mV due to integration/sampling granularity. | Use reset-level, sign/trend, and bounded mean tolerances instead of exact waveform equality. |",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evas-root", type=Path, default=DEFAULT_EVAS_ROOT)
    parser.add_argument("--spectre-root", type=Path, default=DEFAULT_SPECTRE_ROOT)
    parser.add_argument("--output-csv", type=Path, default=ROOT / "docs/EVAS_SPECTRE_PASS_DRIFT_AUDIT.csv")
    parser.add_argument("--output-md", type=Path, default=ROOT / "docs/EVAS_SPECTRE_PASS_DRIFT_AUDIT.md")
    args = parser.parse_args()

    rows = collect(args.evas_root, args.spectre_root)
    write_csv(args.output_csv, rows)
    write_markdown(args.output_md, rows, args.evas_root, args.spectre_root)
    print(f"drift_groups={len(rows)} drift_task_forms={sum(int(row['task_count']) for row in rows)}")
    print(f"wrote {args.output_csv}")
    print(f"wrote {args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
