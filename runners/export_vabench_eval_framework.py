#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path
from typing import Any

from run_gold_dual_suite import compare_waveforms


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
DOCS_DATA_ROOT = ROOT / "docs" / "data"
OVERVIEW_JSON = REPORTS_ROOT / "benchmark_overview.json"

ALIGNMENT_JSON = REPORTS_ROOT / "spectre_alignment_table.json"
ALIGNMENT_CSV = REPORTS_ROOT / "spectre_alignment_table.csv"
ALIGNMENT_MD = REPORTS_ROOT / "spectre_alignment_table.md"
MODEL_ROSTER_JSON = REPORTS_ROOT / "model_eval_roster.json"
MODEL_ROSTER_CSV = REPORTS_ROOT / "model_eval_roster.csv"
MODEL_ROSTER_MD = REPORTS_ROOT / "model_eval_roster.md"
MODEL_ROSTER_TASK_IDS = REPORTS_ROOT / "model_eval_roster_scored_task_ids.txt"

DOCS_ALIGNMENT_JSON = DOCS_DATA_ROOT / "spectre_alignment_table.json"
DOCS_MODEL_ROSTER_JSON = DOCS_DATA_ROOT / "model_eval_roster.json"


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def csv_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    if value is True:
        return "True"
    if value is False:
        return "False"
    return "" if value is None else str(value)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field)) for field in fieldnames})


def fmt(value: Any) -> str:
    if value is None or value == "":
        return "-"
    if isinstance(value, float):
        if value == 0:
            return "0"
        if abs(value) >= 1000 or abs(value) < 0.001:
            return f"{value:.3e}"
        return f"{value:.4g}"
    return str(value)


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> list[str]:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row.get(field)).replace("\n", " ") for field in fields) + " |")
    return lines


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() == "true"
    return bool(value)


def as_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def as_float(value: Any) -> float | None:
    return value if isinstance(value, (int, float)) else None


def max_or_none(values: list[float | None]) -> float | None:
    present = [value for value in values if value is not None]
    return max(present) if present else None


def form_key(entry_id: Any, form: Any) -> tuple[str, str]:
    return str(entry_id or ""), str(form or "")


def load_dual_status(path: str) -> dict[tuple[str, str], dict[str, Any]]:
    summary = read_json(ROOT / path)
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for item in summary.get("results", []):
        if not isinstance(item, dict):
            continue
        raw = item.get("raw_result", {}) if isinstance(item.get("raw_result"), dict) else {}
        spectre = raw.get("spectre", {}) if isinstance(raw.get("spectre"), dict) else {}
        rows[form_key(item.get("entry_id"), item.get("form"))] = {
            "status": raw.get("status") or item.get("status"),
            "expected_result_met": as_bool(item.get("expected_result_met")),
            "spectre_ok": as_bool(spectre.get("ok")),
            "spectre_behavior_score": spectre.get("behavior_score"),
            "checker_task_id": raw.get("checker_task_id"),
            "result_root": item.get("result_root"),
            "wall_time_s": item.get("wall_time_s"),
        }
    return rows


def load_evas_status(path: str) -> dict[tuple[str, str], dict[str, Any]]:
    summary = read_json(ROOT / path)
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for item in summary.get("results", []):
        if not isinstance(item, dict):
            continue
        rows[form_key(item.get("legacy_entry_id"), item.get("form"))] = {
            "status": item.get("raw_status"),
            "compile_sim_pass": as_bool(item.get("compile_sim_pass")),
            "behavior_checker_pass": as_bool(item.get("behavior_checker_pass")),
            "behavior_checker_missing": as_bool(item.get("behavior_checker_missing")),
            "checker_task_id": item.get("checker_task_id"),
            "result_root": item.get("result_root"),
        }
    return rows


def provenance(row: dict[str, Any]) -> str:
    status = str(row.get("expansion_status") or "")
    return "promoted_v1.1" if "v1.1" in status else "inherited_v1"


def waveform_gate_text(contract: dict[str, Any]) -> str:
    return f"{contract.get('relative_rms_gate')}; {contract.get('small_absolute_gate')}"


def tolerance_profile(row: dict[str, Any], contract: dict[str, Any]) -> str:
    policy = str(row.get("parity_policy") or "")
    if policy in {"spectre_equivalence_core_v1", "spectre_equivalence_core_v2"}:
        return waveform_gate_text(contract)
    if policy == "gain_extraction_metric_parity_v1":
        return str(contract.get("gain_metric_gate"))
    if policy == "pll_task_aware":
        return str(contract.get("pll_task_aware"))
    if policy == "full_300_closure":
        if row.get("mean_relative_rms_error") is not None:
            return waveform_gate_text(contract)
        return (
            "checker-only closure: all four backends passed the row behavior checker; "
            "no waveform scalar was materialized for this row"
        )
    return "behavior checker pass gate"


def similarity_summary(row: dict[str, Any]) -> str:
    if row.get("parity_policy") == "gain_extraction_metric_parity_v1" and row.get("relative_gain_delta") is not None:
        return f"relative_gain_delta={fmt(row.get('relative_gain_delta'))}"
    if row.get("parity_policy") == "pll_task_aware" and row.get("mean_relative_rms_error") is not None:
        return (
            f"task_checker_status={row.get('parity_status')}; "
            f"waveform_diagnostic_mean_rel_rms={fmt(row.get('mean_relative_rms_error'))}; "
            f"waveform_diagnostic_worst_rel_rms={fmt(row.get('max_relative_rms_error'))}"
        )
    if row.get("mean_relative_rms_error") is not None:
        return (
            f"mean_rel_rms={fmt(row.get('mean_relative_rms_error'))}; "
            f"worst_rel_rms={fmt(row.get('max_relative_rms_error'))}; "
            f"max_rmse_v={fmt(row.get('max_rmse_v'))}; max_abs_v={fmt(row.get('max_abs_v'))}"
        )
    if row.get("relative_gain_delta") is not None:
        return f"relative_gain_delta={fmt(row.get('relative_gain_delta'))}"
    return f"policy={row.get('parity_policy')}; status={row.get('parity_status')}"


def find_waveform_csvs(result_root: str | None) -> tuple[Path | None, Path | None]:
    if not result_root:
        return None, None
    root = ROOT / result_root
    if not root.exists():
        return None, None
    for evas_csv in sorted(root.rglob("tran.csv")):
        spectre_csv = evas_csv.parent / "spectre" / "tran_spectre.csv"
        if spectre_csv.exists():
            return evas_csv, spectre_csv
    return None, None


def materialized_waveform_metrics(row: dict[str, Any], result_root: str | None) -> tuple[dict[str, Any], str]:
    if row.get("mean_relative_rms_error") is not None:
        return {
            "mean_relative_rms_error": row.get("mean_relative_rms_error"),
            "max_relative_rms_error": row.get("max_relative_rms_error"),
            "max_rmse_v": row.get("max_rmse_v"),
            "max_abs_v": row.get("max_abs_v"),
            "max_digital_mismatch_ratio": row.get("max_digital_mismatch_ratio"),
        }, "overview_report"

    evas_csv, spectre_csv = find_waveform_csvs(result_root)
    if evas_csv is None or spectre_csv is None:
        return {
            "mean_relative_rms_error": None,
            "max_relative_rms_error": None,
            "max_rmse_v": None,
            "max_abs_v": None,
            "max_digital_mismatch_ratio": None,
        }, "not_materialized"

    comparison = compare_waveforms(str(row.get("task_id") or row.get("release_entry_id") or ""), evas_csv, spectre_csv)
    return {
        "mean_relative_rms_error": comparison.get("mean_relative_rms_error"),
        "max_relative_rms_error": comparison.get("max_relative_rms_error"),
        "max_rmse_v": comparison.get("max_rmse_v"),
        "max_abs_v": comparison.get("max_abs_v"),
        "max_digital_mismatch_ratio": comparison.get("max_digital_mismatch_ratio"),
        "waveform_comparison_status": comparison.get("status"),
        "waveform_comparison_reason": comparison.get("reason"),
    }, "recomputed_from_spectre_reference_result"


def metric_family(row: dict[str, Any]) -> str:
    if row.get("parity_policy") == "gain_extraction_metric_parity_v1":
        return "extracted_gain_metric"
    if row.get("parity_policy") == "pll_task_aware":
        return "pll_task_level_lock_frequency_control"
    if row.get("mean_relative_rms_error") is not None:
        return "waveform_relative_rms_and_absolute_voltage"
    if row.get("relative_gain_delta") is not None:
        return "extracted_gain_metric"
    return "behavior_checker_only"


def equivalence_basis(row: dict[str, Any]) -> str:
    family = metric_family(row)
    if family == "waveform_relative_rms_and_absolute_voltage":
        return "common saved transient waveform columns compared on an aligned sample grid"
    if family == "extracted_gain_metric":
        return "EVAS and Spectre extracted gain metric compared instead of pointwise waveform"
    if family == "pll_task_level_lock_frequency_control":
        return "task-level PLL lock/frequency/control checker pass, not pointwise waveform equality"
    return "row behavior checker pass across Spectre reference, Spectre AX, EVAS Rust, and EVAS Python"


def equality_claim(row: dict[str, Any]) -> str:
    if row.get("alignment_status") == "spectre_aligned_within_tolerance":
        return "not bit-exact; equivalent within the stated acceptance gate"
    return "not certified"


def pass_fail(ok: bool | None) -> str:
    if ok is None:
        return "N/A"
    return "PASS" if ok else "FAIL"


def tolerance_result(row: dict[str, Any]) -> str:
    family = metric_family(row)
    if family == "waveform_relative_rms_and_absolute_voltage":
        mean = as_float(row.get("mean_relative_rms_error"))
        worst = as_float(row.get("max_relative_rms_error"))
        rmse = as_float(row.get("max_rmse_v"))
        max_abs = as_float(row.get("max_abs_v"))
        relative_gate = None
        if mean is not None and worst is not None:
            relative_gate = (mean <= 0.10 and worst <= 0.22) or (mean <= 0.08 and worst <= 0.25)
        absolute_gate = None
        if rmse is not None and max_abs is not None:
            absolute_gate = rmse <= 0.05 and max_abs <= 0.30
        return (
            f"relative_gate {pass_fail(relative_gate)}: mean_rel_rms={fmt(mean)} vs <=0.10 "
            f"and worst_rel_rms={fmt(worst)} vs <=0.22 "
            f"(alternate <=0.08/<=0.25); "
            f"small_absolute_gate {pass_fail(absolute_gate)}: max_rmse_v={fmt(rmse)} vs <=0.05 V "
            f"and max_abs_v={fmt(max_abs)} vs <=0.30 V; "
            "acceptance requires behavior pass plus one applicable waveform gate"
        )
    if family == "extracted_gain_metric":
        return f"relative_gain_delta {fmt(row.get('relative_gain_delta'))} <= 0.25"
    if family == "pll_task_level_lock_frequency_control":
        return "PLL task checker returned passed; numeric lock/frequency/control tolerances live in the checker"
    return "four-backend behavior checker returned passed; no scalar waveform tolerance is exposed"


def alignment_status(row: dict[str, Any], backend: dict[str, Any]) -> str:
    checks = [
        row.get("spectre") == "pass",
        row.get("evas") == "pass",
        row.get("parity_status") == "passed",
        backend.get("spectre_reference_status") == "PASS",
        backend.get("spectre_ax_status") == "PASS",
        backend.get("evas_rust_behavior_checker_pass") is True,
        backend.get("evas_python_behavior_checker_pass") is True,
    ]
    return "spectre_aligned_within_tolerance" if all(checks) else "needs_review"


def form_dir_from_row(row: dict[str, Any]) -> str:
    for asset in row.get("gold_assets", []) or []:
        text = str(asset)
        if "/gold/" in text:
            return text.split("/gold/", 1)[0]
    return ""


def release_task_for_row(row: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    form_dir = form_dir_from_row(row)
    if not form_dir:
        return "", {}
    manifest = ROOT / form_dir / "release_task.json"
    return rel(manifest), read_json(manifest)


def public_inputs_for(row: dict[str, Any], release_task: dict[str, Any]) -> list[str]:
    artifacts = release_task.get("artifacts", {}) if isinstance(release_task.get("artifacts"), dict) else {}
    explicit = artifacts.get("public_inputs")
    if isinstance(explicit, list) and explicit:
        return [str(item) for item in explicit]
    inputs = ["prompt.md"]
    gold_names = [Path(str(item)).name for item in row.get("gold_assets", []) or []]
    if row.get("form") == "bugfix" and "dut_buggy.va" in gold_names:
        inputs.append("gold/dut_buggy.va")
    return inputs


def submission_artifacts_for(row: dict[str, Any], release_task: dict[str, Any]) -> list[str]:
    artifacts = release_task.get("artifacts", {}) if isinstance(release_task.get("artifacts"), dict) else {}
    explicit = artifacts.get("submission_artifacts")
    if isinstance(explicit, list) and explicit:
        return [str(item) for item in explicit]
    form = str(row.get("form") or "")
    if form == "tb":
        return ["tb_*.scs"]
    if form == "e2e":
        return ["*.va", "tb_*.scs"]
    return ["*.va"]


def build_alignment(overview: dict[str, Any]) -> dict[str, Any]:
    source_reports = overview.get("source_reports", {}) if isinstance(overview.get("source_reports"), dict) else {}
    contract = overview.get("equivalence_contract", {}) if isinstance(overview.get("equivalence_contract"), dict) else {}
    reference = load_dual_status(str(source_reports.get("spectre_reference_full300_summary", "")))
    ax = load_dual_status(str(source_reports.get("spectre_ax_full300_summary", "")))
    evas_rust = load_evas_status(str(source_reports.get("evas_rust_full300_summary", "")))
    evas_python = load_evas_status(str(source_reports.get("evas_python_full300_summary", "")))

    rows: list[dict[str, Any]] = []
    for idx, row in enumerate(overview.get("form_rows", []), start=1):
        if not isinstance(row, dict):
            continue
        key = form_key(row.get("release_entry_id"), row.get("form"))
        ref = reference.get(key, {})
        ax_row = ax.get(key, {})
        rust = evas_rust.get(key, {})
        py = evas_python.get(key, {})
        backend = {
            "spectre_reference_status": ref.get("status"),
            "spectre_reference_ok": ref.get("spectre_ok"),
            "spectre_ax_status": ax_row.get("status"),
            "spectre_ax_ok": ax_row.get("spectre_ok"),
            "evas_rust_status": rust.get("status"),
            "evas_rust_behavior_checker_pass": rust.get("behavior_checker_pass"),
            "evas_python_status": py.get("status"),
            "evas_python_behavior_checker_pass": py.get("behavior_checker_pass"),
        }
        metrics, waveform_metric_source = materialized_waveform_metrics(row, ref.get("result_root"))
        enriched = {**row, **metrics}
        out = {
            "row": idx,
            "task_id": row.get("task_id"),
            "legacy_task_id": row.get("legacy_task_id"),
            "release_entry_id": row.get("release_entry_id"),
            "form": row.get("form"),
            "category": row.get("category"),
            "level": row.get("level"),
            "difficulty": row.get("difficulty"),
            "track": row.get("track"),
            "counted_in_score": as_bool(row.get("counted_in_score")),
            "provenance": provenance(row),
            "gold_status": row.get("gold_status"),
            "static": row.get("static"),
            "evas": row.get("evas"),
            "spectre": row.get("spectre"),
            "parity_status": row.get("parity_status"),
            "parity_policy": row.get("parity_policy"),
            "bit_exact_claim": contract.get("bit_exact_claim", "not_asserted"),
            "comparison_target": "gold EVAS transient/metric result vs gold Spectre reference result for the same released row",
            "metric_family": metric_family(enriched),
            "equivalence_basis": equivalence_basis(enriched),
            "tolerance_profile": tolerance_profile(enriched, contract),
            "similarity_summary": similarity_summary(enriched),
            "mean_relative_rms_error": enriched.get("mean_relative_rms_error"),
            "max_relative_rms_error": enriched.get("max_relative_rms_error"),
            "max_rmse_v": enriched.get("max_rmse_v"),
            "max_abs_v": enriched.get("max_abs_v"),
            "max_digital_mismatch_ratio": enriched.get("max_digital_mismatch_ratio"),
            "relative_gain_delta": row.get("relative_gain_delta"),
            "waveform_metric_source": waveform_metric_source,
            "waveform_comparison_status": enriched.get("waveform_comparison_status"),
            "waveform_comparison_reason": enriched.get("waveform_comparison_reason"),
            **backend,
            "alignment_status": alignment_status(row, backend),
            "evidence": row.get("evidence"),
            "spectre_reference_result_root": ref.get("result_root"),
            "spectre_ax_result_root": ax_row.get("result_root"),
            "evas_rust_result_root": rust.get("result_root"),
            "evas_python_result_root": py.get("result_root"),
        }
        out["equality_claim"] = equality_claim(out)
        out["tolerance_result"] = tolerance_result(out)
        rows.append(out)

    aligned = [row for row in rows if row["alignment_status"] == "spectre_aligned_within_tolerance"]
    waveform_rows = [row for row in rows if row.get("metric_family") == "waveform_relative_rms_and_absolute_voltage"]
    diagnostic_waveform_rows = [row for row in rows if row.get("mean_relative_rms_error") is not None]
    gain_rows = [row for row in rows if row.get("relative_gain_delta") is not None]
    family_counts = {
        family: sum(1 for row in rows if row.get("metric_family") == family)
        for family in sorted({str(row.get("metric_family")) for row in rows})
    }
    return {
        "date": date.today().isoformat(),
        "release": overview.get("release"),
        "status": "pass" if len(aligned) == len(rows) else "needs_review",
        "summary": {
            "row_count": len(rows),
            "entry_count": overview.get("summary", {}).get("entry_count"),
            "aligned_row_count": len(aligned),
            "needs_review_row_count": len(rows) - len(aligned),
            "scored_row_count": sum(1 for row in rows if row.get("counted_in_score")),
            "inherited_v1_rows": sum(1 for row in rows if row.get("provenance") == "inherited_v1"),
            "promoted_v1_1_rows": sum(1 for row in rows if row.get("provenance") == "promoted_v1.1"),
            "bit_exact_claim": contract.get("bit_exact_claim", "not_asserted"),
            "waveform_metric_row_count": len(waveform_rows),
            "diagnostic_waveform_metric_row_count": len(diagnostic_waveform_rows),
            "waveform_metric_recomputed_row_count": sum(
                1 for row in rows if row.get("waveform_metric_source") == "recomputed_from_spectre_reference_result"
            ),
            "gain_metric_row_count": len(gain_rows),
            "metric_family_counts": family_counts,
            "max_mean_relative_rms_error": max_or_none(
                [as_float(row.get("mean_relative_rms_error")) for row in waveform_rows]
            ),
            "max_worst_signal_relative_rms_error": max_or_none(
                [as_float(row.get("max_relative_rms_error")) for row in waveform_rows]
            ),
            "max_rmse_v": max_or_none([as_float(row.get("max_rmse_v")) for row in waveform_rows]),
            "max_abs_v": max_or_none([as_float(row.get("max_abs_v")) for row in waveform_rows]),
            "max_relative_gain_delta": max_or_none([as_float(row.get("relative_gain_delta")) for row in gain_rows]),
        },
        "equivalence_contract": contract,
        "source_reports": source_reports,
        "rerun_commands": {
            "spectre_reference_full_300": "python3 runners/run_vabench_300_dual_rerun.py --spectre-backend sui-direct --spectre-mode reference --output-root results/<tag> --workers 4 --allow-direct-run",
            "spectre_ax_full_300": "python3 runners/run_vabench_300_dual_rerun.py --spectre-backend sui-direct --spectre-mode ax --output-root results/<tag> --workers 4 --allow-direct-run",
            "evas_rust_full_300": "python3 runners/run_vabench_300_evas_gold.py --engine evas-rust --output-root results/<tag>",
            "evas_python_full_300": "python3 runners/run_vabench_300_evas_gold.py --engine python --output-root results/<tag>",
            "refresh_overview": "python3 runners/report_vabench_release_benchmark_overview.py && python3 runners/export_vabench_eval_framework.py",
        },
        "rows": rows,
    }


def build_model_roster(overview: dict[str, Any], alignment: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    alignment_by_task = {str(row.get("task_id")): row for row in alignment.get("rows", [])}
    for row in overview.get("form_rows", []):
        if not isinstance(row, dict) or not as_bool(row.get("counted_in_score")):
            continue
        manifest, release_task = release_task_for_row(row)
        artifacts = release_task.get("artifacts", {}) if isinstance(release_task.get("artifacts"), dict) else {}
        prompt = artifacts.get("prompt") or (str(Path(manifest).parent / "prompt.md") if manifest else "")
        task_id = str(row.get("task_id") or "")
        rows.append(
            {
                "release_entry_id": row.get("release_entry_id"),
                "task_id": row.get("legacy_task_id") or task_id,
                "normalized_task_id": task_id,
                "form": row.get("form"),
                "level": row.get("level"),
                "track": row.get("track"),
                "difficulty": row.get("difficulty"),
                "category": row.get("category"),
                "base_function": row.get("base_function"),
                "counted_in_score": True,
                "score_surface": "model-capability",
                "manifest": manifest,
                "prompt": prompt,
                "public_inputs": public_inputs_for(row, release_task),
                "submission_artifacts": submission_artifacts_for(row, release_task),
                "private_reference_artifacts": artifacts.get("private_reference_artifacts", []),
                "final_judge": "Spectre + deterministic behavior checker",
                "fast_judge": "EVAS Rust/Python behavior checker",
                "gold_alignment_status": alignment_by_task.get(task_id, {}).get("alignment_status"),
                "tolerance_profile": alignment_by_task.get(task_id, {}).get("tolerance_profile"),
                "provenance": provenance(row),
            }
        )

    rows.sort(key=lambda item: (str(item["category"]), str(item["release_entry_id"]), str(item["form"])))
    return {
        "date": date.today().isoformat(),
        "release": overview.get("release"),
        "status": "ready" if rows else "empty",
        "summary": {
            "scored_model_row_count": len(rows),
            "entry_count": len({row["release_entry_id"] for row in rows}),
            "inherited_v1_rows": sum(1 for row in rows if row["provenance"] == "inherited_v1"),
            "promoted_v1_1_rows": sum(1 for row in rows if row["provenance"] == "promoted_v1.1"),
            "gold_aligned_rows": sum(
                1 for row in rows if row.get("gold_alignment_status") == "spectre_aligned_within_tolerance"
            ),
        },
        "runner_contract": {
            "unified_runner": "runners/run_vabench_model_eval.py --score-roster benchmark-vabench-release-v1/reports/model_eval_roster.json",
            "generation_evas_runner": "runners/run_vabench_release_minimax_baseline.py --score-roster benchmark-vabench-release-v1/reports/model_eval_roster.json",
            "spectre_final_judge_runner": "runners/run_vabench_release_model_dual_judge.py --score-roster benchmark-vabench-release-v1/reports/model_eval_roster.json",
            "api_support": "OpenAI-compatible chat completions and Anthropic messages API through existing runner flags.",
            "credential_policy": "API keys are read from env or --api-key-file and are not written to result metadata.",
            "result_contract": "The unified runner writes results/vabench-model-eval-<model>-<tag>/summary.json and summary.md with EVAS and optional Spectre sections.",
        },
        "example_commands": {
            "full_eval_with_spectre": "python3 runners/run_vabench_model_eval.py --model <model> --base-url <url> --api-format openai --api-key-file <key-file> --final-judge spectre --tag <tag> --resume",
            "evas_only_baseline": "python3 runners/run_vabench_model_eval.py --model <model> --base-url <url> --api-format openai --api-key-file <key-file> --final-judge none --tag <tag> --resume",
            "deepseek_v4_flash_smoke": "python3 runners/run_vabench_model_eval.py --model deepseek-v4-flash --base-url https://api.deepseek.com --api-format openai --api-key-file <key-file> --limit 1 --final-judge none --proxy-url <proxy-url-if-needed>",
            "one_task_smoke": "python3 runners/run_vabench_model_eval.py --model <model> --base-url <url> --task-id <task_id> --limit 1 --dry-run",
            "list_roster": "python3 runners/run_vabench_model_eval.py --list",
        },
        "form_rows": rows,
        "rows": rows,
    }


def write_alignment_md(report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# vaBench Spectre Alignment Table",
        "",
        f"Date: {report['date']}",
        f"Status: `{report['status']}`",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| rows | {summary['row_count']} |",
        f"| aligned rows | {summary['aligned_row_count']} |",
        f"| needs review | {summary['needs_review_row_count']} |",
        f"| scored rows | {summary['scored_row_count']} |",
        f"| inherited v1 rows | {summary['inherited_v1_rows']} |",
        f"| promoted v1.1 rows | {summary['promoted_v1_1_rows']} |",
        f"| bit-exact claim | `{summary['bit_exact_claim']}` |",
        f"| waveform acceptance rows | {summary['waveform_metric_row_count']} |",
        f"| diagnostic waveform metric rows | {summary['diagnostic_waveform_metric_row_count']} |",
        f"| diagnostic waveform metrics recomputed from result CSV | {summary['waveform_metric_recomputed_row_count']} |",
        f"| max mean relative RMS error | {fmt(summary['max_mean_relative_rms_error'])} |",
        f"| max worst-signal relative RMS error | {fmt(summary['max_worst_signal_relative_rms_error'])} |",
        f"| max RMSE V | {fmt(summary['max_rmse_v'])} |",
        f"| max abs V | {fmt(summary['max_abs_v'])} |",
        "",
        "## How To Read This Table",
        "",
        "- Comparison target: the released gold row is run through EVAS and through Spectre; the table compares those outputs for the same DUT/testbench row.",
        "- Equality claim: this table does not claim bit-exact equality. It claims behavioral equivalence within the explicit acceptance gate shown per row.",
        "- Waveform rows: `mean_relative_rms_error` is the average normalized RMS error across common saved signals; `max_relative_rms_error` is the worst saved signal; `max_rmse_v` and `max_abs_v` are absolute voltage errors.",
        "- Gain rows: the acceptance metric is extracted gain agreement, not point-by-point waveform equality.",
        "- PLL/task rows: the acceptance metric is the task checker for lock/frequency/control behavior; pointwise waveform equality is not the right claim.",
        "- Checker-only rows, if any, should not be described as having a numeric waveform tolerance unless waveform metrics are materialized.",
        "",
        "## Contract",
        "",
    ]
    for key, value in report["equivalence_contract"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(
        [
            "",
            "## Rerun Commands",
            "",
        ]
    )
    for key, value in report["rerun_commands"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Full Row Table",
            "",
            *md_table(
                report["rows"],
                [
                    "row",
                    "task_id",
                    "category",
                    "form",
                    "provenance",
                    "alignment_status",
                    "equality_claim",
                    "metric_family",
                    "similarity_summary",
                    "tolerance_profile",
                    "tolerance_result",
                ],
            ),
        ]
    )
    ALIGNMENT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_model_roster_md(report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# vaBench Model Evaluation Roster",
        "",
        f"Date: {report['date']}",
        f"Status: `{report['status']}`",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| scored model rows | {summary['scored_model_row_count']} |",
        f"| entries | {summary['entry_count']} |",
        f"| inherited v1 rows | {summary['inherited_v1_rows']} |",
        f"| promoted v1.1 rows | {summary['promoted_v1_1_rows']} |",
        f"| gold aligned rows | {summary['gold_aligned_rows']} |",
        "",
        "## Runner Contract",
        "",
    ]
    for key, value in report["runner_contract"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Example Commands", ""])
    for key, value in report["example_commands"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Scored Model Rows",
            "",
            *md_table(
                report["rows"],
                [
                    "task_id",
                    "category",
                    "form",
                    "difficulty",
                    "prompt",
                    "submission_artifacts",
                    "gold_alignment_status",
                ],
            ),
        ]
    )
    MODEL_ROSTER_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_eval_framework() -> dict[str, Path]:
    overview = read_json(OVERVIEW_JSON)
    alignment = build_alignment(overview)
    roster = build_model_roster(overview, alignment)

    write_json(ALIGNMENT_JSON, alignment)
    write_csv(
        ALIGNMENT_CSV,
        alignment["rows"],
        [
            "row",
            "task_id",
            "legacy_task_id",
            "release_entry_id",
            "form",
            "category",
            "level",
            "difficulty",
            "track",
            "counted_in_score",
            "provenance",
            "alignment_status",
            "spectre_reference_status",
            "spectre_ax_status",
            "evas_rust_behavior_checker_pass",
            "evas_python_behavior_checker_pass",
            "comparison_target",
            "equality_claim",
            "metric_family",
            "equivalence_basis",
            "parity_policy",
            "bit_exact_claim",
            "similarity_summary",
            "tolerance_profile",
            "tolerance_result",
            "waveform_metric_source",
            "waveform_comparison_status",
            "waveform_comparison_reason",
            "mean_relative_rms_error",
            "max_relative_rms_error",
            "max_rmse_v",
            "max_abs_v",
            "max_digital_mismatch_ratio",
            "relative_gain_delta",
            "evidence",
        ],
    )
    write_alignment_md(alignment)

    write_json(MODEL_ROSTER_JSON, roster)
    write_csv(
        MODEL_ROSTER_CSV,
        roster["rows"],
        [
            "task_id",
            "normalized_task_id",
            "release_entry_id",
            "form",
            "category",
            "level",
            "difficulty",
            "track",
            "manifest",
            "prompt",
            "public_inputs",
            "submission_artifacts",
            "final_judge",
            "fast_judge",
            "gold_alignment_status",
            "tolerance_profile",
            "provenance",
        ],
    )
    write_model_roster_md(roster)
    MODEL_ROSTER_TASK_IDS.write_text(
        "\n".join(str(row["task_id"]) for row in roster["rows"]) + "\n",
        encoding="utf-8",
    )

    write_json(DOCS_ALIGNMENT_JSON, alignment)
    write_json(DOCS_MODEL_ROSTER_JSON, roster)

    return {
        "alignment_json": ALIGNMENT_JSON,
        "alignment_csv": ALIGNMENT_CSV,
        "alignment_md": ALIGNMENT_MD,
        "model_roster_json": MODEL_ROSTER_JSON,
        "model_roster_csv": MODEL_ROSTER_CSV,
        "model_roster_md": MODEL_ROSTER_MD,
        "model_roster_task_ids": MODEL_ROSTER_TASK_IDS,
        "docs_alignment_json": DOCS_ALIGNMENT_JSON,
        "docs_model_roster_json": DOCS_MODEL_ROSTER_JSON,
    }


def main() -> None:
    written = export_eval_framework()
    for name, path in written.items():
        print(f"{name}: {rel(path)}")


if __name__ == "__main__":
    main()
