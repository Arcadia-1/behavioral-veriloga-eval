#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


DEFAULT_EVAS_DIR = Path("results/vabench-main-v1-main120-gold-evas-2026-05-08")
DEFAULT_SPECTRE_DIR = Path("results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08")
DEFAULT_TASKS_ROOT = Path("tasks")
DEFAULT_MARKDOWN_OUTPUT = Path("docs/VABENCH_MAIN120_MATERIALIZATION.md")
DEFAULT_CSV_OUTPUT = Path("docs/VABENCH_MAIN120_MATERIALIZATION.csv")
SOURCE_SUFFIXES = {".scs", ".va", ".vams"}
BENCHMARK_SPLIT = "vabench-main-v1"

FORM_TO_FAMILY = {
    "dut": "spec-to-va",
    "tb": "tb-generation",
    "bugfix": "bugfix",
    "e2e": "end-to-end",
}

STOP_TOKENS = {
    "vbm1",
    "smoke",
    "dut",
    "tb",
    "e2e",
    "bug",
    "bugfix",
    "ref",
    "fixed",
    "task",
}

CATEGORY_HINTS = [
    ("comparator", "comparator"),
    ("strongarm", "comparator"),
    ("offset_comparator", "comparator"),
    ("pfd", "phase-detector"),
    ("vco", "pll-clock"),
    ("lock_detector", "pll-clock"),
    ("dac", "dac"),
    ("cdac", "dac"),
    ("thermometer", "dac"),
    ("sar", "adc-sar"),
    ("counter", "digital-logic"),
    ("divider", "digital-logic"),
    ("decoder", "digital-logic"),
    ("latch", "digital-logic"),
    ("edge_detector", "digital-logic"),
    ("barrel", "calibration"),
    ("selector", "calibration"),
    ("shuffler", "calibration"),
    ("calibration", "calibration"),
    ("lowpass", "amplifier-filter"),
    ("integrator", "amplifier-filter"),
    ("rectifier", "amplifier-filter"),
    ("slew", "signal-source"),
    ("clamp", "signal-source"),
    ("track_hold", "sample-hold"),
    ("leaky_hold", "sample-hold"),
    ("peak_detector", "measurement"),
    ("settling_time", "measurement"),
    ("file_metric", "measurement"),
    ("one_shot_timer", "analog-events"),
]


@dataclass(frozen=True)
class ParsedTaskId:
    task_id: str
    base: str
    form: str
    family: str
    category_hint: str


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def summary_section(summary: dict) -> dict:
    backend = str(summary.get("backend", ""))
    section = summary.get(backend)
    if isinstance(section, dict):
        return section
    for value in summary.values():
        if isinstance(value, dict) and "pass_tasks" in value:
            return value
    return {}


def pass_tasks(summary_path: Path) -> list[str]:
    summary = load_json(summary_path)
    section = summary_section(summary)
    tasks = section.get("pass_tasks", [])
    if not isinstance(tasks, list):
        raise ValueError(f"{summary_path} does not contain a pass_tasks list")
    return [str(task) for task in tasks]


def axis_rates(summary_path: Path) -> dict[str, float]:
    section = summary_section(load_json(summary_path))
    rates = section.get("axis_rates", {})
    return dict(rates) if isinstance(rates, dict) else {}


def parse_task_id(task_id: str) -> ParsedTaskId:
    stem = task_id.removeprefix("vbm1_")
    for form in ("bugfix", "dut", "e2e", "tb"):
        suffix = f"_{form}"
        if stem.endswith(suffix):
            base = stem[: -len(suffix)]
            category = infer_category(base)
            return ParsedTaskId(
                task_id=task_id,
                base=base,
                form=form,
                family=FORM_TO_FAMILY[form],
                category_hint=category,
            )
    raise ValueError(f"cannot infer main120 form from task_id={task_id!r}")


def infer_category(base: str) -> str:
    for needle, category in CATEGORY_HINTS:
        if needle in base:
            return category
    return "uncategorized"


def rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_list(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*") if path.is_file())


def source_file_list(root: Path) -> list[Path]:
    return [path for path in file_list(root) if path.suffix.lower() in SOURCE_SUFFIXES]


def file_names(paths: Iterable[Path]) -> str:
    return ";".join(path.name for path in paths)


def content_fingerprints(paths: Iterable[Path]) -> dict[str, str]:
    return {path.name: sha256_file(path) for path in paths}


def staged_has_bugfix_pair(paths: Iterable[Path]) -> bool:
    names = {path.name.lower() for path in paths if path.suffix.lower() == ".va"}
    has_buggy = any(token in Path(name).stem for name in names for token in ("buggy", "broken", "badcase", "bad"))
    has_fixed = any(token in Path(name).stem for name in names for token in ("fixed", "goodcase", "good", "ref"))
    return has_buggy and has_fixed


def promotion_contract(parsed: ParsedTaskId, source_paths: Iterable[Path]) -> dict[str, str]:
    if parsed.form != "bugfix":
        return {
            "asset_type": "vabench_task",
            "benchmark_split": BENCHMARK_SPLIT,
            "release_form": "normal",
            "provenance_status": "clean",
            "source_main120_id": parsed.task_id,
            "badcase_origin": "",
            "counts_model_capability": "true",
            "counts_benchmark_coverage": "true",
            "counts_bugfix_claim": "false",
            "promotion_blockers": "missing_prompt_meta_checks_gold_review",
        }

    if staged_has_bugfix_pair(source_paths):
        return {
            "asset_type": "vabench_task",
            "benchmark_split": BENCHMARK_SPLIT,
            "release_form": "true-bugfix",
            "provenance_status": "badcase_available",
            "source_main120_id": parsed.task_id,
            "badcase_origin": "original",
            "counts_model_capability": "true",
            "counts_benchmark_coverage": "true",
            "counts_bugfix_claim": "true",
            "promotion_blockers": "missing_prompt_meta_checks_gold_review",
        }

    return {
        "asset_type": "vabench_task",
        "benchmark_split": BENCHMARK_SPLIT,
        "release_form": "evidence-only",
        "provenance_status": "historical_bugfix_fixed_only",
        "source_main120_id": parsed.task_id,
        "badcase_origin": "",
        "counts_model_capability": "false",
        "counts_benchmark_coverage": "false",
        "counts_bugfix_claim": "false",
        "promotion_blockers": "missing_buggy_fixed_pair;needs_D004_review;missing_prompt_meta_checks_gold_review",
    }


def tokens(text: str) -> set[str]:
    raw = re.split(r"[^a-zA-Z0-9]+", text.lower())
    normalized = set()
    for token in raw:
        if not token or token in STOP_TOKENS:
            continue
        if token.endswith("s") and len(token) > 3:
            token = token[:-1]
        aliases = {"cal": "calibration", "clk": "clock", "cmp": "comparator"}
        normalized.add(aliases.get(token, token))
    return normalized


def collect_current_tasks(tasks_root: Path) -> tuple[set[str], dict[str, set[str]], dict[str, str], dict[str, dict]]:
    current_ids: set[str] = set()
    current_tokens: dict[str, set[str]] = {}
    current_paths: dict[str, str] = {}
    current_meta: dict[str, dict] = {}
    for meta_path in sorted(tasks_root.glob("**/meta.json")):
        try:
            meta = load_json(meta_path)
        except json.JSONDecodeError:
            continue
        task_id = str(meta.get("id") or meta.get("task_id") or meta_path.parent.name)
        current_ids.add(task_id)
        current_meta[task_id] = meta
        token_source = " ".join(
            [
                task_id,
                str(meta.get("category", "")),
                " ".join(str(item) for item in meta.get("artifacts", [])),
                " ".join(str(item) for item in meta.get("source_files", [])),
            ]
        )
        current_tokens[task_id] = tokens(token_source)
        current_paths[task_id] = meta_path.parent.as_posix()
    return current_ids, current_tokens, current_paths, current_meta


def promotion_contract_from_current_meta(parsed: ParsedTaskId, meta: dict) -> dict[str, str] | None:
    if meta.get("asset_type", "vabench_task") != "vabench_task":
        return None
    release_form = meta.get("release_form")
    provenance_status = meta.get("provenance_status")
    counts = meta.get("counts")
    if release_form is None or provenance_status is None or not isinstance(counts, dict):
        return None
    blockers = meta.get("promotion_blockers", [])
    if isinstance(blockers, list):
        blocker_text = ";".join(str(item) for item in blockers)
    else:
        blocker_text = str(blockers)
    return {
        "asset_type": str(meta.get("asset_type", "vabench_task")),
        "benchmark_split": str(meta.get("benchmark_split", BENCHMARK_SPLIT)),
        "release_form": str(release_form),
        "provenance_status": str(provenance_status),
        "source_main120_id": str(meta.get("source_main120_id", parsed.task_id)),
        "badcase_origin": str(meta.get("badcase_origin", "")),
        "counts_model_capability": str(bool(counts.get("model_capability", False))).lower(),
        "counts_benchmark_coverage": str(bool(counts.get("benchmark_coverage", False))).lower(),
        "counts_bugfix_claim": str(bool(counts.get("bugfix_claim", False))).lower(),
        "promotion_blockers": blocker_text,
    }


def candidate_current_tasks(parsed: ParsedTaskId, current_tokens: dict[str, set[str]], *, limit: int = 3) -> str:
    query = tokens(parsed.base)
    if not query:
        return ""
    scored: list[tuple[float, str]] = []
    for task_id, candidate in current_tokens.items():
        if not candidate:
            continue
        overlap = len(query & candidate)
        if overlap == 0:
            continue
        score = overlap / len(query | candidate)
        if score >= 0.25:
            scored.append((score, task_id))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return ";".join(f"{task_id}:{score:.2f}" for score, task_id in scored[:limit])


def read_result_status(root: Path, task_id: str, backend: str) -> tuple[str, str]:
    result_path = root / task_id / f"{backend}_result.json"
    if not result_path.exists():
        return "MISSING", ""
    result = load_json(result_path)
    scores = result.get("scores", {})
    weighted = scores.get("weighted_total", "") if isinstance(scores, dict) else ""
    return str(result.get("status", "UNKNOWN")), str(weighted)


def build_rows(repo_root: Path, evas_dir: Path, spectre_dir: Path, tasks_root: Path) -> tuple[list[dict[str, str]], dict]:
    evas_tasks = pass_tasks(evas_dir / "summary.json")
    spectre_tasks = pass_tasks(spectre_dir / "summary.json")
    all_task_ids = sorted(set(evas_tasks) | set(spectre_tasks))
    current_ids, current_tokens, current_paths, current_meta = collect_current_tasks(tasks_root)

    rows: list[dict[str, str]] = []
    for task_id in all_task_ids:
        parsed = parse_task_id(task_id)
        evas_staged = file_list(evas_dir / task_id / "staged")
        spectre_staged = file_list(spectre_dir / task_id / "staged")
        evas_source = source_file_list(evas_dir / task_id / "staged")
        spectre_source = source_file_list(spectre_dir / task_id / "staged")
        evas_source_hashes = content_fingerprints(evas_source)
        spectre_source_hashes = content_fingerprints(spectre_source)
        source_hash_match = evas_source_hashes == spectre_source_hashes and bool(evas_source_hashes)
        exact_current = task_id in current_ids
        contract = (
            promotion_contract_from_current_meta(parsed, current_meta.get(task_id, {}))
            if exact_current
            else None
        )
        if contract is None:
            contract = promotion_contract(parsed, evas_source if evas_source else spectre_source)
        evas_status, evas_weighted = read_result_status(evas_dir, task_id, "evas")
        spectre_status, spectre_weighted = read_result_status(spectre_dir, task_id, "spectre")
        row = {
            "task_id": task_id,
            "base": parsed.base,
            "form": parsed.form,
            "family": parsed.family,
            "category_hint": parsed.category_hint,
            "exact_current_task": "yes" if exact_current else "no",
            "current_task_path": current_paths.get(task_id, ""),
            "candidate_current_tasks": "" if exact_current else candidate_current_tasks(parsed, current_tokens),
            "evas_status": evas_status,
            "spectre_status": spectre_status,
            "evas_weighted_total": evas_weighted,
            "spectre_weighted_total": spectre_weighted,
            "evas_staged_files": file_names(evas_staged),
            "spectre_staged_files": file_names(spectre_staged),
            "evas_staged_source_files": file_names(evas_source),
            "spectre_staged_source_files": file_names(spectre_source),
            "staged_source_hash_match": "yes" if source_hash_match else "no",
            "evas_staged_dir": rel(evas_dir / task_id / "staged", repo_root),
            "spectre_staged_dir": rel(spectre_dir / task_id / "staged", repo_root),
            "materialization_state": "needs_source_task" if not exact_current else "has_exact_task_id",
            "missing_source_pieces": "" if exact_current else "prompt.md;meta.json;checks.yaml;gold/",
            **contract,
        }
        rows.append(row)

    stats = {
        "evas_summary": rel(evas_dir / "summary.json", repo_root),
        "spectre_summary": rel(spectre_dir / "summary.json", repo_root),
        "evas_pass_tasks": len(evas_tasks),
        "spectre_pass_tasks": len(spectre_tasks),
        "paired_tasks": len(set(evas_tasks) & set(spectre_tasks)),
        "task_rows": len(rows),
        "exact_current_overlap": sum(1 for row in rows if row["exact_current_task"] == "yes"),
        "needs_source_task": sum(1 for row in rows if row["materialization_state"] == "needs_source_task"),
        "dual_pass": sum(1 for row in rows if row["evas_status"] == "PASS" and row["spectre_status"] == "PASS"),
        "staged_source_present_both": sum(
            1 for row in rows if row["evas_staged_source_files"] and row["spectre_staged_source_files"]
        ),
        "staged_source_hash_match": sum(1 for row in rows if row["staged_source_hash_match"] == "yes"),
        "forms": dict(Counter(row["form"] for row in rows)),
        "families": dict(Counter(row["family"] for row in rows)),
        "release_forms": dict(Counter(row["release_form"] for row in rows)),
        "provenance_statuses": dict(Counter(row["provenance_status"] for row in rows)),
        "countable_model_capability": sum(1 for row in rows if row["counts_model_capability"] == "true"),
        "countable_benchmark_coverage": sum(1 for row in rows if row["counts_benchmark_coverage"] == "true"),
        "countable_bugfix_claim": sum(1 for row in rows if row["counts_bugfix_claim"] == "true"),
        "categories": dict(Counter(row["category_hint"] for row in rows)),
        "evas_axis_rates": axis_rates(evas_dir / "summary.json"),
        "spectre_axis_rates": axis_rates(spectre_dir / "summary.json"),
    }
    return rows, stats


def markdown_table(headers: list[str], body: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in body)
    return "\n".join(lines)


def build_markdown(rows: list[dict[str, str]], stats: dict, csv_output: Path, generated_on: str) -> str:
    form_rows = [
        [form, str(stats["forms"].get(form, 0)), FORM_TO_FAMILY[form]]
        for form in ("dut", "tb", "bugfix", "e2e")
    ]
    category_rows = [
        [category, str(count)]
        for category, count in sorted(stats["categories"].items(), key=lambda item: (-item[1], item[0]))
    ]
    release_rows = [
        [form, str(count)]
        for form, count in sorted(stats["release_forms"].items(), key=lambda item: (-item[1], item[0]))
    ]
    provenance_rows = [
        [status, str(count)]
        for status, count in sorted(stats["provenance_statuses"].items(), key=lambda item: (-item[1], item[0]))
    ]
    base_to_forms: dict[str, set[str]] = defaultdict(set)
    base_to_candidates: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        base_to_forms[row["base"]].add(row["form"])
        if row["candidate_current_tasks"]:
            for item in row["candidate_current_tasks"].split(";"):
                base_to_candidates[row["base"]].add(item.split(":", 1)[0])
    base_rows = []
    for base in sorted(base_to_forms):
        forms = ",".join(form for form in ("dut", "tb", "bugfix", "e2e") if form in base_to_forms[base])
        candidates = ";".join(sorted(base_to_candidates.get(base, set()))) or "-"
        base_rows.append([base, forms, candidates])

    lines = [
        "# vaBench Main120 Materialization Inventory",
        "",
        f"Generated: {generated_on}",
        "",
        "## Summary",
        "",
        "This inventory treats `vabench-main-v1-main120` as validated result evidence",
        "that still needs to be restored/materialized into source-controlled benchmark",
        "tasks before it can serve as a release-quality benchmark source split.",
        "",
        markdown_table(
            ["Metric", "Value"],
            [
                ["EVAS pass tasks", str(stats["evas_pass_tasks"])],
                ["Spectre pass tasks", str(stats["spectre_pass_tasks"])],
                ["Paired EVAS/Spectre task IDs", str(stats["paired_tasks"])],
                ["Dual PASS rows", str(stats["dual_pass"])],
                ["Exact overlap with current `tasks/` IDs", str(stats["exact_current_overlap"])],
                ["Rows needing source task materialization", str(stats["needs_source_task"])],
                ["Rows with staged source assets in both runs", str(stats["staged_source_present_both"])],
                ["Rows where EVAS/Spectre staged source hashes match", str(stats["staged_source_hash_match"])],
                ["Rows countable as model capability after current policy", str(stats["countable_model_capability"])],
                ["Rows countable as bugfix claim after current policy", str(stats["countable_bugfix_claim"])],
                ["Row-level CSV", f"`{csv_output.as_posix()}`"],
            ],
        ),
        "",
        "## Source Evidence",
        "",
        markdown_table(
            ["Evidence", "Path"],
            [
                ["EVAS main120 summary", f"`{stats['evas_summary']}`"],
                ["Spectre main120 summary", f"`{stats['spectre_summary']}`"],
            ],
        ),
        "",
        "## Forms",
        "",
        markdown_table(["Form", "Rows", "Target family"], form_rows),
        "",
        "## Category Hints",
        "",
        markdown_table(["Category hint", "Rows"], category_rows),
        "",
        "## Promotion Policy State",
        "",
        "These fields are policy gates, not final human-reviewed release labels.",
        "`evidence-only` rows are retained in the inventory but excluded from",
        "model-capability and bugfix-claim denominators until a reviewer approves",
        "a real source task.",
        "",
        markdown_table(["Release form", "Rows"], release_rows),
        "",
        markdown_table(["Provenance status", "Rows"], provenance_rows),
        "",
        "## Base Circuit Groups",
        "",
        "The 120 rows are organized as 30 base circuits times four task forms.",
        "Candidate current tasks are fuzzy hints for manual deduplication; they are",
        "not source-of-truth mappings.",
        "",
        markdown_table(["Base", "Forms present", "Candidate current tasks"], base_rows),
        "",
        "## Materialization Decision",
        "",
        "The next safe action is to create source task directories from the staged",
        "`.va`/`.scs` files and the recorded dual-pass evidence, while marking",
        "`prompt.md`, `meta.json`, and `checks.yaml` as review targets rather than",
        "pretending they already exist in `tasks/`.",
        "",
    ]
    return "\n".join(lines)


def write_csv(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a source-materialization inventory for the validated vaBench main120 result asset."
    )
    parser.add_argument("--evas-dir", type=Path, default=DEFAULT_EVAS_DIR)
    parser.add_argument("--spectre-dir", type=Path, default=DEFAULT_SPECTRE_DIR)
    parser.add_argument("--tasks-root", type=Path, default=DEFAULT_TASKS_ROOT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    parser.add_argument("--csv-output", type=Path, default=DEFAULT_CSV_OUTPUT)
    parser.add_argument("--date", default=date.today().isoformat())
    args = parser.parse_args()

    repo_root = Path.cwd()
    rows, stats = build_rows(repo_root, args.evas_dir, args.spectre_dir, args.tasks_root)
    if not rows:
        raise RuntimeError("main120 inventory produced zero rows")

    write_csv(rows, args.csv_output)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.write_text(
        build_markdown(rows, stats, args.csv_output, args.date),
        encoding="utf-8",
    )
    print(f"wrote {args.markdown_output}")
    print(f"wrote {args.csv_output}")
    print(
        "summary: "
        f"rows={stats['task_rows']} dual_pass={stats['dual_pass']} "
        f"exact_current_overlap={stats['exact_current_overlap']} "
        f"needs_source_task={stats['needs_source_task']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
