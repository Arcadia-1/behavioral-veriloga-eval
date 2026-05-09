#!/usr/bin/env python3
"""Tag benchmark tasks with Verilog-A/Spectre features for targeted regression.

The output is an analysis artifact, not a benchmark mutation.  It is used by
`select_affected_tasks.py` to choose a focused regression set after a kernel,
preflight, parser, source, or checker change.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BENCH = ROOT / "benchmark-vabench-main-v1"


FEATURE_PATTERNS: dict[str, list[re.Pattern[str]]] = {
    "uses_cross": [re.compile(r"@\s*\(\s*cross\s*\(", re.I), re.compile(r"\bcross\s*\(", re.I)],
    "uses_above": [re.compile(r"@\s*\(\s*above\s*\(", re.I), re.compile(r"\babove\s*\(", re.I)],
    "uses_timer": [re.compile(r"@\s*\(\s*timer\s*\(", re.I), re.compile(r"\btimer\s*\(", re.I)],
    "uses_initial_step": [re.compile(r"\binitial_step\b", re.I)],
    "uses_final_step": [re.compile(r"\bfinal_step\b", re.I)],
    "uses_transition": [re.compile(r"\btransition\s*\(", re.I)],
    "uses_slew": [re.compile(r"\bslew\s*\(", re.I)],
    "uses_idt": [re.compile(r"\bidt\s*\(", re.I), re.compile(r"\bidtmod\s*\(", re.I)],
    "uses_abstime": [re.compile(r"\$abstime\b"), re.compile(r"\babstime\b")],
    "uses_bound_step": [re.compile(r"\$bound_step\s*\(", re.I)],
    "uses_fileio": [re.compile(r"\$(?:fopen|fclose|fwrite|fstrobe|fdisplay)\s*\(", re.I)],
    "uses_random": [re.compile(r"\$(?:rdist_|random)", re.I)],
    "uses_math_exp_log": [re.compile(r"\b(?:exp|ln|log|sqrt|pow)\s*\(", re.I), re.compile(r"\$(?:exp|ln|log|sqrt|pow)\s*\(", re.I)],
    "uses_bitwise": [re.compile(r"(?:<<|>>|\^|\||&)")],
    "uses_integer_array": [re.compile(r"\binteger\s+\w+\s*\[", re.I)],
    "uses_dynamic_vector_index": [re.compile(r"\[[A-Za-z_][A-Za-z0-9_$]*\]")],
    "uses_conditional": [re.compile(r"\bif\s*\(", re.I), re.compile(r"\bcase\s*\(", re.I)],
    "uses_loop": [re.compile(r"\bfor\s*\(", re.I), re.compile(r"\bwhile\s*\(", re.I)],
    "uses_contribution": [re.compile(r"<\+")],
    "uses_pulse_source": [re.compile(r"\bvsource\b[^\n]*\btype\s*=\s*pulse\b", re.I)],
    "uses_pwl_source": [re.compile(r"\bvsource\b[^\n]*\btype\s*=\s*pwl\b", re.I), re.compile(r"\bwave\s*=\s*\[", re.I)],
    "uses_sine_source": [re.compile(r"\bvsource\b[^\n]*\btype\s*=\s*sine\b", re.I)],
    "uses_dc_source": [re.compile(r"\bvsource\b[^\n]*\btype\s*=\s*dc\b", re.I)],
    "uses_save_statement": [re.compile(r"^\s*save\b", re.I | re.M)],
    "uses_ahdl_include": [re.compile(r"^\s*ahdl_include\b", re.I | re.M)],
}


CHANGE_FEATURES: dict[str, list[str]] = {
    "cross": ["uses_cross"],
    "cross_on_pulse": ["uses_cross_on_pulse"],
    "above": ["uses_above"],
    "timer": ["uses_timer"],
    "event": ["uses_cross", "uses_above", "uses_timer", "uses_initial_step", "uses_final_step"],
    "source": ["uses_pulse_source", "uses_pwl_source", "uses_sine_source", "uses_dc_source"],
    "pulse": ["uses_pulse_source"],
    "pwl": ["uses_pwl_source"],
    "sine": ["uses_sine_source"],
    "transition": ["uses_transition"],
    "abstime": ["uses_abstime"],
    "fileio": ["uses_fileio"],
    "math": ["uses_math_exp_log"],
    "bitwise": ["uses_bitwise"],
    "array": ["uses_integer_array", "uses_dynamic_vector_index"],
    "parser": ["uses_cross", "uses_timer", "uses_transition", "uses_fileio", "uses_bitwise", "uses_dynamic_vector_index"],
    "preflight": ["uses_pwl_source", "uses_fileio", "uses_transition", "uses_dynamic_vector_index", "uses_ahdl_include"],
}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _detect_features(text_by_kind: dict[str, str]) -> dict[str, dict[str, int]]:
    hits: dict[str, dict[str, int]] = {}
    all_text = "\n".join(text_by_kind.values())
    for feature, patterns in FEATURE_PATTERNS.items():
        per_kind: dict[str, int] = {}
        for kind, text in text_by_kind.items():
            count = sum(len(pattern.findall(text)) for pattern in patterns)
            if count:
                per_kind[kind] = count
        if per_kind:
            hits[feature] = per_kind

    # Helpful derived features that are awkward to capture with one regex.
    if "uses_transition" in hits and "uses_conditional" in hits:
        if re.search(r"\bif\s*\([^;{}]*\)\s*[^;{}]*transition\s*\(", all_text, re.I | re.S):
            hits.setdefault("uses_conditional_transition", {"derived": 1})
    if "uses_cross" in hits and "uses_pulse_source" in hits:
        hits.setdefault("uses_cross_on_pulse", {"derived": 1})
    if "uses_abstime" in hits and "uses_conditional" in hits:
        hits.setdefault("uses_abstime_condition", {"derived": 1})
    return hits


def _detect_uncertainty(text_by_kind: dict[str, str]) -> list[str]:
    """Return conservative markers for cases where regex tags may miss features."""
    flags: set[str] = set()
    for kind, text in text_by_kind.items():
        if not kind.endswith(":va") and kind not in {"candidate:va", "gold:va"}:
            continue
        if re.search(r"`define\b", text):
            flags.add("has_macro_define")
        macro_uses = re.findall(r"`([A-Za-z_][A-Za-z0-9_$]*)", text)
        meaningful_macro_uses = [
            name for name in macro_uses
            if name not in {"include", "define", "ifdef", "ifndef", "else", "endif"}
        ]
        if meaningful_macro_uses:
            flags.add("has_macro_use")
        includes = re.findall(r"`include\s+\"([^\"]+)\"", text)
        nonstandard_includes = [
            item for item in includes
            if Path(item).name not in {"constants.vams", "disciplines.vams"}
        ]
        if nonstandard_includes:
            flags.add("has_nonstandard_veriloga_include")
    return sorted(flags)


def _append_text(texts: dict[str, str], files: list[str], key: str, path: Path) -> None:
    texts[key] = texts.get(key, "") + "\n" + _read_text(path)
    files.append(str(path))


def _task_texts(
    task_dir: Path,
    *,
    scope: str,
    candidate_root: Path | None,
    model: str,
    sample_idx: int,
) -> tuple[dict[str, str], list[str]]:
    texts: dict[str, str] = {}
    files: list[str] = []
    for path in sorted(task_dir.glob("gold/*")):
        if path.suffix.lower() in {".va", ".scs"}:
            key = f"gold:{path.suffix.lower()[1:]}"
            _append_text(texts, files, key, path)
    if candidate_root is not None:
        sample_dir = candidate_root / model / task_dir.name / f"sample_{sample_idx}"
        for path in sorted(sample_dir.glob("*")):
            if path.suffix.lower() in {".va", ".scs"}:
                key = f"candidate:{path.suffix.lower()[1:]}"
                _append_text(texts, files, key, path)
    if scope == "all":
        for name in ("prompt.md", "checker.py", "checks.yaml"):
            path = task_dir / name
            if path.is_file():
                _append_text(texts, files, name, path)
    return texts, files


def build_feature_index(
    bench_dir: Path,
    *,
    scope: str = "executable",
    candidate_root: Path | None = None,
    model: str = "",
    sample_idx: int = 0,
) -> dict[str, Any]:
    task_root = bench_dir / "tasks"
    tasks: dict[str, Any] = {}
    feature_counts: Counter[str] = Counter()
    feature_by_form: dict[str, Counter[str]] = defaultdict(Counter)
    feature_by_pack: dict[str, Counter[str]] = defaultdict(Counter)

    for meta_path in sorted(task_root.glob("*/meta.json")):
        task_dir = meta_path.parent
        meta = _read_json(meta_path)
        task_id = meta.get("task_id") or task_dir.name
        task_form = meta.get("task_form") or meta.get("family", "")
        pack_id = meta.get("pack_id") or meta.get("circuit_function_id") or meta.get("core_function", "")
        texts, scanned_files = _task_texts(
            task_dir,
            scope=scope,
            candidate_root=candidate_root,
            model=model,
            sample_idx=sample_idx,
        )
        feature_hits = _detect_features(texts)
        uncertainty = _detect_uncertainty(texts)
        features = sorted(feature_hits)
        for feature in features:
            feature_counts[feature] += 1
            if task_form:
                feature_by_form[task_form][feature] += 1
            if pack_id:
                feature_by_pack[pack_id][feature] += 1
        tasks[task_id] = {
            "task_id": task_id,
            "task_dir": str(task_dir),
            "task_form": task_form,
            "pack_id": pack_id,
            "core_function": meta.get("core_function") or meta.get("category", ""),
            "features": features,
            "feature_hits": feature_hits,
            "uncertainty": uncertainty,
            "scanned_files": scanned_files,
        }

    return {
        "benchmark": str(bench_dir),
        "scope": scope,
        "candidate_root": str(candidate_root) if candidate_root is not None else None,
        "model": model or None,
        "sample_idx": sample_idx if candidate_root is not None else None,
        "task_count": len(tasks),
        "feature_counts": dict(sorted(feature_counts.items())),
        "feature_by_form": {k: dict(sorted(v.items())) for k, v in sorted(feature_by_form.items())},
        "feature_by_pack": {k: dict(sorted(v.items())) for k, v in sorted(feature_by_pack.items())},
        "uncertainty_counts": dict(sorted(Counter(
            flag for task in tasks.values() for flag in task.get("uncertainty", [])
        ).items())),
        "change_feature_map": CHANGE_FEATURES,
        "tasks": tasks,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bench-dir", type=Path, default=DEFAULT_BENCH)
    parser.add_argument("--output", type=Path, default=ROOT / "analysis" / "vabench_main_feature_tags.json")
    parser.add_argument("--scope", choices=["executable", "all"], default="executable",
                        help="executable scans gold/candidate .va/.scs only; all also scans prompt/checker/checks.")
    parser.add_argument("--candidate-dir", type=Path, help="Optional generated-root to include candidate .va/.scs features.")
    parser.add_argument("--model", default="", help="Model slug under --candidate-dir.")
    parser.add_argument("--sample-idx", type=int, default=0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.candidate_dir and not args.model:
        raise SystemExit("--model is required when --candidate-dir is provided")
    candidate_root = args.candidate_dir.resolve() if args.candidate_dir else None
    index = build_feature_index(
        args.bench_dir.resolve(),
        scope=args.scope,
        candidate_root=candidate_root,
        model=args.model,
        sample_idx=args.sample_idx,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "task_count": index["task_count"],
        "feature_count": len(index["feature_counts"]),
        "uncertainty_counts": index["uncertainty_counts"],
        "top_features": sorted(index["feature_counts"].items(), key=lambda kv: (-kv[1], kv[0]))[:12],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
