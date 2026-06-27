#!/usr/bin/env python3
"""Audit vaBench v3 for duplicate and source-import filler risks.

This script is intentionally report-only. It does not rewrite tasks; it creates
deterministic JSON/Markdown evidence for GitHub issue #29 so reviewers can
decide which rows should remain scored, be merged, or receive stronger tests.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as _dt
import difflib
import hashlib
import json
import re
import statistics
import sys
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python <3.11 fallback.
    tomllib = None  # type: ignore[assignment]


ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = ROOT / "tasks"
REPORTS_DIR = ROOT / "reports"
JSON_REPORT = REPORTS_DIR / "issue29_duplicate_and_filler_audit.json"
MD_REPORT = REPORTS_DIR / "issue29_duplicate_and_filler_audit.md"

ISSUE_GROUPS: list[dict[str, Any]] = [
    {
        "id": "lowpass_original_vs_bugfix",
        "issue_tasks": ["007-first-order-lowpass", "286-first-order-lowpass-bugfix"],
        "why_flagged": "Same low-pass kernel appears once as a DUT construction task and once as a bugfix task.",
    },
    {
        "id": "window_comparator_dut_vs_tb",
        "issue_tasks": ["049-window-comparator-detector", "284-window-comparator-testbench"],
        "why_flagged": "Same window-comparator function appears as DUT and testbench-generation variants.",
    },
    {
        "id": "aperture_delay_pair",
        "issue_tasks": ["081-aperture-delay-track-and-hold", "285-aperture-delay-sample-hold"],
        "why_flagged": "Two aperture-delay sample/track-and-hold tasks may differ mainly by wrapper wording.",
    },
    {
        "id": "timer_reacquire_pair",
        "issue_tasks": ["097-cppll-tracking-reacquire-timer", "107-reference-step-clock"],
        "why_flagged": "Both tasks exercise timer/clock-step timing behavior and may overlap as control-flow kernels.",
    },
    {
        "id": "signal_chain_vs_components",
        "issue_tasks": [
            "099-dither-adder",
            "101-fixed-gain-amplifier",
            "111-clocked-sine-source",
            "287-gain-extraction-flow",
        ],
        "why_flagged": "An L2 flow may package kernels that also appear as standalone source/gain/source tasks.",
    },
    {
        "id": "absolute_value_duplicate",
        "issue_tasks": ["288-absolute-value", "148-absolute-value"],
        "why_flagged": "Two tasks share the same public title and likely the same absolute-value transfer function.",
    },
    {
        "id": "smooth_tanh_comparator_duplicate",
        "issue_tasks": ["292-smooth-tanh-comparator", "146-smooth-comparator-tanh"],
        "why_flagged": "Two tasks appear to name the same smooth tanh comparator transfer behavior.",
    },
    {
        "id": "pfd_active_low_reset_pair",
        "issue_tasks": ["300-pfd-active-low-reset", "282-pfd-timer-reset"],
        "why_flagged": "Two PFD reset tasks may share state/timer reset semantics.",
    },
    {
        "id": "subradix_vs_weighted_decoder",
        "issue_tasks": ["294-subradix-dac10", "274-weighted-decoder-6bit"],
        "why_flagged": "Two weighted decoder/DAC tasks may overlap at the bit-weight decoding kernel.",
    },
]

MANUAL_GROUP_ADJUDICATIONS: dict[str, dict[str, str]] = {
    "lowpass_original_vs_bugfix": {
        "classification": "valid_variant_needs_counting_policy",
        "status": "Manual review completed for 007/286; EVAS recertification refreshed for the repaired boundary slice.",
        "decision": (
            "Keep 007 as the independent L1 first-order-lowpass DUT construction task. "
            "Keep 286 as a bugfix-form repair variant for the same lowpass function, "
            "but do not count it as additional independent lowpass circuit-function coverage."
        ),
        "evidence": (
            "Task 007 hidden gold PASS and 5/5 concrete negatives FAIL_SIM_CORRECTNESS; "
            "its prompt no longer exposes hidden-evaluator or source-provenance wording. "
            "Task 286 hidden gold PASS and 4/4 concrete bugfix negatives FAIL_SIM_CORRECTNESS; "
            "its visible smoke bench is now distinct from the full hidden 160 ns settling bench. "
            "Spectre was not rerun in this local audit."
        ),
    },
    "timer_reacquire_pair": {
        "classification": "manually_split_pending_spectre",
        "status": "EVAS-only review refreshed; Spectre was not rerun by request.",
        "decision": (
            "Keep as distinct candidate rows after manual split: task 097 grades the "
            "CPPLL reacquire DUT with a supplied reference-step-clock support artifact, "
            "while task 107 grades the standalone reference-step-clock DUT."
        ),
        "evidence": (
            "Task 097 hidden gold PASS, visible smoke PASS, and 5/5 concrete negatives "
            "FAIL_SIM_CORRECTNESS after adding a vctrl_span dynamic check. Task 107 "
            "hidden gold PASS and 5/5 concrete negatives FAIL_SIM_CORRECTNESS with "
            "hidden parameters different from visible smoke parameters."
        ),
    },
    "signal_chain_vs_components": {
        "classification": "manually_split_pending_spectre",
        "status": "Manual review completed for 099/101/111/287; EVAS recertification refreshed for the edited boundary slice.",
        "decision": (
            "Keep 099 and 101 as standalone L1 component tasks after boundary repair; "
            "keep 111 only as an L2 support component for measurement-flow stimulus; "
            "keep 287 as a Measurement L2 composed flow. The 287/component overlap is "
            "component-in-flow overlap, not a duplicate-function merge condition."
        ),
        "evidence": (
            "Task 099 now targets only dither_adder.va with task-specific dither/common-mode "
            "checker evidence: hidden gold PASS and 4/4 concrete negatives FAIL_SIM_CORRECTNESS. "
            "Task 101 now targets only gain_amp_fixed.va with task-specific gain/polarity/common-mode "
            "checker evidence: hidden gold PASS and 4/4 concrete negatives FAIL_SIM_CORRECTNESS. "
            "Task 111 remains flow-staged support L2: hidden gold PASS and zero-source negative "
            "FAIL_SIM_CORRECTNESS under the existing gain-extraction flow checker. Task 287 remains "
            "Measurement L2: hidden gold PASS and unity-gain negative FAIL_SIM_CORRECTNESS. "
            "Spectre was not rerun in this local audit."
        ),
    },
}

COMMON_WORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "task",
    "verilog",
    "module",
    "input",
    "output",
    "voltage",
    "analog",
    "behavior",
    "behavioral",
    "must",
    "use",
    "using",
    "dut",
    "test",
    "hidden",
    "visible",
    "public",
    "write",
    "file",
    "candidate",
}


@dataclasses.dataclass(frozen=True)
class TaskInfo:
    task_dir: Path
    number: int
    slug: str
    task_id: str
    name: str
    title: str
    form: str
    level: str
    difficulty: str
    category: str
    targets: tuple[str, ...]
    instruction: str
    checks: str
    solution: str
    starter: str
    audit: str
    negative_entries: tuple[dict[str, str], ...]
    negative_file_count: int

    @property
    def display(self) -> str:
        return self.task_dir.name

    @property
    def source_family(self) -> bool:
        return "_source_" in self.task_id.lower()

    @property
    def solution_loc(self) -> int:
        return count_code_lines(self.solution)

    @property
    def concrete_negative_count(self) -> int:
        return max(len(self.negative_entries), self.negative_file_count)

    @property
    def zero_only_negative(self) -> bool:
        if self.concrete_negative_count != 1:
            return False
        joined = " ".join(
            [entry.get("id", "") + " " + entry.get("path", "") for entry in self.negative_entries]
        ).lower()
        return "zero" in joined or "stuck" in joined

    @property
    def normalized_solution(self) -> str:
        return normalize_code(self.solution)

    @property
    def normalized_prompt(self) -> str:
        return normalize_text(self.instruction)

    @property
    def normalized_checks(self) -> str:
        return normalize_text(self.checks)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def load_task_toml(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if tomllib is not None:
        return tomllib.loads(raw.decode("utf-8"))
    text = raw.decode("utf-8")
    data: dict[str, Any] = {}
    artifacts: dict[str, Any] = {}
    in_artifacts = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "[artifacts]":
            in_artifacts = True
            continue
        if "=" not in stripped:
            continue
        key, value = [part.strip() for part in stripped.split("=", 1)]
        if value.startswith('"') and value.endswith('"'):
            parsed: Any = value[1:-1]
        elif value.startswith("[") and value.endswith("]"):
            parsed = [item.strip().strip('"') for item in value[1:-1].split(",") if item.strip()]
        else:
            parsed = value
        if in_artifacts:
            artifacts[key] = parsed
        else:
            data[key] = parsed
    if artifacts:
        data["artifacts"] = artifacts
    return data


def normalize_text(text: str) -> str:
    lowered = text.lower()
    lowered = re.sub(r"```.*?```", " ", lowered, flags=re.S)
    lowered = re.sub(r"[^a-z0-9_.$:+-]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def normalize_code(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    text = re.sub(r"//.*", " ", text)
    text = text.lower()
    text = re.sub(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", lambda m: m.group(0).lower(), text)
    text = re.sub(r"\s+", "", text)
    return text


def count_code_lines(text: str) -> int:
    no_block = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    count = 0
    for line in no_block.splitlines():
        stripped = re.sub(r"//.*", "", line).strip()
        if stripped:
            count += 1
    return count


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def token_set(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9_.$:+-]{3,}", normalize_text(text))
        if token not in COMMON_WORDS
    }


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / max(1, len(a | b))


def sequence_ratio(a: str, b: str, max_chars: int = 16000) -> float:
    if not a or not b:
        return 0.0
    if len(a) > max_chars:
        a = a[:max_chars]
    if len(b) > max_chars:
        b = b[:max_chars]
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def extract_markdown_excerpt(text: str, max_chars: int = 900) -> str:
    lines: list[str] = []
    keep_next = False
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        low = line.lower()
        if line.startswith("#") or any(
            marker in low
            for marker in [
                "required behavior",
                "behavior",
                "interface",
                "public",
                "implement",
                "write",
                "requirements",
                "expected",
            ]
        ):
            keep_next = True
        if keep_next and line:
            lines.append(line)
        if keep_next and len(lines) >= 18:
            break
    if not lines:
        lines = [line.rstrip() for line in text.splitlines() if line.strip()][:18]
    excerpt = "\n".join(lines).strip()
    if len(excerpt) > max_chars:
        excerpt = excerpt[: max_chars - 1].rstrip() + "…"
    return excerpt


def collect_artifact_text(root: Path, targets: tuple[str, ...] = ()) -> str:
    if not root.exists():
        return ""
    target_files = [root / target for target in targets if (root / target).is_file()]
    if target_files:
        files = sorted(target_files)
    else:
        text_suffixes = {".va", ".vams", ".scs", ".cir", ".sp", ".spi", ".txt", ".md"}
        files = sorted(
            file_path
            for file_path in root.rglob("*")
            if file_path.is_file() and file_path.suffix.lower() in text_suffixes
        )
    chunks = []
    for file_path in files:
        chunks.append(f"// FILE: {file_path.relative_to(root)}\n{read_text(file_path)}")
    return "\n\n".join(chunks)


def collect_negative_entries(task_dir: Path) -> tuple[tuple[dict[str, str], ...], int]:
    neg_dir = task_dir / "negative_variants"
    entries: list[dict[str, str]] = []
    if neg_dir.exists():
        for manifest in sorted(neg_dir.rglob("manifest.json")):
            try:
                data = json.loads(read_text(manifest))
            except json.JSONDecodeError:
                continue
            for key in ("variants", "cases", "negatives"):
                items = data.get(key)
                if not isinstance(items, list):
                    continue
                for idx, item in enumerate(items):
                    if not isinstance(item, dict):
                        continue
                    path = item.get("path") or item.get("artifact") or item.get("source") or ""
                    rel_manifest = manifest.relative_to(task_dir).as_posix()
                    entries.append(
                        {
                            "id": str(item.get("id") or f"{key}_{idx:03d}"),
                            "path": str(path),
                            "description": str(
                                item.get("description")
                                or item.get("mutation")
                                or item.get("reason")
                                or ""
                            ),
                            "manifest": rel_manifest,
                        }
                    )
    artifact_suffixes = {".va", ".vams", ".scs", ".cir", ".sp", ".spi"}
    file_count = (
        len(
            [
                file_path
                for file_path in neg_dir.rglob("*")
                if file_path.is_file() and file_path.suffix.lower() in artifact_suffixes
            ]
        )
        if neg_dir.exists()
        else 0
    )
    dedup: dict[tuple[str, str], dict[str, str]] = {}
    for entry in entries:
        dedup[(entry["id"], entry["path"])] = entry
    return tuple(dedup.values()), file_count


def load_tasks() -> list[TaskInfo]:
    tasks: list[TaskInfo] = []
    for task_dir in sorted(TASKS_DIR.iterdir(), key=lambda p: p.name):
        if not task_dir.is_dir():
            continue
        match = re.match(r"^(\d+)-(.+)$", task_dir.name)
        if not match:
            continue
        task_toml = task_dir / "task.toml"
        if not task_toml.exists():
            continue
        meta = load_task_toml(task_toml)
        artifacts = meta.get("artifacts", {})
        targets = tuple(str(item) for item in artifacts.get("target", []) if item)
        negative_entries, negative_file_count = collect_negative_entries(task_dir)
        tasks.append(
            TaskInfo(
                task_dir=task_dir,
                number=int(match.group(1)),
                slug=match.group(2),
                task_id=str(meta.get("id", "")),
                name=str(meta.get("name", task_dir.name)),
                title=str(meta.get("title", "")),
                form=str(meta.get("form", "")),
                level=str(meta.get("level", "")),
                difficulty=str(meta.get("difficulty", "")),
                category=str(meta.get("category", "")),
                targets=targets,
                instruction=read_text(task_dir / str(meta.get("instruction", "instruction.md"))),
                checks=read_text(task_dir / str(meta.get("harness_dir", "test_harness")) / "checks.yaml"),
                solution=collect_artifact_text(
                    task_dir / str(meta.get("solution_dir", "solution")),
                    targets,
                ),
                starter=collect_artifact_text(task_dir / str(meta.get("starter_dir", "starter"))),
                audit=read_text(task_dir / "AUDIT.md"),
                negative_entries=negative_entries,
                negative_file_count=negative_file_count,
            )
        )
    return tasks


def pair_metrics(a: TaskInfo, b: TaskInfo) -> dict[str, float]:
    return {
        "prompt_token_jaccard": round(jaccard(token_set(a.instruction), token_set(b.instruction)), 4),
        "solution_token_jaccard": round(jaccard(token_set(a.solution), token_set(b.solution)), 4),
        "checker_token_jaccard": round(jaccard(token_set(a.checks), token_set(b.checks)), 4),
        "prompt_sequence_similarity": round(sequence_ratio(a.normalized_prompt, b.normalized_prompt), 4),
        "solution_sequence_similarity": round(sequence_ratio(a.normalized_solution, b.normalized_solution), 4),
        "checker_sequence_similarity": round(sequence_ratio(a.normalized_checks, b.normalized_checks), 4),
    }


def relation_label(a: TaskInfo, b: TaskInfo, metrics: dict[str, float]) -> tuple[str, str]:
    same_title = normalize_text(a.title) == normalize_text(b.title) and bool(a.title)
    cross_form = a.form != b.form
    solution_sim = metrics["solution_sequence_similarity"]
    checker_sim = metrics["checker_sequence_similarity"]
    prompt_sim = metrics["prompt_sequence_similarity"]
    title_overlap = jaccard(token_set(a.title), token_set(b.title))
    same_target_set = bool(a.targets) and set(a.targets) == set(b.targets)
    if same_title and solution_sim >= 0.94 and checker_sim >= 0.80 and not cross_form:
        return (
            "hard_duplicate",
            "Same public title and near-identical solution in the same artifact form; keep at most one scored row unless tests prove distinct behavior.",
        )
    if cross_form and (same_title or title_overlap >= 0.25 or solution_sim >= 0.80 or checker_sim >= 0.35):
        return (
            "valid_variant_needs_counting_policy",
            "Overlapping function appears in different artifact roles; can be kept as a separate skill only if scoring/counting labels avoid claiming an independent circuit function.",
        )
    if solution_sim >= 0.94 and checker_sim >= 0.80 and same_target_set:
        return (
            "hard_duplicate",
            "Solution, target artifact set, and checker contracts are all highly similar; likely duplicate benchmark credit.",
        )
    if solution_sim >= 0.84 or prompt_sim >= 0.78 or checker_sim >= 0.86:
        return (
            "high_overlap",
            "High prompt/solution/checker overlap; needs manual review before counting as an independent task.",
        )
    if a.source_family and b.source_family and (
        min(a.solution_loc, b.solution_loc) <= 20
        or min(a.concrete_negative_count, b.concrete_negative_count) < 4
    ):
        return (
            "filler_risk",
            "Source-family rows are short or have weak negative evidence; audit for source-import filler before scoring.",
        )
    return (
        "needs_human_review",
        "Automatic similarity is not decisive; inspect behavior, hidden checks, and negative variants manually.",
    )


def task_risks(task: TaskInfo) -> list[str]:
    risks: list[str] = []
    if task.concrete_negative_count == 0:
        risks.append("no_concrete_negative_variants")
    elif task.concrete_negative_count < 4:
        risks.append("low_negative_variant_count")
    if task.zero_only_negative:
        risks.append("zero_only_negative")
    if task.solution_loc <= 20:
        risks.append("short_solution_leq_20_loc")
    if task.source_family and task.solution_loc <= 20:
        risks.append("source_family_short_solution")
    if task.source_family and task.concrete_negative_count < 4:
        risks.append("source_family_low_negative_count")
    if "checker:" not in task.checks and "sim_correct:" not in task.checks:
        risks.append("checker_config_sparse")
    return risks


def build_issue_group_reports(tasks_by_name: dict[str, TaskInfo]) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for group in ISSUE_GROUPS:
        members = [tasks_by_name[name] for name in group["issue_tasks"] if name in tasks_by_name]
        missing = [name for name in group["issue_tasks"] if name not in tasks_by_name]
        pairs: list[dict[str, Any]] = []
        labels: list[str] = []
        for i, a in enumerate(members):
            for b in members[i + 1 :]:
                metrics = pair_metrics(a, b)
                label, recommendation = relation_label(a, b, metrics)
                labels.append(label)
                pairs.append(
                    {
                        "task_a": a.display,
                        "task_b": b.display,
                        "classification": label,
                        "recommendation": recommendation,
                        "metrics": metrics,
                    }
                )
        if "hard_duplicate" in labels:
            group_class = "hard_duplicate"
        elif "high_overlap" in labels:
            group_class = "high_overlap"
        elif "valid_variant_needs_counting_policy" in labels:
            group_class = "valid_variant_needs_counting_policy"
        elif "filler_risk" in labels:
            group_class = "filler_risk"
        else:
            group_class = "needs_human_review"
        reports.append(
            {
                "id": group["id"],
                "why_flagged": group["why_flagged"],
                "missing_tasks": missing,
                "classification": MANUAL_GROUP_ADJUDICATIONS.get(group["id"], {}).get(
                    "classification",
                    group_class,
                ),
                "auto_classification": group_class,
                "manual_adjudication": MANUAL_GROUP_ADJUDICATIONS.get(group["id"]),
                "members": [task_summary(member) for member in members],
                "pairs": pairs,
                "prompt_excerpts": {
                    member.display: extract_markdown_excerpt(member.instruction)
                    for member in members
                },
            }
        )
    return reports


def task_summary(task: TaskInfo) -> dict[str, Any]:
    return {
        "name": task.display,
        "id": task.task_id,
        "title": task.title,
        "form": task.form,
        "level": task.level,
        "difficulty": task.difficulty,
        "category": task.category,
        "targets": list(task.targets),
        "solution_loc": task.solution_loc,
        "negative_count": task.concrete_negative_count,
        "risks": task_risks(task),
        "solution_sha256_normalized": sha256_text(task.normalized_solution) if task.normalized_solution else "",
    }


def build_coarse_scan(tasks: list[TaskInfo], issue_pair_keys: set[tuple[str, str]]) -> dict[str, Any]:
    title_groups: dict[str, list[str]] = {}
    solution_hash_groups: dict[str, list[str]] = {}
    for task in tasks:
        title_key = normalize_text(task.title)
        if title_key:
            title_groups.setdefault(title_key, []).append(task.display)
        if task.normalized_solution:
            solution_hash_groups.setdefault(sha256_text(task.normalized_solution), []).append(task.display)

    duplicate_titles = {
        key: value for key, value in sorted(title_groups.items()) if len(value) > 1
    }
    exact_solution_duplicates = {
        key: value for key, value in sorted(solution_hash_groups.items()) if len(value) > 1
    }

    near_solution_pairs: list[dict[str, Any]] = []
    prompt_overlap_pairs: list[dict[str, Any]] = []
    solution_tokens = {task.display: token_set(task.solution) for task in tasks}
    prompt_tokens = {task.display: token_set(task.instruction) for task in tasks}

    for i, a in enumerate(tasks):
        for b in tasks[i + 1 :]:
            key = tuple(sorted([a.display, b.display]))
            sol_j = jaccard(solution_tokens[a.display], solution_tokens[b.display])
            prompt_j = jaccard(prompt_tokens[a.display], prompt_tokens[b.display])
            same_title = normalize_text(a.title) == normalize_text(b.title) and bool(a.title)
            maybe_solution_dup = sol_j >= 0.72 or same_title
            maybe_prompt_dup = prompt_j >= 0.74 or same_title
            if maybe_solution_dup:
                sol_seq = sequence_ratio(a.normalized_solution, b.normalized_solution)
                if sol_seq >= 0.82 or same_title:
                    label, recommendation = relation_label(
                        a,
                        b,
                        {
                            "solution_sequence_similarity": sol_seq,
                            "checker_sequence_similarity": sequence_ratio(a.normalized_checks, b.normalized_checks),
                            "prompt_sequence_similarity": sequence_ratio(a.normalized_prompt, b.normalized_prompt),
                        },
                    )
                    near_solution_pairs.append(
                        {
                            "task_a": a.display,
                            "task_b": b.display,
                            "issue_named_pair": key in issue_pair_keys,
                            "classification": label,
                            "solution_similarity": round(sol_seq, 4),
                            "solution_token_jaccard": round(sol_j, 4),
                            "checker_similarity": round(
                                sequence_ratio(a.normalized_checks, b.normalized_checks), 4
                            ),
                            "forms": [a.form, b.form],
                            "titles": [a.title, b.title],
                            "recommendation": recommendation,
                        }
                    )
            if maybe_prompt_dup:
                prompt_seq = sequence_ratio(a.normalized_prompt, b.normalized_prompt)
                if prompt_seq >= 0.86 or same_title:
                    prompt_overlap_pairs.append(
                        {
                            "task_a": a.display,
                            "task_b": b.display,
                            "issue_named_pair": key in issue_pair_keys,
                            "prompt_similarity": round(prompt_seq, 4),
                            "prompt_token_jaccard": round(prompt_j, 4),
                            "forms": [a.form, b.form],
                            "titles": [a.title, b.title],
                        }
                    )

    risk_rows = [
        task_summary(task)
        for task in tasks
        if task_risks(task)
    ]
    risk_rows.sort(key=lambda row: (len(row["risks"]), row["name"]), reverse=True)

    return {
        "duplicate_titles": duplicate_titles,
        "exact_solution_duplicates": exact_solution_duplicates,
        "near_solution_pairs": sorted(
            near_solution_pairs,
            key=lambda row: (row["solution_similarity"], row["solution_token_jaccard"]),
            reverse=True,
        )[:80],
        "prompt_overlap_pairs": sorted(
            prompt_overlap_pairs,
            key=lambda row: (row["prompt_similarity"], row["prompt_token_jaccard"]),
            reverse=True,
        )[:80],
        "task_risks": risk_rows,
    }


def issue_pair_key_set() -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    for group in ISSUE_GROUPS:
        names = group["issue_tasks"]
        for i, a in enumerate(names):
            for b in names[i + 1 :]:
                keys.add(tuple(sorted([a, b])))
    return keys


def build_report() -> dict[str, Any]:
    tasks = load_tasks()
    tasks_by_name = {task.display: task for task in tasks}
    risks_by_task = {task.display: task_risks(task) for task in tasks if task_risks(task)}
    source_tasks = [task for task in tasks if task.source_family]
    negative_counts = [task.concrete_negative_count for task in tasks]
    solution_locs = [task.solution_loc for task in tasks if task.solution_loc > 0]
    report = {
        "report_id": "issue29_duplicate_and_filler_audit",
        "generated_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "release": "benchmark-vabench-release-v3",
        "scope": {
            "task_count": len(tasks),
            "source_family_heuristic_count": len(source_tasks),
            "forms": count_by(tasks, "form"),
            "levels": count_by(tasks, "level"),
            "difficulties": count_by(tasks, "difficulty"),
            "categories": count_by(tasks, "category"),
            "negative_count_min": min(negative_counts) if negative_counts else 0,
            "negative_count_median": statistics.median(negative_counts) if negative_counts else 0,
            "negative_count_max": max(negative_counts) if negative_counts else 0,
            "solution_loc_min": min(solution_locs) if solution_locs else 0,
            "solution_loc_median": statistics.median(solution_locs) if solution_locs else 0,
            "solution_loc_max": max(solution_locs) if solution_locs else 0,
        },
        "release_wording_recommendation": (
            "Until duplicate/high-overlap groups are manually resolved, describe v3 as "
            "\"300 candidate task directories\" rather than \"300 high-quality independent tasks\"."
        ),
        "issue29_named_groups": build_issue_group_reports(tasks_by_name),
        "coarse_scan": build_coarse_scan(tasks, issue_pair_key_set()),
        "risks_by_task": risks_by_task,
        "method": {
            "similarity": (
                "Prompt/checker/solution overlap uses token Jaccard plus difflib sequence ratios on "
                "normalized text. These are triage signals, not final benchmark admission decisions."
            ),
            "negative_count": (
                "Both legacy cases/artifact and v3 variants/path negative manifest schemas are counted; "
                "the report also counts concrete .va files under negative_variants/."
            ),
            "source_family_heuristic": (
                "A row is treated as source-family when its task id contains `_source_`, matching the "
                "current v3 source-import lineage marker."
            ),
            "manual_adjudication": (
                "Named groups may include explicit manual adjudication notes when a human review has "
                "already resolved the automatic triage signal for the current audit slice."
            ),
        },
    }
    return report


def count_by(tasks: list[TaskInfo], attr: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for task in tasks:
        value = getattr(task, attr) or "<missing>"
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", "<br>")


def render_markdown(report: dict[str, Any]) -> str:
    scope = report["scope"]
    lines = [
        "# Issue #29 Duplicate and Filler Audit",
        "",
        "> Report-only audit for vaBench v3. This file is generated by "
        "`benchmark-vabench-release-v3/scripts/audit_issue29_duplicates.py`.",
        "",
        "## Scope",
        "",
        f"- Release: `{report['release']}`",
        f"- Generated UTC: `{report['generated_at_utc']}`",
        f"- Task directories scanned: **{scope['task_count']}**",
        f"- Forms: `{scope['forms']}`",
        f"- Levels: `{scope['levels']}`",
        f"- Source-family heuristic rows: **{scope['source_family_heuristic_count']}**",
        f"- Negative variants per task: min `{scope['negative_count_min']}`, median `{scope['negative_count_median']}`, max `{scope['negative_count_max']}`",
        f"- Solution LOC: min `{scope['solution_loc_min']}`, median `{scope['solution_loc_median']}`, max `{scope['solution_loc_max']}`",
        "",
        "## Release Wording Recommendation",
        "",
        f"- {report['release_wording_recommendation']}",
        "",
        "## Issue #29 Named Groups",
        "",
        "| Group | Classification | Members | Why flagged | Recommendation signal |",
        "| --- | --- | --- | --- | --- |",
    ]
    for group in report["issue29_named_groups"]:
        pair_labels = sorted({pair["classification"] for pair in group["pairs"]})
        signal = ", ".join(pair_labels) if pair_labels else "missing_or_singleton"
        if group.get("manual_adjudication"):
            signal = f"{signal}; manual={group['manual_adjudication']['status']}"
        members = ", ".join(f"`{member['name']}`" for member in group["members"])
        lines.append(
            f"| `{group['id']}` | `{group['classification']}` | {members} | "
            f"{md_escape(group['why_flagged'])} | `{signal}` |"
        )

    lines.extend(["", "## Named Group Pair Evidence", ""])
    for group in report["issue29_named_groups"]:
        lines.extend([f"### `{group['id']}`", ""])
        if group["missing_tasks"]:
            lines.append(f"- Missing tasks: `{group['missing_tasks']}`")
        lines.append(f"- Why flagged: {group['why_flagged']}")
        lines.append(f"- Group classification: `{group['classification']}`")
        if group.get("manual_adjudication"):
            manual = group["manual_adjudication"]
            lines.append(f"- Automatic classification before manual review: `{group['auto_classification']}`")
            lines.append(f"- Manual status: {manual['status']}")
            lines.append(f"- Manual decision: {manual['decision']}")
            lines.append(f"- Manual evidence: {manual['evidence']}")
        if group["pairs"]:
            lines.extend(
                [
                    "",
                    "| Pair | Class | Prompt sim | Solution sim | Checker sim | Recommendation |",
                    "| --- | --- | ---: | ---: | ---: | --- |",
                ]
            )
            for pair in group["pairs"]:
                m = pair["metrics"]
                lines.append(
                    f"| `{pair['task_a']}` ↔ `{pair['task_b']}` | `{pair['classification']}` | "
                    f"{m['prompt_sequence_similarity']} | {m['solution_sequence_similarity']} | "
                    f"{m['checker_sequence_similarity']} | {md_escape(pair['recommendation'])} |"
                )
        lines.extend(["", "<details><summary>Prompt excerpts used for human review</summary>", ""])
        for task_name, excerpt in group["prompt_excerpts"].items():
            lines.extend([f"#### `{task_name}`", "", "~~~markdown", excerpt, "~~~", ""])
        lines.extend(["</details>", ""])

    coarse = report["coarse_scan"]
    lines.extend(
        [
            "## Full 300-Task Coarse Scan",
            "",
            "### Duplicate Titles",
            "",
        ]
    )
    if coarse["duplicate_titles"]:
        for title_key, tasks in coarse["duplicate_titles"].items():
            lines.append(f"- `{title_key}`: " + ", ".join(f"`{task}`" for task in tasks))
    else:
        lines.append("- None found.")

    lines.extend(["", "### Exact Normalized Solution Duplicates", ""])
    if coarse["exact_solution_duplicates"]:
        for solution_hash, tasks in coarse["exact_solution_duplicates"].items():
            lines.append(f"- `{solution_hash}`: " + ", ".join(f"`{task}`" for task in tasks))
    else:
        lines.append("- None found.")

    lines.extend(
        [
            "",
            "### Top Near-Solution Overlap Pairs",
            "",
            "| Pair | Issue named | Class | Solution sim | Checker sim | Forms | Titles |",
            "| --- | --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in coarse["near_solution_pairs"][:40]:
        lines.append(
            f"| `{row['task_a']}` ↔ `{row['task_b']}` | `{row['issue_named_pair']}` | "
            f"`{row['classification']}` | {row['solution_similarity']} | "
            f"{row['checker_similarity']} | `{row['forms']}` | {md_escape(str(row['titles']))} |"
        )

    lines.extend(
        [
            "",
            "### Top Prompt-Overlap Pairs",
            "",
            "| Pair | Issue named | Prompt sim | Forms | Titles |",
            "| --- | --- | ---: | --- | --- |",
        ]
    )
    for row in coarse["prompt_overlap_pairs"][:40]:
        lines.append(
            f"| `{row['task_a']}` ↔ `{row['task_b']}` | `{row['issue_named_pair']}` | "
            f"{row['prompt_similarity']} | `{row['forms']}` | {md_escape(str(row['titles']))} |"
        )

    lines.extend(
        [
            "",
            "### Task-Level Risk Flags",
            "",
            "| Task | Form | Level | Category | LOC | Negatives | Risks |",
            "| --- | --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in coarse["task_risks"][:120]:
        lines.append(
            f"| `{row['name']}` | `{row['form']}` | `{row['level']}` | `{row['category']}` | "
            f"{row['solution_loc']} | {row['negative_count']} | "
            f"{', '.join(f'`{risk}`' for risk in row['risks'])} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation Notes",
            "",
            "- Similarity scores are triage evidence. A pair with high overlap can still be retained if the public spec, artifact role, hidden checker, and negative variants test genuinely different skills.",
            "- Cross-form variants such as DUT vs testbench or DUT vs bugfix should not automatically be deleted; they need explicit counting policy so release claims do not double-count one circuit function as independent coverage.",
            "- Short source-family rows are not automatically invalid, but they need strong negatives and circuit-meaningful wording to avoid becoming source-import filler.",
            "- The JSON report contains all rows beyond the truncated Markdown tables.",
            "",
        ]
    )
    return "\n".join(lines)


def write_reports(report: dict[str, Any], json_out: Path, md_out: Path) -> None:
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_out.write_text(render_markdown(report) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", type=Path, default=JSON_REPORT)
    parser.add_argument("--md-out", type=Path, default=MD_REPORT)
    args = parser.parse_args(argv)

    report = build_report()
    write_reports(report, args.json_out, args.md_out)
    print(f"wrote {args.json_out}")
    print(f"wrote {args.md_out}")
    print(json.dumps(report["scope"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
