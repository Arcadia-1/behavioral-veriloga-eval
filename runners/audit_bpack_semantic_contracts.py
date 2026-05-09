#!/usr/bin/env python3
"""Audit bpack prompt/checker/gold semantic contract alignment.

This is intentionally conservative.  It does not try to prove that a prompt is
perfect; it flags cases where the public prompt can plausibly disagree with the
checker/gold contract that the model is later scored against.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BENCH = ROOT / "benchmark-bpack-v1"

MODULE_RE = re.compile(r"\bmodule\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")
INCLUDE_RE = re.compile(r'^\s*ahdl_include\s+"([^"]+)"', re.MULTILINE | re.IGNORECASE)
SAVE_RE = re.compile(r"^\s*save\s+(.+)$", re.MULTILINE | re.IGNORECASE)
TRAN_RE = re.compile(r"^\s*tran\s+.+$", re.MULTILINE | re.IGNORECASE)
CHECK_ITEM_RE = re.compile(r'^\s*-\s*"?([A-Za-z0-9_()@.<>\- ]+)"?\s*$', re.MULTILINE)

CHECK_KEYWORDS = {
    "output_shows_hysteresis_window": ("hysteresis", "threshold", "hold"),
    "upward_and_downward_trip_points_are_separated": ("rising", "falling", "threshold"),
    "ptr_is_one_hot_after_reset": ("one-hot", "reset", "pointer"),
    "cell_en_nonzero_after_reset": ("cell_en", "selected", "after reset"),
    "dwa_rotation_correct": ("dwa", "rotation", "pointer"),
    "dac_output_monotonic": ("monotonic", "code", "aout"),
    "dac_output_range_sufficient": ("range", "span", "vref"),
    "output_has_expected_pulse_width": ("pulse", "width", "stretcher"),
    "output_tracks_window": ("window", "inside", "outside"),
    "threshold_crossing_detected": ("threshold", "cross"),
    "sample_hold_tracks_on_clock": ("sample", "hold", "clock"),
    "clock_divides_by_expected_ratio": ("divide", "clock", "ratio"),
    "pfd_up_dn_pulses": ("up", "dn", "pfd"),
    "prbs_sequence_matches": ("prbs", "lfsr", "sequence"),
}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _gold_modules(task_dir: Path) -> list[str]:
    modules: list[str] = []
    for va_path in sorted((task_dir / "gold").glob("*.va")):
        for match in MODULE_RE.finditer(_read_text(va_path)):
            if match.group(1) not in modules:
                modules.append(match.group(1))
    return modules


def _gold_includes(task_dir: Path) -> list[str]:
    includes: list[str] = []
    for tb_path in sorted((task_dir / "gold").glob("*.scs")):
        for match in INCLUDE_RE.finditer(_read_text(tb_path)):
            name = Path(match.group(1)).name
            if name not in includes:
                includes.append(name)
    return includes


def _gold_save_names(task_dir: Path) -> list[str]:
    names: list[str] = []
    for tb_path in sorted((task_dir / "gold").glob("*.scs")):
        text = _read_text(tb_path).replace("\\\n", " ")
        for match in SAVE_RE.finditer(text):
            for token in re.split(r"\s+", match.group(1).strip()):
                token = token.strip()
                if token and token != "\\" and token not in names:
                    names.append(token)
    return names


def _gold_tran_lines(task_dir: Path) -> list[str]:
    lines: list[str] = []
    for tb_path in sorted((task_dir / "gold").glob("*.scs")):
        for match in TRAN_RE.finditer(_read_text(tb_path)):
            line = re.sub(r"\s+", " ", match.group(0).strip())
            if line not in lines:
                lines.append(line)
    return lines


def _checks_yaml_items(task_dir: Path) -> list[str]:
    path = task_dir / "checks.yaml"
    if not path.exists():
        return []
    items: list[str] = []
    for match in CHECK_ITEM_RE.finditer(_read_text(path)):
        item = match.group(1).strip().strip('"')
        if item and item not in items:
            items.append(item)
    return items


def _checker_source_task(task_dir: Path) -> str | None:
    path = task_dir / "checker.py"
    if not path.exists():
        return None
    text = _read_text(path)
    match = re.search(r"source_task_id\s*=\s*meta\.get\([^,]+,\s*'([^']+)'", text)
    return match.group(1) if match else None


def _add_issue(issues: list[dict[str, str]], severity: str, code: str, detail: str) -> None:
    issues.append({"severity": severity, "code": code, "detail": detail})


def _audit_one(task_dir: Path) -> dict[str, Any]:
    meta = _read_json(task_dir / "meta.json")
    prompt = _read_text(task_dir / "prompt.md")
    prompt_l = prompt.lower()
    task_id = meta.get("task_id", task_dir.name)
    task_form = meta.get("task_form", meta.get("family", ""))
    scoring = meta.get("scoring", [])
    gold_modules = _gold_modules(task_dir)
    gold_includes = _gold_includes(task_dir)
    gold_save_names = _gold_save_names(task_dir)
    gold_tran_lines = _gold_tran_lines(task_dir)
    checks_items = _checks_yaml_items(task_dir)
    checker_source_task = _checker_source_task(task_dir)
    issues: list[dict[str, str]] = []

    # Public identity should be visible when the model is expected to generate or
    # repair a DUT.  For tb-generation the provided DUT identity should be visible
    # as include/module/instance contract.
    if task_form in {"bugfix", "spec-to-va", "end-to-end"}:
        missing_modules = [m for m in gold_modules if m.lower() not in prompt_l]
        if missing_modules:
            _add_issue(issues, "FAIL", "gold_module_not_public", ", ".join(missing_modules))
    elif task_form == "tb-generation":
        missing_includes = [inc for inc in gold_includes if inc.lower() not in prompt_l]
        if missing_includes:
            _add_issue(issues, "FAIL", "gold_include_not_public", ", ".join(missing_includes))

    if "sim_correct" in scoring and checker_source_task and checker_source_task.lower() not in prompt_l:
        # Not fatal: bpack prompts often use a normalized task id rather than the
        # original source id.  It is still useful as provenance/audit signal.
        _add_issue(issues, "WARN", "checker_source_task_not_named", checker_source_task)

    public_contract_count = prompt_l.count("public evaluation contract")
    if public_contract_count > 1:
        _add_issue(issues, "WARN", "duplicate_public_evaluation_contract", str(public_contract_count))

    if re.search(r"required public waveform columns[\s\S]{0,160}`\\`", prompt, flags=re.IGNORECASE):
        _add_issue(issues, "FAIL", "malformed_required_waveform_columns", "contains bare backslash column")
    if re.search(r"^\s*save\s+.*\\\s*\n\s*```", prompt, flags=re.IGNORECASE | re.MULTILINE):
        _add_issue(issues, "FAIL", "malformed_public_save_statement", "save continuation is not followed by continued signals")

    if task_form == "spec-to-va":
        if "do not generate a testbench" in prompt_l and "testbench contract" in prompt_l:
            _add_issue(issues, "WARN", "dut_only_prompt_contains_testbench_contract", "source spec retained TB contract")
        if "return exactly two fenced code blocks" in prompt_l:
            _add_issue(issues, "WARN", "dut_only_prompt_contains_two_block_deliverable", "conflicts with DUT-only wrapper")
    if task_form == "tb-generation" and ("module " in prompt_l or ".va" not in prompt_l):
        if "do not generate verilog-a modules" not in prompt_l:
            _add_issue(issues, "WARN", "tb_prompt_may_not_exclude_dut_generation", "missing explicit no-DUT constraint")

    for item in checks_items:
        if item in {"@(cross(", "transition(", "tran", "save", "ahdl_include", "simulator lang=spectre"}:
            continue
        keywords = CHECK_KEYWORDS.get(item)
        if keywords and not all(keyword.lower() in prompt_l for keyword in keywords):
            _add_issue(issues, "WARN", "checker_behavior_not_fully_named", f"{item}: expected keywords {keywords}")

    if gold_tran_lines and not any("tran " in line.lower() and line.lower() in prompt_l for line in gold_tran_lines):
        if not any("tran tran" in prompt_l for _ in gold_tran_lines):
            _add_issue(issues, "WARN", "gold_tran_not_public", "; ".join(gold_tran_lines))

    if gold_save_names:
        key_saves = [name for name in gold_save_names if re.match(r"[A-Za-z_\\][A-Za-z0-9_\\]*$", name)]
        visible = [name for name in key_saves if name.lower().strip("\\") in prompt_l]
        if len(visible) < min(len(key_saves), 3):
            _add_issue(
                issues,
                "WARN",
                "few_gold_save_names_public",
                f"visible={len(visible)} of {len(key_saves)} public-ish save names",
            )

    status = "FAIL" if any(i["severity"] == "FAIL" for i in issues) else "WARN" if issues else "PASS"
    return {
        "task_id": task_id,
        "task_form": task_form,
        "pack_id": meta.get("pack_id"),
        "circuit_function_id": meta.get("circuit_function_id"),
        "core_function": meta.get("core_function"),
        "scoring": scoring,
        "status": status,
        "issues": issues,
        "gold_modules": gold_modules,
        "gold_includes": gold_includes,
        "gold_save_names": gold_save_names,
        "gold_tran_lines": gold_tran_lines,
        "checks_items": checks_items,
        "checker_source_task": checker_source_task,
    }


def _write_markdown(path: Path, summary: dict[str, Any]) -> None:
    rows = summary["tasks"]
    lines = [
        "# bpack48 Semantic Prompt-Checker-Gold Audit",
        "",
        "**Date**: 2026-05-08",
        "",
        "This audit checks whether public prompts expose the semantic contract that",
        "checkers and gold harnesses later validate.  It is conservative and",
        "heuristic: `WARN` means manual review or prompt cleanup is recommended, not",
        "that the benchmark is invalid.",
        "",
        "## Summary",
        "",
        f"- Tasks: `{summary['task_count']}`",
        f"- PASS: `{summary['status_counts'].get('PASS', 0)}`",
        f"- WARN: `{summary['status_counts'].get('WARN', 0)}`",
        f"- FAIL: `{summary['status_counts'].get('FAIL', 0)}`",
        "",
        "## Issue Counts",
        "",
        "| Issue | Count |",
        "| --- | ---: |",
    ]
    for code, count in sorted(summary["issue_counts"].items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"| `{code}` | {count} |")
    lines.extend([
        "",
        "## Task Findings",
        "",
        "| Status | Task | Pack | Form | Issues |",
        "| --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        issue_text = "<br>".join(f"{i['severity']}:{i['code']}={i['detail']}" for i in row["issues"]) or "none"
        lines.append(
            f"| {row['status']} | `{row['task_id']}` | `{row['pack_id']}` | `{row['task_form']}` | {issue_text} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "- `PASS` means this heuristic found no prompt/checker/gold contract drift.",
        "- `WARN` should be reviewed before promoting `bpack48` findings into a paper-facing claim.",
        "- `FAIL` should be fixed or explicitly waived before using the affected task in a benchmark gate.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bench-dir", type=Path, default=DEFAULT_BENCH)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "analysis")
    args = parser.parse_args()

    bench_dir = args.bench_dir.resolve()
    rows = [_audit_one(task_dir) for task_dir in sorted((bench_dir / "tasks").iterdir()) if task_dir.is_dir()]
    rows.sort(key=lambda r: ({"FAIL": 0, "WARN": 1, "PASS": 2}[r["status"]], r["pack_id"], r["task_form"], r["task_id"]))

    issue_counts = Counter(issue["code"] for row in rows for issue in row["issues"])
    status_counts = Counter(row["status"] for row in rows)
    by_pack = defaultdict(Counter)
    by_form = defaultdict(Counter)
    for row in rows:
        by_pack[row["pack_id"]][row["status"]] += 1
        by_form[row["task_form"]][row["status"]] += 1

    summary: dict[str, Any] = {
        "date": "2026-05-08",
        "benchmark": str(bench_dir),
        "task_count": len(rows),
        "status_counts": dict(status_counts),
        "issue_counts": dict(issue_counts),
        "by_pack": {pack: dict(counts) for pack, counts in sorted(by_pack.items())},
        "by_form": {form: dict(counts) for form, counts in sorted(by_form.items())},
        "tasks": rows,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    bench_slug = bench_dir.name.replace("benchmark-", "").replace("_", "-")
    json_path = args.output_dir / f"{bench_slug}_semantic_contract_audit_20260508.json"
    md_path = args.output_dir / f"{bench_slug}_semantic_contract_audit_20260508.md"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_markdown(md_path, summary)
    print(json.dumps({"task_count": len(rows), "status_counts": dict(status_counts), "issue_counts": dict(issue_counts)}, indent=2))
    print(f"json={json_path}")
    print(f"md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
