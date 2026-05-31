#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from run_gold_suite import ahdl_includes, checker_task_id, choose_gold_tb, read_meta
from run_vabench_release_evas_speed_experiment import (
    MODES as EVAS_MODES,
    NO_CLAIM_REASON as EVAS_ONLY_NO_CLAIM_REASON,
    SPEED_ARTIFACT_JSON,
    inject_simulator_options,
    load_speed_rows,
    select_rows,
    task_dir_for,
)
from run_gold_dual_suite import compare_waveforms
from simulate_evas import evaluate_behavior_with_timeout, has_behavior_check, run_case
from vabench_release_paths import release_entry_dir


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
SPEED_OPT_ROOT = ROOT / "speed-optimization"
REPORTS_ROOT = SPEED_OPT_ROOT / "reports"
DEFAULT_OUTPUT_ROOT = ROOT / "results" / f"same-server-speed-{date.today().isoformat().replace('-', '')}"
DEFAULT_REPORT_JSON = REPORTS_ROOT / "same_server_speed_smoke.json"
DEFAULT_REPORT_MD = REPORTS_ROOT / "same_server_speed_smoke.md"
SCHEMA_VERSION = "same-server-speed.v1"
ARTIFACT_KIND = "candidate_same_server_evas_spectre_timing"
NO_CLAIM_REASON = (
    "Same-server timing is measured directly on one host and the artifact emits "
    "checker/waveform Spectre-equivalence gates. Paper-facing speed claims should use only "
    "equivalence-gated rows and still need repeated cold/warm runs."
)


@dataclass(frozen=True)
class SpectreMode:
    cli_args: tuple[str, ...]
    label: str
    normalize_settings: bool = False
    half_maxstep: bool = False


NORMALIZED_SPECTRE_SIMULATOR_OPTIONS = {
    "reltol": "1e-5",
    "vabstol": "1e-8",
    "iabstol": "1e-12",
    "gmin": "1e-12",
}
NORMALIZED_SPECTRE_TRAN_OPTIONS = {
    "errpreset": "conservative",
}


SPECTRE_MODES: dict[str, SpectreMode] = {
    "classic": SpectreMode((), "legacy non-AX Spectre path"),
    "ax": SpectreMode(("+preset=ax", "+mt"), "legacy alias for ax_speed"),
    "ax_speed": SpectreMode(("+preset=ax", "+mt"), "fast Spectre AX preset speed baseline"),
    "spectre_ax_default_speed": SpectreMode(("+preset=ax", "+mt"), "fast Spectre AX preset speed baseline"),
    "ax_normalized": SpectreMode(
        ("+preset=ax", "+mt"),
        "AX preset with explicit shared tran/options settings for precision ranking",
        normalize_settings=True,
    ),
    "spectre_ax_equalized_precision": SpectreMode(
        ("+preset=ax", "+mt"),
        "AX preset with explicit shared tran/options settings for precision ranking",
        normalize_settings=True,
    ),
    "reference_strict_primary": SpectreMode(
        (),
        "non-AX Spectre reference with explicit shared tran/options settings",
        normalize_settings=True,
    ),
    "spectre_reference_strict_primary": SpectreMode(
        (),
        "non-AX Spectre reference with explicit shared tran/options settings",
        normalize_settings=True,
    ),
    "reference_strict_halfstep": SpectreMode(
        (),
        "non-AX Spectre reference sensitivity run with explicit half maxstep when present",
        normalize_settings=True,
        half_maxstep=True,
    ),
}


@dataclass(frozen=True)
class Selection:
    row: dict[str, object]
    task_dir: Path
    task_id: str
    checker_id: str


@dataclass(frozen=True)
class WorkItem:
    index: int
    selection: Selection
    backend: str
    mode: str


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def safe_path_component(value: object) -> str:
    text = str(value or "none")
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_") or "none"


def selection_variant(selection: Selection) -> str:
    return safe_path_component(selection.row.get("variant") or "gold")


def selection_output_root(output_root: Path, selection: Selection, backend: str) -> Path:
    return (
        output_root
        / backend
        / safe_path_component(selection.row["entry_id"])
        / safe_path_component(selection.row["form"])
        / selection_variant(selection)
        / safe_path_component(selection.task_id)
    )


def float_or_none(value: object) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def geomean(values: list[float]) -> float | None:
    positives = [value for value in values if value > 0.0 and math.isfinite(value)]
    if not positives:
        return None
    return math.exp(sum(math.log(value) for value in positives) / len(positives))


def prepend_current_python_bin_to_path() -> None:
    """Make the venv's console scripts visible without dropping Cadence PATH."""
    py_bin = str(Path(sys.executable).parent)
    path_parts = [part for part in os.environ.get("PATH", "").split(os.pathsep) if part]
    if py_bin not in path_parts:
        os.environ["PATH"] = os.pathsep.join([py_bin, *path_parts])


def parse_duration_seconds(text: str) -> float | None:
    text = text.strip()
    match = re.fullmatch(
        r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*"
        r"(fs|ps|ns|us|µs|ms|s|sec|secs|second|seconds)?",
        text,
    )
    if match is None:
        return None
    value = float(match.group(1))
    unit = (match.group(2) or "s").lower()
    scale = {
        "fs": 1e-15,
        "ps": 1e-12,
        "ns": 1e-9,
        "us": 1e-6,
        "µs": 1e-6,
        "ms": 1e-3,
        "s": 1.0,
        "sec": 1.0,
        "secs": 1.0,
        "second": 1.0,
        "seconds": 1.0,
    }[unit]
    return value * scale


def parse_spectre_timing(text: str) -> dict[str, float]:
    timing: dict[str, float] = {}
    tran_match = re.search(
        r"Total time required for tran analysis `tran':.*?elapsed\s*=\s*([^\n,]+)",
        text,
        flags=re.DOTALL,
    )
    if tran_match:
        parsed = parse_duration_seconds(tran_match.group(1).strip())
        if parsed is not None:
            timing["tran_elapsed_s"] = parsed

    aggregate_match = re.search(
        r"Time used:.*?elapsed\s*=\s*([^\n,]+)",
        text,
        flags=re.DOTALL,
    )
    if aggregate_match:
        parsed = parse_duration_seconds(aggregate_match.group(1).strip())
        if parsed is not None:
            timing["aggregate_elapsed_s"] = parsed

    wall_match = re.search(
        r"with elapsed time \(wall clock\):\s*([^\n.]+(?:\.[0-9]+)?\s*(?:ms|s|sec|seconds)?)",
        text,
    )
    if wall_match:
        parsed = parse_duration_seconds(wall_match.group(1).strip())
        if parsed is not None:
            timing["reported_wall_s"] = parsed

    steps_match = re.search(r"Number of accepted tran steps\s*=\s*([0-9]+)", text)
    if steps_match:
        timing["accepted_tran_steps"] = float(steps_match.group(1))

    ahdl_match = re.search(r"Finished compilation in\s+([0-9.]+)\s+s\s+\(elapsed\)", text)
    if ahdl_match:
        timing["ahdl_compile_elapsed_s"] = float(ahdl_match.group(1))

    return timing


def decode_psf_name(value: str) -> str:
    return (
        value.replace(r"\"", '"')
        .replace(r"\\", "\\")
        .replace(r"\<", "<")
        .replace(r"\>", ">")
    )


def parse_psf_pair(line: str) -> tuple[str, str] | None:
    match = re.match(r'^"((?:[^"\\]|\\.)*)"\s+(.+?)\s*$', line)
    if match is None:
        return None
    return decode_psf_name(match.group(1)), match.group(2).strip()


def parse_psf_float(value: str) -> float:
    token = value.strip()
    if token.startswith("(") and token.endswith(")"):
        token = token[1:-1].split()[0]
    return float(token)


def find_spectre_tran_file(raw_dir: Path) -> Path:
    preferred = [
        raw_dir / "tran.tran.tran",
        raw_dir / "tran.tran",
        raw_dir / "tran",
    ]
    for path in preferred:
        if path.exists() and path.is_file():
            return path
    candidates = sorted(path for path in raw_dir.rglob("*tran*") if path.is_file())
    if not candidates:
        raise FileNotFoundError(f"no transient PSFASCII file under {raw_dir}")
    return candidates[0]


def read_psf_trace_names(psf_path: Path) -> list[str]:
    section = ""
    traces: list[str] = []
    with psf_path.open("r", encoding="utf-8", errors="replace") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            if line in {"HEADER", "TYPE", "SWEEP", "TRACE", "VALUE"}:
                section = line
                if section == "VALUE":
                    break
                continue
            if section != "TRACE":
                continue
            parsed = parse_psf_pair(line)
            if parsed is None:
                continue
            name, _kind = parsed
            if name not in traces:
                traces.append(name)
    return traces


def write_spectre_psf_csv(raw_dir: Path, csv_path: Path) -> dict[str, object]:
    psf_path = find_spectre_tran_file(raw_dir)
    trace_names = read_psf_trace_names(psf_path)
    columns = ["time", *[name for name in trace_names if name != "time"]]
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    rows = 0
    section = ""
    current: dict[str, float] = {}
    with psf_path.open("r", encoding="utf-8", errors="replace") as src, csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as dst:
        writer = csv.DictWriter(dst, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for raw_line in src:
            line = raw_line.strip()
            if not line:
                continue
            if line in {"HEADER", "TYPE", "SWEEP", "TRACE", "VALUE"}:
                section = line
                continue
            if section != "VALUE":
                continue
            parsed = parse_psf_pair(line)
            if parsed is None:
                continue
            name, value_text = parsed
            try:
                value = parse_psf_float(value_text)
            except ValueError:
                continue
            if name == "time":
                if current:
                    writer.writerow(current)
                    rows += 1
                current = {"time": value}
            elif name in columns:
                current[name] = value
        if current:
            writer.writerow(current)
            rows += 1

    if rows == 0:
        raise ValueError(f"no transient rows parsed from {psf_path}")
    return {
        "psf_path": rel(psf_path),
        "csv_path": rel(csv_path),
        "rows": rows,
        "columns": columns,
    }


def evaluate_csv_behavior(
    checker_id: str,
    csv_path: Path | None,
    *,
    timeout_s: int,
) -> dict[str, object]:
    available = has_behavior_check(checker_id)
    if csv_path is None or not csv_path.exists():
        return {
            "check_available": available,
            "score": None,
            "ok": False,
            "notes": ["missing csv"],
        }
    score, notes = evaluate_behavior_with_timeout(checker_id, csv_path, timeout_s=timeout_s)
    ok = available and score >= 1.0
    return {
        "check_available": available,
        "score": score,
        "ok": ok,
        "notes": notes,
    }


def prepare_selection(row: dict[str, object]) -> Selection:
    task_dir = task_dir_for(row)
    meta = read_meta(task_dir)
    task_id = str(meta.get("task_id") or meta.get("id") or task_dir.name)
    return Selection(
        row=row,
        task_dir=task_dir,
        task_id=task_id,
        checker_id=checker_task_id(meta, task_id),
    )


def entry_forms_dir(selection: Selection) -> Path:
    return release_entry_dir(PACKAGE_ROOT / "tasks", str(selection.row["entry_id"])) / "forms"


def form_gold_dir(selection: Selection, form: str) -> Path:
    return entry_forms_dir(selection) / form / "gold"


def existing_gold_dirs(selection: Selection) -> list[Path]:
    forms = [str(selection.row["form"]), "tb", "e2e", "dut", "bugfix"]
    seen: set[Path] = set()
    dirs: list[Path] = []
    for form in forms:
        gold = form_gold_dir(selection, form)
        if gold in seen or not gold.is_dir():
            continue
        seen.add(gold)
        dirs.append(gold)
    return dirs


def copy_gold_contents(src_gold: Path, dst_gold: Path, *, overwrite: bool) -> None:
    if not src_gold.is_dir():
        return
    for item in sorted(src_gold.iterdir()):
        dst = dst_gold / item.name
        if dst.exists() and not overwrite:
            continue
        if item.is_dir():
            if dst.exists() and overwrite:
                shutil.rmtree(dst)
            if not dst.exists():
                shutil.copytree(item, dst)
        elif item.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dst)


def choose_fixture_tb_gold(selection: Selection) -> Path:
    form = str(selection.row["form"])
    preferred_forms = {
        "tb": ("tb", "e2e", "dut", "bugfix"),
        "e2e": ("e2e", "tb", "dut", "bugfix"),
        "dut": ("dut", "tb", "e2e", "bugfix"),
        "bugfix": ("bugfix", "tb", "e2e", "dut"),
    }.get(form, (form, "tb", "e2e", "dut", "bugfix"))
    for candidate_form in preferred_forms:
        gold = form_gold_dir(selection, candidate_form)
        if gold.is_dir() and choose_gold_tb(gold) is not None:
            return gold
    raise FileNotFoundError(f"no gold testbench found for {selection.row['entry_id']}/{form}")


def variant_source_path(selection: Selection, gold_dir: Path) -> Path | None:
    if str(selection.row.get("form")) != "bugfix":
        return None
    variant = str(selection.row.get("variant") or "fixed")
    source_name = {
        "fixed": "dut_fixed.va",
        "buggy": "dut_buggy.va",
    }.get(variant)
    if source_name is None:
        return None
    source = gold_dir / source_name
    return source if source.exists() else None


def current_form_primary_va(selection: Selection) -> Path | None:
    current_gold = selection.task_dir / "gold"
    variant_source = variant_source_path(selection, current_gold)
    if variant_source is not None:
        return variant_source
    va_files = sorted(path for path in current_gold.glob("*.va") if path.is_file())
    if len(va_files) == 1:
        return va_files[0]
    if str(selection.row.get("form")) == "dut" and va_files:
        return va_files[0]
    return None


def candidate_include_sources(selection: Selection, include: str, *, prefer_primary: bool) -> list[Path]:
    include_path = Path(include)
    include_name = include_path.name
    candidates: list[Path] = []

    primary = current_form_primary_va(selection)
    if prefer_primary and primary is not None:
        candidates.append(primary)

    for gold in existing_gold_dirs(selection):
        candidates.append(gold / include)
        candidates.append(gold / include_name)
        if prefer_primary:
            variant_source = variant_source_path(selection, gold)
            if variant_source is not None:
                candidates.append(variant_source)
            va_files = sorted(path for path in gold.glob("*.va") if path.is_file())
            if len(va_files) == 1:
                candidates.append(va_files[0])

    seen: set[Path] = set()
    unique: list[Path] = []
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except FileNotFoundError:
            resolved = candidate
        if resolved in seen or not candidate.exists() or not candidate.is_file():
            continue
        seen.add(resolved)
        unique.append(candidate)
    return unique


def materialize_includes(selection: Selection, gold_dir: Path, includes: list[str]) -> list[str]:
    notes: list[str] = []
    for index, include in enumerate(includes):
        target = gold_dir / include
        prefer_primary = index == 0
        if target.exists():
            if str(selection.row.get("form")) != "bugfix" or not prefer_primary:
                continue
        sources = candidate_include_sources(selection, include, prefer_primary=prefer_primary)
        if not sources:
            continue
        source = sources[0]
        if target.exists():
            try:
                if target.resolve() == source.resolve():
                    continue
            except FileNotFoundError:
                pass
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        notes.append(f"materialized {include} from {rel(source)}")
    return notes


def materialize_runnable_gold(
    selection: Selection,
    stage_gold: Path,
    *,
    simulator_options: tuple[str, ...] = (),
) -> tuple[Path, list[str]]:
    notes: list[str] = []
    tb_gold = choose_fixture_tb_gold(selection)
    copy_gold_contents(tb_gold, stage_gold, overwrite=False)
    if tb_gold != selection.task_dir / "gold":
        notes.append(f"testbench source: {rel(tb_gold)}")
    copy_gold_contents(selection.task_dir / "gold", stage_gold, overwrite=True)

    tb_path = choose_gold_tb(stage_gold)
    if tb_path is None:
        raise FileNotFoundError(f"no gold testbench found for {selection.row['entry_id']}/{selection.row['form']}")
    if simulator_options:
        tb_path.write_text(
            inject_simulator_options(tb_path.read_text(encoding="utf-8"), simulator_options),
            encoding="utf-8",
        )
    includes = ahdl_includes(tb_path)
    if not includes:
        raise FileNotFoundError(f"no ahdl_include found in {tb_path}")
    notes.extend(materialize_includes(selection, stage_gold, includes))
    missing = [name for name in includes if not (stage_gold / name).exists()]
    if missing:
        raise FileNotFoundError(
            f"missing included files for {selection.row['entry_id']}/{selection.row['form']}: {', '.join(missing)}"
        )
    return tb_path, notes


def is_spectre_tran_line(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and not stripped.startswith(("//", "*")) and re.match(r"^tran\b", stripped) is not None


def is_spectre_simulator_options_line(line: str) -> bool:
    stripped = line.strip()
    return (
        bool(stripped)
        and not stripped.startswith(("//", "*"))
        and re.match(r"^simulatorOptions\s+options\b", stripped) is not None
    )


def strip_line_for_manifest(line: str | None) -> str | None:
    if line is None:
        return None
    return line.strip() or None


def split_spectre_inline_comment(line: str) -> tuple[str, str, str]:
    newline = "\n" if line.endswith("\n") else ""
    body = line[:-1] if newline else line
    marker = body.find("//")
    if marker < 0:
        return body, "", newline
    return body[:marker].rstrip(), body[marker:], newline


def upsert_spectre_assignment(line: str, key: str, value: str) -> str:
    body, comment, newline = split_spectre_inline_comment(line)
    pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(key)}\s*=\s*[^ \t]+")
    replacement = f"{key}={value}"
    if pattern.search(body):
        body = pattern.sub(replacement, body, count=1)
    else:
        body = body.rstrip() + f" {replacement}"
    if comment:
        body = f"{body.rstrip()} {comment}"
    return body + newline


def extract_spectre_assignment(line: str | None, key: str) -> str | None:
    if line is None:
        return None
    match = re.search(rf"(?<![A-Za-z0-9_]){re.escape(key)}\s*=\s*([^ \t\n]+)", line)
    if match is None:
        return None
    return match.group(1).strip()


def halve_spectre_duration_token(token: str) -> str | None:
    match = re.fullmatch(
        r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)([A-Za-zµ]*)",
        token.strip(),
    )
    if match is None:
        return None
    value = float(match.group(1))
    return f"{value / 2.0:.12g}{match.group(2)}"


def extract_spectre_run_settings(tb_path: Path) -> dict[str, object]:
    lines = tb_path.read_text(encoding="utf-8").splitlines()
    tran_lines = [line.strip() for line in lines if is_spectre_tran_line(line)]
    option_lines = [line.strip() for line in lines if is_spectre_simulator_options_line(line)]
    tran_line = tran_lines[0] if tran_lines else None
    option_line = option_lines[0] if option_lines else None
    return {
        "tran_line": strip_line_for_manifest(tran_line),
        "tran_lines": tran_lines,
        "simulator_options_line": strip_line_for_manifest(option_line),
        "simulator_options_lines": option_lines,
        "maxstep": extract_spectre_assignment(tran_line, "maxstep"),
        "stop": extract_spectre_assignment(tran_line, "stop"),
        "errpreset": extract_spectre_assignment(tran_line, "errpreset"),
        "reltol": extract_spectre_assignment(option_line, "reltol"),
        "vabstol": extract_spectre_assignment(option_line, "vabstol"),
        "iabstol": extract_spectre_assignment(option_line, "iabstol"),
        "gmin": extract_spectre_assignment(option_line, "gmin"),
    }


def normalize_spectre_run_settings(tb_path: Path, *, half_maxstep: bool) -> dict[str, object]:
    lines = tb_path.read_text(encoding="utf-8").splitlines(keepends=True)
    original_settings = extract_spectre_run_settings(tb_path)
    tran_index: int | None = None
    option_index: int | None = None
    for index, line in enumerate(lines):
        if tran_index is None and is_spectre_tran_line(line):
            tran_index = index
        if option_index is None and is_spectre_simulator_options_line(line):
            option_index = index

    half_maxstep_applied = False
    half_maxstep_from = None
    half_maxstep_to = None
    if tran_index is not None:
        line = lines[tran_index]
        for key, value in NORMALIZED_SPECTRE_TRAN_OPTIONS.items():
            line = upsert_spectre_assignment(line, key, value)
        if half_maxstep:
            maxstep = extract_spectre_assignment(line, "maxstep")
            if maxstep is not None:
                halved = halve_spectre_duration_token(maxstep)
                if halved is not None:
                    line = upsert_spectre_assignment(line, "maxstep", halved)
                    half_maxstep_applied = True
                    half_maxstep_from = maxstep
                    half_maxstep_to = halved
        lines[tran_index] = line

    if option_index is None:
        option_line = "simulatorOptions options " + " ".join(
            f"{key}={value}" for key, value in NORMALIZED_SPECTRE_SIMULATOR_OPTIONS.items()
        )
        option_line += "\n"
        insert_at = tran_index if tran_index is not None else len(lines)
        lines.insert(insert_at, option_line)
    else:
        option_line = lines[option_index]
        for key, value in NORMALIZED_SPECTRE_SIMULATOR_OPTIONS.items():
            option_line = upsert_spectre_assignment(option_line, key, value)
        lines[option_index] = option_line

    tb_path.write_text("".join(lines), encoding="utf-8")
    normalized_settings = extract_spectre_run_settings(tb_path)
    return {
        **normalized_settings,
        "normalized_settings": True,
        "normalization_profile": "spectre_shared_tran_options_v1",
        "requested_tran_options": NORMALIZED_SPECTRE_TRAN_OPTIONS,
        "requested_simulator_options": NORMALIZED_SPECTRE_SIMULATOR_OPTIONS,
        "original_tran_line": original_settings.get("tran_line"),
        "original_simulator_options_line": original_settings.get("simulator_options_line"),
        "half_maxstep_requested": half_maxstep,
        "half_maxstep_applied": half_maxstep_applied,
        "half_maxstep_from": half_maxstep_from,
        "half_maxstep_to": half_maxstep_to,
    }


def build_spectre_settings_manifest(
    selection: Selection,
    spectre_mode: str,
    mode: SpectreMode,
    *,
    tb_path: Path,
    fixture_notes: list[str],
) -> dict[str, object]:
    if mode.normalize_settings:
        settings = normalize_spectre_run_settings(tb_path, half_maxstep=mode.half_maxstep)
    else:
        settings = {
            **extract_spectre_run_settings(tb_path),
            "normalized_settings": False,
            "normalization_profile": None,
            "requested_tran_options": {},
            "requested_simulator_options": {},
            "half_maxstep_requested": mode.half_maxstep,
            "half_maxstep_applied": False,
            "half_maxstep_from": None,
            "half_maxstep_to": None,
        }
    return {
        "entry_id": selection.row["entry_id"],
        "form": selection.row["form"],
        "variant": selection.row.get("variant") or "gold",
        "task_id": selection.task_id,
        "mode": spectre_mode,
        "mode_label": mode.label,
        "cli_args": list(mode.cli_args),
        "testbench_path": rel(tb_path),
        "fixture_notes": fixture_notes,
        **settings,
    }


def stage_selected_mode_task(
    selection: Selection,
    mode_id: str,
    *,
    stage_root: Path,
) -> tuple[Path, Path, Path, list[str]]:
    mode = EVAS_MODES[mode_id]
    stage_task = stage_root / mode.mode_id
    if stage_task.exists():
        shutil.rmtree(stage_task)
    stage_gold = stage_task / "gold"
    stage_gold.mkdir(parents=True, exist_ok=True)
    shutil.copy2(selection.task_dir / "meta.json", stage_task / "meta.json")
    checks_yaml = selection.task_dir / "checks.yaml"
    if checks_yaml.exists():
        shutil.copy2(checks_yaml, stage_task / "checks.yaml")
    tb_path, fixture_notes = materialize_runnable_gold(
        selection,
        stage_gold,
        simulator_options=mode.simulator_options,
    )
    includes = ahdl_includes(tb_path)
    primary_dut = stage_gold / includes[0]
    return stage_task, primary_dut, tb_path, fixture_notes


def run_evas_mode(
    selection: Selection,
    mode_id: str,
    *,
    output_root: Path,
    timeout_s: int,
) -> dict[str, object]:
    mode = EVAS_MODES[mode_id]
    stage_root = selection_output_root(output_root, selection, "staged")
    stage_task, primary_dut, tb_path, fixture_notes = stage_selected_mode_task(
        selection,
        mode_id,
        stage_root=stage_root,
    )
    result_root = selection_output_root(output_root, selection, "evas") / mode_id
    t0 = time.perf_counter()
    raw = run_case(
        stage_task,
        primary_dut,
        tb_path,
        output_root=result_root,
        timeout_s=timeout_s,
        task_id_override=selection.task_id,
        checker_task_id_override=selection.checker_id,
    )
    wall = time.perf_counter() - t0
    artifacts = raw.get("artifacts", [])
    csv_path = Path(str(artifacts[2])) if isinstance(artifacts, list) and len(artifacts) > 2 else None
    scores = raw.get("scores", {})
    if not isinstance(scores, dict):
        scores = {}
    behavior_score = float_or_none(scores.get("sim_correct"))
    behavior_available = has_behavior_check(selection.checker_id)
    behavior_ok = behavior_available and behavior_score == 1.0
    simulation_ok = (
        raw.get("status") == "PASS"
        or (
            float_or_none(scores.get("tb_compile")) == 1.0
            and csv_path is not None
            and csv_path.exists()
        )
    )
    return {
        "backend": "evas",
        "mode": mode_id,
        "phase": mode.phase,
        "status": raw.get("status"),
        "ok": raw.get("status") == "PASS",
        "simulation_ok": simulation_ok,
        "checker_id": selection.checker_id,
        "csv_path": rel(csv_path) if csv_path is not None and csv_path.exists() else None,
        "behavior_check_available": behavior_available,
        "behavior_score": behavior_score,
        "behavior_ok": behavior_ok,
        "wall_time_s": wall,
        "scores": scores,
        "timing": raw.get("timing", {}),
        "fixture_notes": fixture_notes,
        "notes": raw.get("notes", []),
        "result_root": rel(result_root),
        "stdout_tail": raw.get("stdout_tail", "")[-2000:],
    }


def copy_gold_to_run_dir(
    selection: Selection,
    run_dir: Path,
    *,
    spectre_mode: str,
    mode: SpectreMode,
) -> tuple[Path, list[str], dict[str, object]]:
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    tb_path, fixture_notes = materialize_runnable_gold(selection, run_dir)
    settings_manifest = build_spectre_settings_manifest(
        selection,
        spectre_mode,
        mode,
        tb_path=tb_path,
        fixture_notes=fixture_notes,
    )
    return tb_path, fixture_notes, settings_manifest


def run_spectre_direct(
    selection: Selection,
    spectre_mode: str,
    *,
    output_root: Path,
    timeout_s: int,
) -> dict[str, object]:
    if spectre_mode not in SPECTRE_MODES:
        raise ValueError(f"unknown Spectre mode: {spectre_mode}")
    mode = SPECTRE_MODES[spectre_mode]
    run_dir = selection_output_root(output_root, selection, "spectre") / spectre_mode
    tb_path, fixture_notes, settings_manifest = copy_gold_to_run_dir(
        selection,
        run_dir,
        spectre_mode=spectre_mode,
        mode=mode,
    )
    raw_dir = run_dir / f"{tb_path.stem}.raw"
    log_path = run_dir / "spectre.out"
    cmd = [
        "spectre",
        "-64",
        tb_path.name,
        "+escchars",
        "+log",
        str(log_path),
        "-format",
        "psfascii",
        "-raw",
        str(raw_dir),
        *mode.cli_args,
        "+lqtimeout",
        "900",
        "-maxw",
        "5",
        "-maxn",
        "5",
        "+logstatus",
    ]
    settings_manifest["command"] = " ".join(cmd)
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            cwd=run_dir,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
        wall = time.perf_counter() - t0
    except subprocess.TimeoutExpired as exc:
        wall = time.perf_counter() - t0
        return {
            "backend": "spectre",
            "mode": spectre_mode,
            "status": "timeout",
            "ok": False,
            "simulation_ok": False,
            "wall_time_s": wall,
            "returncode": None,
            "timing": {},
            "command": " ".join(cmd),
            "spectre_settings": settings_manifest,
            "fixture_notes": fixture_notes,
            "result_root": rel(run_dir),
            "stdout_tail": ((exc.stdout or "") + "\n" + (exc.stderr or ""))[-2000:],
        }

    combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
    if log_path.exists():
        combined = combined + "\n" + log_path.read_text(encoding="utf-8", errors="replace")
    timing = parse_spectre_timing(combined)
    ok = proc.returncode == 0 and raw_dir.exists()
    csv_path = run_dir / "tran_spectre.csv"
    parse_info: dict[str, object] | None = None
    parse_notes: list[str] = []
    if ok:
        try:
            parse_info = write_spectre_psf_csv(raw_dir, csv_path)
        except Exception as exc:  # noqa: BLE001 - record parser failures in the artifact.
            parse_notes.append(f"{type(exc).__name__}: {exc}")
    behavior = evaluate_csv_behavior(
        selection.checker_id,
        csv_path if csv_path.exists() else None,
        timeout_s=timeout_s,
    )
    simulation_ok = ok and csv_path.exists()
    return {
        "backend": "spectre",
        "mode": spectre_mode,
        "status": "PASS" if simulation_ok else "FAIL",
        "ok": simulation_ok and behavior.get("ok") is True,
        "simulation_ok": simulation_ok,
        "checker_id": selection.checker_id,
        "csv_path": rel(csv_path) if csv_path.exists() else None,
        "psf_parse": parse_info,
        "behavior_check_available": behavior["check_available"],
        "behavior_score": behavior["score"],
        "behavior_ok": behavior["ok"],
        "wall_time_s": wall,
        "returncode": proc.returncode,
        "timing": timing,
        "command": " ".join(cmd),
        "spectre_settings": settings_manifest,
        "result_root": rel(run_dir),
        "fixture_notes": fixture_notes,
        "notes": parse_notes + list(behavior["notes"]),
        "stdout_tail": combined[-2000:],
    }


def run_work_item(
    item: WorkItem,
    *,
    output_root: Path,
    timeout_s: int,
) -> dict[str, object]:
    t0 = time.perf_counter()
    try:
        if item.backend == "spectre":
            result = run_spectre_direct(
                item.selection,
                item.mode,
                output_root=output_root,
                timeout_s=timeout_s,
            )
        elif item.backend == "evas":
            result = run_evas_mode(
                item.selection,
                item.mode,
                output_root=output_root,
                timeout_s=timeout_s,
            )
        else:
            raise ValueError(f"unknown backend: {item.backend}")
    except Exception as exc:  # noqa: BLE001 - matrix jobs must record failures.
        result = {
            "backend": item.backend,
            "mode": item.mode,
            "status": "ERROR",
            "ok": False,
            "simulation_ok": False,
            "wall_time_s": time.perf_counter() - t0,
            "notes": [f"{type(exc).__name__}: {exc}"],
            "stdout_tail": "",
        }
    result["entry_id"] = item.selection.row["entry_id"]
    result["form"] = item.selection.row["form"]
    result["variant"] = item.selection.row.get("variant") or "gold"
    result["task_id"] = item.selection.task_id
    return result


def build_work_items(
    selections: list[Selection],
    *,
    evas_modes: list[str],
    spectre_modes: list[str],
) -> list[WorkItem]:
    items: list[WorkItem] = []
    for selection in selections:
        for spectre_mode in spectre_modes:
            items.append(
                WorkItem(
                    index=len(items),
                    selection=selection,
                    backend="spectre",
                    mode=spectre_mode,
                )
            )
        for evas_mode in evas_modes:
            items.append(
                WorkItem(
                    index=len(items),
                    selection=selection,
                    backend="evas",
                    mode=evas_mode,
                )
            )
    return items


def run_work_items(
    items: list[WorkItem],
    *,
    output_root: Path,
    timeout_s: int,
    jobs: int,
) -> list[dict[str, object]]:
    ordered: list[dict[str, object] | None] = [None] * len(items)
    if jobs <= 1:
        for item in items:
            result = run_work_item(item, output_root=output_root, timeout_s=timeout_s)
            ordered[item.index] = result
            print_progress(item.index + 1, len(items), result)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
            future_map = {
                executor.submit(
                    run_work_item,
                    item,
                    output_root=output_root,
                    timeout_s=timeout_s,
                ): item
                for item in items
            }
            for completed, future in enumerate(concurrent.futures.as_completed(future_map), start=1):
                item = future_map[future]
                result = future.result()
                ordered[item.index] = result
                print_progress(completed, len(items), result)
    return [result for result in ordered if result is not None]


def print_progress(completed: int, total: int, result: dict[str, object]) -> None:
    wall = float_or_none(result.get("wall_time_s"))
    wall_text = "?" if wall is None else f"{wall:.3f}s"
    print(
        "[{completed}/{total}] {entry}/{form} {backend}/{mode}: {status} {wall}".format(
            completed=completed,
            total=total,
            entry=result.get("entry_id", ""),
            form=result.get("form", ""),
            backend=result.get("backend", ""),
            mode=result.get("mode", ""),
            status=result.get("status", ""),
            wall=wall_text,
        ),
        flush=True,
    )


def resolve_artifact_path(value: object) -> Path | None:
    if not value:
        return None
    path = Path(str(value))
    if path.is_absolute():
        return path
    return ROOT / path


def compare_csv_pair(task_id: str, left_csv: Path | None, right_csv: Path | None) -> dict[str, object]:
    if left_csv is None or right_csv is None:
        return {
            "status": "blocked",
            "reason": "missing csv",
        }
    try:
        return compare_waveforms(task_id, left_csv, right_csv)
    except Exception as exc:  # noqa: BLE001 - keep gate failures data-bearing.
        return {
            "status": "blocked",
            "reason": f"{type(exc).__name__}: {exc}",
        }


def classify_parity(parity: dict[str, object]) -> tuple[str, str | None]:
    status = str(parity.get("status", "blocked"))
    if status in {"passed", "self"}:
        return "pass", None
    reason = str(parity.get("reason") or status)
    if status == "blocked":
        return "blocked", reason
    return "fail", reason


REFERENCE_SPECTRE_MODE_PRIORITY = (
    "spectre_reference_strict_primary",
    "reference_strict_primary",
    "classic",
)


def result_mode_label(result: dict[str, object]) -> str:
    return f"{result.get('backend')}/{result.get('mode')}"


def apply_equivalence_gates(results: list[dict[str, object]], spectre_modes: list[str]) -> None:
    grouped: dict[tuple[str, str, str], dict[tuple[str, str], dict[str, object]]] = defaultdict(dict)
    for result in results:
        key = (
            str(result["entry_id"]),
            str(result["form"]),
            str(result.get("variant") or "gold"),
            str(result["task_id"]),
        )
        grouped[key][(str(result["backend"]), str(result["mode"]))] = result

    for (_entry_id, _form, _variant, task_id), cells in grouped.items():
        strict = cells.get(("evas", "strict_current"))
        strict_csv = resolve_artifact_path(strict.get("csv_path")) if strict else None
        for (backend, mode), result in cells.items():
            if backend != "evas":
                continue

            reasons: list[str] = []
            blocked: list[str] = []
            strict_parity: dict[str, object]
            spectre_parity: dict[str, object] = {}

            if result.get("simulation_ok") is not True:
                reasons.append("candidate_simulation_not_ok")
            if result.get("behavior_check_available") is not True:
                blocked.append("candidate_no_behavior_checker")
            elif result.get("behavior_ok") is not True:
                reasons.append("candidate_behavior_check_failed")

            candidate_csv = resolve_artifact_path(result.get("csv_path"))
            if mode == "strict_current":
                strict_parity = {"status": "self"}
            elif strict is None or strict.get("simulation_ok") is not True or strict_csv is None:
                strict_parity = {
                    "status": "blocked",
                    "reason": "missing strict_current EVAS reference",
                }
            else:
                strict_parity = compare_csv_pair(task_id, candidate_csv, strict_csv)

            strict_class, strict_reason = classify_parity(strict_parity)
            if strict_class == "blocked":
                blocked.append(f"strict_evas_parity:{strict_reason}")
            elif strict_class == "fail":
                reasons.append(f"strict_evas_parity:{strict_reason}")

            for spectre_mode in spectre_modes:
                spectre = cells.get(("spectre", spectre_mode))
                if spectre is None or spectre.get("simulation_ok") is not True:
                    parity = {
                        "status": "blocked",
                        "reason": "missing Spectre reference",
                    }
                elif spectre.get("behavior_check_available") is not True:
                    parity = {
                        "status": "blocked",
                        "reason": "spectre_no_behavior_checker",
                    }
                elif spectre.get("behavior_ok") is not True:
                    parity = {
                        "status": "needs_review",
                        "reason": "spectre_behavior_check_failed",
                    }
                else:
                    spectre_csv = resolve_artifact_path(spectre.get("csv_path"))
                    parity = compare_csv_pair(task_id, candidate_csv, spectre_csv)
                spectre_parity[spectre_mode] = parity
                parity_class, parity_reason = classify_parity(parity)
                if parity_class == "blocked":
                    blocked.append(f"spectre_{spectre_mode}_parity:{parity_reason}")
                elif parity_class == "fail":
                    reasons.append(f"spectre_{spectre_mode}_parity:{parity_reason}")

            status = "PASS"
            if reasons:
                status = "FAIL"
            elif blocked:
                status = "BLOCKED"
            gate = {
                "status": status,
                "reasons": reasons,
                "blocked": blocked,
                "strict_evas_parity": strict_parity,
                "spectre_parity": spectre_parity,
            }
            result["equivalence_gate"] = gate
            result["accuracy_gate"] = gate  # Legacy artifact key; prefer equivalence_gate.


def reference_comparisons(results: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    summary: list[dict[str, object]] = []
    grouped: dict[tuple[str, str, str, str], dict[tuple[str, str], dict[str, object]]] = defaultdict(dict)
    for result in results:
        key = (
            str(result["entry_id"]),
            str(result["form"]),
            str(result.get("variant") or "gold"),
            str(result["task_id"]),
        )
        grouped[key][(str(result["backend"]), str(result["mode"]))] = result

    for (entry_id, form, variant, task_id), cells in sorted(grouped.items()):
        reference: dict[str, object] | None = None
        for mode in REFERENCE_SPECTRE_MODE_PRIORITY:
            candidate = cells.get(("spectre", mode))
            if candidate is not None:
                reference = candidate
                break
        if reference is None:
            continue
        reference_csv = resolve_artifact_path(reference.get("csv_path"))
        if reference.get("simulation_ok") is not True or reference_csv is None:
            continue

        for (_backend, _mode), candidate in sorted(cells.items()):
            if candidate is reference:
                continue
            candidate_csv = resolve_artifact_path(candidate.get("csv_path"))
            comparison = compare_csv_pair(task_id, candidate_csv, reference_csv)
            status = str(comparison.get("status", "blocked"))
            rows.append(
                {
                    "entry_id": entry_id,
                    "form": form,
                    "variant": variant,
                    "task_id": task_id,
                    "candidate": result_mode_label(candidate),
                    "reference": result_mode_label(reference),
                    "candidate_simulation_ok": candidate.get("simulation_ok") is True,
                    "candidate_behavior_ok": candidate.get("behavior_ok"),
                    "reference_behavior_ok": reference.get("behavior_ok"),
                    "status": status,
                    "max_abs_v": comparison.get("max_abs_v"),
                    "max_rmse_v": comparison.get("max_rmse_v"),
                    "mean_relative_rms_error": comparison.get("mean_relative_rms_error"),
                    "max_relative_rms_error": comparison.get("max_relative_rms_error"),
                    "signals_compared": comparison.get("signals_compared"),
                    "reason": comparison.get("reason"),
                    "comparison": comparison,
                }
            )

    by_candidate: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_candidate[str(row["candidate"])].append(row)
    for candidate, candidate_rows in sorted(by_candidate.items()):
        comparable = [
            row for row in candidate_rows if str(row.get("status")) in {"passed", "needs_review"}
        ]
        max_abs_values = [
            float(row["max_abs_v"])
            for row in comparable
            if float_or_none(row.get("max_abs_v")) is not None
        ]
        max_rel_values = [
            float(row["max_relative_rms_error"])
            for row in comparable
            if float_or_none(row.get("max_relative_rms_error")) is not None
        ]
        summary.append(
            {
                "candidate": candidate,
                "runs": len(candidate_rows),
                "passed_count": sum(1 for row in candidate_rows if row.get("status") == "passed"),
                "needs_review_count": sum(1 for row in candidate_rows if row.get("status") == "needs_review"),
                "blocked_count": sum(1 for row in candidate_rows if row.get("status") == "blocked"),
                "max_abs_v_worst": max(max_abs_values) if max_abs_values else None,
                "max_relative_rms_error_worst": max(max_rel_values) if max_rel_values else None,
            }
        )
    return rows, summary


def summarize(results: list[dict[str, object]]) -> dict[str, object]:
    by_backend_mode: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for result in results:
        by_backend_mode[(str(result["backend"]), str(result["mode"]))].append(result)

    mode_summary: list[dict[str, object]] = []
    for (backend, mode), rows in sorted(by_backend_mode.items()):
        walls = [float(row["wall_time_s"]) for row in rows if float_or_none(row.get("wall_time_s")) is not None]
        mode_summary.append(
            {
                "backend": backend,
                "mode": mode,
                "runs": len(rows),
                "simulation_ok_count": sum(1 for row in rows if row.get("simulation_ok") is True),
                "pass_count": sum(1 for row in rows if row.get("ok") is True),
                "nonpass_count": sum(1 for row in rows if row.get("ok") is not True),
                "total_wall_time_s": sum(walls),
                "mean_wall_time_s": (sum(walls) / len(walls)) if walls else None,
                "geomean_wall_time_s": geomean(walls),
            }
        )

    speedups: list[dict[str, object]] = []
    equivalence_gated_speedups: list[dict[str, object]] = []
    grouped: dict[tuple[str, str, str, str], dict[tuple[str, str], dict[str, object]]] = defaultdict(dict)
    for result in results:
        key = (
            str(result["entry_id"]),
            str(result["form"]),
            str(result.get("variant") or "gold"),
            str(result["task_id"]),
        )
        grouped[key][(str(result["backend"]), str(result["mode"]))] = result
    for (entry_id, form, variant, task_id), cells in sorted(grouped.items()):
        for spectre_mode in sorted({mode for backend, mode in cells if backend == "spectre"}):
            spectre = cells.get(("spectre", spectre_mode))
            if not spectre or spectre.get("simulation_ok") is not True:
                continue
            spectre_wall = float(spectre["wall_time_s"])
            for evas_mode in sorted({mode for backend, mode in cells if backend == "evas"}):
                evas = cells.get(("evas", evas_mode))
                if not evas or evas.get("simulation_ok") is not True:
                    continue
                evas_wall = float(evas["wall_time_s"])
                speedups.append(
                    {
                        "entry_id": entry_id,
                        "form": form,
                        "variant": variant,
                        "task_id": task_id,
                        "spectre_mode": spectre_mode,
                        "evas_mode": evas_mode,
                        "spectre_wall_time_s": spectre_wall,
                        "evas_wall_time_s": evas_wall,
                        "spectre_over_evas_speedup": spectre_wall / evas_wall if evas_wall > 0 else None,
                    }
                )
                gate = evas.get("equivalence_gate", evas.get("accuracy_gate", {}))
                if isinstance(gate, dict) and gate.get("status") == "PASS":
                    equivalence_gated_speedups.append(speedups[-1])

    gate_summary: list[dict[str, object]] = []
    by_evas_mode: dict[str, list[dict[str, object]]] = defaultdict(list)
    for result in results:
        if result.get("backend") == "evas":
            by_evas_mode[str(result["mode"])].append(result)
    for mode, rows in sorted(by_evas_mode.items()):
        statuses = []
        for row in rows:
            gate = row.get("equivalence_gate", row.get("accuracy_gate", {}))
            statuses.append(str(gate.get("status", "MISSING")) if isinstance(gate, dict) else "MISSING")
        gate_summary.append(
            {
                "mode": mode,
                "runs": len(rows),
                "pass_count": statuses.count("PASS"),
                "fail_count": statuses.count("FAIL"),
                "blocked_count": statuses.count("BLOCKED"),
                "missing_count": statuses.count("MISSING"),
            }
        )

    equivalence_gated_geomean = geomean(
        [
            float(row["spectre_over_evas_speedup"])
            for row in equivalence_gated_speedups
            if float_or_none(row.get("spectre_over_evas_speedup")) is not None
        ]
    )
    ref_comparison_rows, ref_comparison_summary = reference_comparisons(results)
    return {
        "mode_summary": mode_summary,
        "equivalence_gate_summary": gate_summary,
        "accuracy_gate_summary": gate_summary,
        "speedups": speedups,
        "equivalence_gated_speedups": equivalence_gated_speedups,
        "accuracy_gated_speedups": equivalence_gated_speedups,
        "geomean_spectre_over_evas_speedup": geomean(
            [
                float(row["spectre_over_evas_speedup"])
                for row in speedups
                if float_or_none(row.get("spectre_over_evas_speedup")) is not None
            ]
        ),
        "geomean_equivalence_gated_spectre_over_evas_speedup": equivalence_gated_geomean,
        "geomean_accuracy_gated_spectre_over_evas_speedup": equivalence_gated_geomean,
        "reference_comparisons": ref_comparison_rows,
        "reference_comparison_summary": ref_comparison_summary,
    }


def audit_fixture_materialization(
    selections: list[Selection],
    *,
    output_root: Path,
) -> dict[str, object]:
    results: list[dict[str, object]] = []
    for selection in selections:
        audit_dir = selection_output_root(output_root, selection, "fixture_audit")
        if audit_dir.exists():
            shutil.rmtree(audit_dir)
        record: dict[str, object] = {
            "entry_id": selection.row["entry_id"],
            "form": selection.row["form"],
            "variant": selection.row.get("variant") or "gold",
            "task_id": selection.task_id,
            "result_root": rel(audit_dir),
            "ok": False,
            "status": "ERROR",
            "notes": [],
        }
        try:
            tb_path, fixture_notes = materialize_runnable_gold(selection, audit_dir)
            includes = ahdl_includes(tb_path)
            missing = [name for name in includes if not (audit_dir / name).exists()]
            record.update(
                {
                    "tb_path": rel(tb_path),
                    "includes": includes,
                    "fixture_notes": fixture_notes,
                    "missing_includes": missing,
                    "ok": not missing,
                    "status": "PASS" if not missing else "FAIL",
                    "notes": [] if not missing else [f"missing includes: {', '.join(missing)}"],
                }
            )
        except Exception as exc:  # noqa: BLE001 - audit should enumerate every fixture defect.
            record["notes"] = [f"{type(exc).__name__}: {exc}"]
        results.append(record)

    failures = [row for row in results if row.get("ok") is not True]
    return {
        "schema_version": "same-server-fixture-audit.v1",
        "artifact_kind": "vabench_release_fixture_materialization_audit",
        "date": date.today().isoformat(),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "selected_rows": len(selections),
        "output_root": rel(output_root),
        "pass_count": len(results) - len(failures),
        "fail_count": len(failures),
        "results": results,
    }


def write_fixture_audit_markdown(path: Path, artifact: dict[str, object]) -> None:
    lines = [
        "# vaBench Fixture Materialization Audit",
        "",
        f"Date: {artifact['date']}",
        f"Selected rows: {artifact['selected_rows']}",
        f"PASS: {artifact['pass_count']}",
        f"FAIL: {artifact['fail_count']}",
        f"Output root: `{artifact['output_root']}`",
        "",
        "| Entry | Form | Variant | Task | Status | Notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in artifact["results"]:
        notes = ", ".join(str(item) for item in row.get("notes", []))
        lines.append(
            "| `{entry}` | `{form}` | `{variant}` | `{task}` | `{status}` | {notes} |".format(
                entry=row["entry_id"],
                form=row["form"],
                variant=row.get("variant") or "gold",
                task=row["task_id"],
                status=row["status"],
                notes=notes or "-",
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def markdown_table_cell(value: object, *, code: bool = False) -> str:
    if value is None:
        return "-"
    text = str(value).replace("\n", "<br>").replace("|", "\\|").strip()
    if not text:
        return "-"
    return f"`{text}`" if code else text


def write_markdown(path: Path, artifact: dict[str, object]) -> None:
    summary = artifact["summary"]
    lines = [
        "# Same-Server EVAS/Spectre Speed",
        "",
        f"Date: {artifact['date']}",
        f"Claim allowed: `{artifact['claim_allowed']}`",
        f"Reason: {artifact['no_claim_reason']}",
        "",
        "## Scope",
        "",
        f"- Host: `{artifact['host']}`",
        f"- Selected rows: {artifact['selected_rows']}",
        f"- Jobs: {artifact['jobs']}",
        f"- EVAS modes: `{', '.join(artifact['evas_modes'])}`",
        f"- Spectre modes: `{', '.join(artifact['spectre_modes'])}`",
        f"- Output root: `{artifact['output_root']}`",
        "",
        "## Mode Summary",
        "",
        "| Backend | Mode | Runs | Sim OK | Behavior PASS | Behavior non-PASS | Total wall s | Mean wall s |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary["mode_summary"]:
        lines.append(
            "| {backend} | {mode} | {runs} | {simulation_ok_count} | {pass_count} | {nonpass_count} | {total:.3f} | {mean} |".format(
                backend=row["backend"],
                mode=row["mode"],
                runs=row["runs"],
                simulation_ok_count=row.get("simulation_ok_count", "-"),
                pass_count=row["pass_count"],
                nonpass_count=row["nonpass_count"],
                total=float(row["total_wall_time_s"]),
                mean="None" if row["mean_wall_time_s"] is None else f"{float(row['mean_wall_time_s']):.3f}",
            )
        )

    if summary.get("reference_comparison_summary"):
        lines.extend(
            [
                "",
                "## Reference Comparison Summary",
                "",
                "Each candidate is compared against the same-row strict Spectre reference. "
                "The waveform status uses the simulator-equivalence policy from `run_gold_dual_suite.py`.",
                "",
                "| Candidate | Runs | Passed | Needs review | Blocked | Worst max abs V | Worst max relative RMS error |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in summary["reference_comparison_summary"]:
            lines.append(
                "| {candidate} | {runs} | {passed} | {review} | {blocked} | {max_abs} | {max_rel} |".format(
                    candidate=markdown_table_cell(row["candidate"], code=True),
                    runs=row["runs"],
                    passed=row["passed_count"],
                    review=row["needs_review_count"],
                    blocked=row["blocked_count"],
                    max_abs="-"
                    if row["max_abs_v_worst"] is None
                    else f"{float(row['max_abs_v_worst']):.6g}",
                    max_rel="-"
                    if row["max_relative_rms_error_worst"] is None
                    else f"{float(row['max_relative_rms_error_worst']):.6g}",
                )
            )

    if summary.get("reference_comparisons"):
        lines.extend(
            [
                "",
                "## Per-Row Reference Comparisons",
                "",
                "| Entry | Form | Variant | Candidate | Reference | Behavior OK | Waveform | Max abs V | Max relative RMS error | Signals |",
                "| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: |",
            ]
        )
        for row in summary["reference_comparisons"]:
            lines.append(
                "| `{entry}` | `{form}` | `{variant}` | {candidate} | {reference} | `{behavior}` | `{status}` | {max_abs} | {max_rel} | {signals} |".format(
                    entry=row["entry_id"],
                    form=row["form"],
                    variant=row.get("variant") or "gold",
                    candidate=markdown_table_cell(row["candidate"], code=True),
                    reference=markdown_table_cell(row["reference"], code=True),
                    behavior=row.get("candidate_behavior_ok"),
                    status=row["status"],
                    max_abs="-"
                    if row["max_abs_v"] is None
                    else f"{float(row['max_abs_v']):.6g}",
                    max_rel="-"
                    if row["max_relative_rms_error"] is None
                    else f"{float(row['max_relative_rms_error']):.6g}",
                    signals=row.get("signals_compared") or "-",
                )
            )

    spectre_results = [row for row in artifact["results"] if row.get("backend") == "spectre"]
    if spectre_results:
        lines.extend(
            [
                "",
                "## Spectre Run Settings",
                "",
                "This table records the final staged testbench settings used by Spectre. "
                "For normalized precision-ranking modes, `tran` and `simulatorOptions` are rewritten "
                "before Spectre is launched; speed-baseline modes keep the staged testbench unchanged.",
                "",
                "| Entry | Form | Variant | Mode | Normalized | CLI args | tran line | simulatorOptions line | Result root |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for result in spectre_results:
            settings = result.get("spectre_settings", {})
            if not isinstance(settings, dict):
                settings = {}
            lines.append(
                "| `{entry}` | `{form}` | `{variant}` | `{mode}` | `{normalized}` | {cli_args} | {tran_line} | {options_line} | {result_root} |".format(
                    entry=result["entry_id"],
                    form=result["form"],
                    variant=result.get("variant") or "gold",
                    mode=result["mode"],
                    normalized=settings.get("normalized_settings"),
                    cli_args=markdown_table_cell(" ".join(str(item) for item in settings.get("cli_args", [])), code=True),
                    tran_line=markdown_table_cell(settings.get("tran_line"), code=True),
                    options_line=markdown_table_cell(settings.get("simulator_options_line"), code=True),
                    result_root=markdown_table_cell(result.get("result_root"), code=True),
                )
            )

    lines.extend(
        [
            "",
            "## Spectre-Equivalence Gate Summary",
            "",
            "These gates check whether EVAS preserves task behavior and stays within "
            "accepted Spectre-equivalent waveform tolerance. They are not a higher-than-Spectre "
            "precision target.",
            "",
            "| EVAS mode | Runs | Gate PASS | Gate FAIL | Gate BLOCKED | Gate missing |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in summary.get("equivalence_gate_summary") or summary.get("accuracy_gate_summary", []):
        lines.append(
            "| {mode} | {runs} | {passed} | {failed} | {blocked} | {missing} |".format(
                mode=row["mode"],
                runs=row["runs"],
                passed=row["pass_count"],
                failed=row["fail_count"],
                blocked=row["blocked_count"],
                missing=row["missing_count"],
            )
        )

    lines.extend(
        [
            "",
            "## Per-Row Spectre-Equivalence Gates",
            "",
            "| Entry | Form | Variant | EVAS mode | Gate | Reasons | Blocked |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for result in artifact["results"]:
        if result.get("backend") != "evas":
            continue
        gate = result.get("equivalence_gate", result.get("accuracy_gate", {}))
        if not isinstance(gate, dict):
            gate = {}
        reasons = ", ".join(str(item) for item in gate.get("reasons", []))
        blocked = ", ".join(str(item) for item in gate.get("blocked", []))
        lines.append(
            "| `{entry}` | `{form}` | `{variant}` | `{mode}` | `{status}` | {reasons} | {blocked} |".format(
                entry=result["entry_id"],
                form=result["form"],
                variant=result.get("variant") or "gold",
                mode=result["mode"],
                status=gate.get("status", "MISSING"),
                reasons=reasons or "-",
                blocked=blocked or "-",
            )
        )

    lines.extend(
        [
            "",
            "## Simulation-Only Speedups",
            "",
            "| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |",
            "| --- | --- | --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in summary["speedups"]:
        speedup = row["spectre_over_evas_speedup"]
        lines.append(
            "| `{entry}` | `{form}` | `{variant}` | `{smode}` | `{emode}` | {sw:.3f} | {ew:.3f} | {sp} |".format(
                entry=row["entry_id"],
                form=row["form"],
                variant=row.get("variant") or "gold",
                smode=row["spectre_mode"],
                emode=row["evas_mode"],
                sw=float(row["spectre_wall_time_s"]),
                ew=float(row["evas_wall_time_s"]),
                sp="None" if speedup is None else f"{float(speedup):.3f}",
            )
        )

    lines.extend(
        [
            "",
            "## Spectre-Equivalence-Gated Speedups",
            "",
            "| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |",
            "| --- | --- | --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in summary.get("equivalence_gated_speedups") or summary.get("accuracy_gated_speedups", []):
        speedup = row["spectre_over_evas_speedup"]
        lines.append(
            "| `{entry}` | `{form}` | `{variant}` | `{smode}` | `{emode}` | {sw:.3f} | {ew:.3f} | {sp} |".format(
                entry=row["entry_id"],
                form=row["form"],
                variant=row.get("variant") or "gold",
                smode=row["spectre_mode"],
                emode=row["evas_mode"],
                sw=float(row["spectre_wall_time_s"]),
                ew=float(row["evas_wall_time_s"]),
                sp="None" if speedup is None else f"{float(speedup):.3f}",
            )
        )

    lines.extend(
        [
            "",
            "## Interpretation Guardrails",
            "",
            "- Speedups use `simulation_ok`, so rows without a behavior checker can still contribute timing if the simulator produced waveforms.",
            "- Equivalence-gated speedups require candidate behavior pass, strict-EVAS parity, and parity to every selected Spectre mode.",
            "- `spectre/ax_speed` is the main fast Spectre speed baseline; `spectre/ax` remains a legacy alias for the same command-line preset.",
            "- `spectre/ax_normalized` keeps `+preset=ax +mt` but rewrites the staged testbench to the shared precision settings before launch.",
            "- `spectre/reference_strict_primary` uses the same staged `tran`/`simulatorOptions` settings without runner-added AX preset.",
            "- `spectre/classic` is the stricter non-X reference path; AX/classic waveform differences are expected and should anchor EVAS tolerance rather than imply a single exact waveform truth.",
            "- The waveform gate is an acceptance tolerance for Spectre-equivalent behavioral output, not a requirement that EVAS exceed Spectre precision.",
            "- Cold Spectre runs include AHDL CMI compilation; warm-cache repetitions should be reported separately.",
            "- A `BLOCKED` gate is not evidence of wrong behavior; it means the checker or reference evidence is incomplete.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Run direct same-server EVAS/Spectre timing on vaBench release rows.")
    ap.add_argument("--speed-artifact", default=str(SPEED_ARTIFACT_JSON))
    ap.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    ap.add_argument("--report-json", default=str(DEFAULT_REPORT_JSON))
    ap.add_argument("--report-md", default=str(DEFAULT_REPORT_MD))
    ap.add_argument("--suite", choices=("slow-outliers", "all", "top-wall"), default="slow-outliers")
    ap.add_argument("--entry", action="append", default=[])
    ap.add_argument("--form", action="append", default=[])
    ap.add_argument("--limit", type=int, default=2)
    ap.add_argument("--evas-mode", action="append", choices=tuple(EVAS_MODES), default=[])
    ap.add_argument("--spectre-mode", action="append", choices=tuple(SPECTRE_MODES), default=[])
    ap.add_argument("--skip-evas", action="store_true", help="Run Spectre modes only; useful for settings smoke tests.")
    ap.add_argument("--timeout-s", type=int, default=300)
    ap.add_argument("--jobs", type=int, default=1, help="Parallel backend/mode jobs. Use 8 for matrix runs on thu-sui.")
    ap.add_argument(
        "--audit-fixtures-only",
        action="store_true",
        help="Materialize selected release fixtures and verify testbench ahdl_include files exist without running simulators.",
    )
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    prepend_current_python_bin_to_path()
    output_root = Path(args.output_root)
    if not output_root.is_absolute():
        output_root = ROOT / output_root
    output_root.mkdir(parents=True, exist_ok=True)
    report_json = Path(args.report_json)
    if not report_json.is_absolute():
        report_json = ROOT / report_json
    report_md = Path(args.report_md)
    if not report_md.is_absolute():
        report_md = ROOT / report_md

    selected_rows = select_rows(
        load_speed_rows(Path(args.speed_artifact).resolve()),
        suite=args.suite,
        entries=set(args.entry) if args.entry else None,
        forms=set(args.form) if args.form else None,
        limit=args.limit,
    )
    selections = [prepare_selection(row) for row in selected_rows]
    evas_modes = [] if args.skip_evas else (args.evas_mode or ["strict_current", "profile_fast_skip_source_error_control"])
    spectre_modes = args.spectre_mode or ["ax"]

    if args.audit_fixtures_only:
        artifact = audit_fixture_materialization(selections, output_root=output_root)
        report_json.parent.mkdir(parents=True, exist_ok=True)
        report_json.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
        write_fixture_audit_markdown(report_md, artifact)
        print(
            "wrote fixture audit artifact: "
            f"rows={artifact['selected_rows']}; fail={artifact['fail_count']}; report={rel(report_json)}"
        )
        return 0 if artifact["fail_count"] == 0 else 1

    work_items = build_work_items(
        selections,
        evas_modes=evas_modes,
        spectre_modes=spectre_modes,
    )
    results = run_work_items(
        work_items,
        output_root=output_root,
        timeout_s=args.timeout_s,
        jobs=max(1, args.jobs),
    )
    apply_equivalence_gates(results, spectre_modes)

    artifact = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": ARTIFACT_KIND,
        "date": date.today().isoformat(),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "claim_allowed": False,
        "no_claim_reason": NO_CLAIM_REASON,
        "evas_only_no_claim_reason": EVAS_ONLY_NO_CLAIM_REASON,
        "host": subprocess.run(["hostname"], capture_output=True, text=True, check=False).stdout.strip(),
        "selected_rows": len(selections),
        "jobs": max(1, args.jobs),
        "evas_modes": evas_modes,
        "spectre_modes": spectre_modes,
        "output_root": rel(output_root),
        "results": results,
        "summary": summarize(results),
    }
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    write_markdown(report_md, artifact)
    print(
        "wrote same-server speed artifact: "
        f"rows={len(selections)}; evas_modes={','.join(evas_modes)}; "
        f"spectre_modes={','.join(spectre_modes)}; report={rel(report_json)}"
    )
    return 0 if all(result.get("simulation_ok") is True for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
