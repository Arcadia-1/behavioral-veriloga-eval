#!/usr/bin/env python3
"""
audit_issue29_duplicates.py — v3 task duplicate/source-import filler audit.

Report-only: produces ``issue29_duplicate_and_filler_audit.json`` and
``issue29_duplicate_and_filler_audit.md``.  Never deletes or modifies tasks.

Usage:
    python3 benchmark-vabench-release-v3/scripts/audit_issue29_duplicates.py
"""
from __future__ import annotations

import hashlib
import json
import re
import textwrap
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
TASKS_DIR = ROOT / "tasks"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ─── Helpers ───────────────────────────────────────────────────

def read_task_toml(task_dir: Path) -> dict:
    """Read task.toml, returning {} on any error."""
    toml_path = task_dir / "task.toml"
    if not toml_path.exists():
        return {}
    raw = toml_path.read_text(encoding="utf-8", errors="ignore")
    data: dict = {}
    current_key: str | None = None
    in_array = False
    array_key: str | None = None
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Sections like [artifacts]
        if line.startswith("[") and line.endswith("]"):
            current_key = line.strip("[]")
            continue
        # Arrays
        if line.startswith("[[") and line.endswith("]]"):
            array_key = line.strip("[]")
            data.setdefault(array_key, [])
            continue
        if "=" in line and not line.startswith("[["):
            k, _, v = line.partition("=")
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k == "id":
                data["id"] = v
            elif k == "name":
                data["name"] = v
            elif k == "title":
                data["title"] = v
            elif k == "form":
                data["form"] = v
            elif k == "level":
                data["level"] = v
            elif k == "difficulty":
                data["difficulty"] = v
            elif k == "category":
                data["category"] = v
            elif current_key == "artifacts" and k == "target":
                data.setdefault("targets", []).append(v)
    return data


def solution_files(task_dir: Path) -> list[Path]:
    """Return all .va files under solution/."""
    sol_dir = task_dir / "solution"
    return sorted(sol_dir.rglob("*.va")) if sol_dir.exists() else []


def negative_count(task_dir: Path) -> int:
    neg_dir = task_dir / "negative_variants"
    if not neg_dir.exists():
        return 0
    return len([d for d in neg_dir.iterdir() if d.is_dir() and d.name.startswith("neg_")])


def solution_sha256(task_dir: Path) -> str | None:
    """SHA-256 of normalized (strip whitespace) concatenated solution code."""
    files = solution_files(task_dir)
    if not files:
        return None
    texts: list[str] = []
    for f in files:
        try:
            code = f.read_text(encoding="utf-8", errors="ignore")
            # Normalize: strip leading/trailing whitespace per line
            norm = "".join(line.strip() for line in code.splitlines())
            texts.append(norm)
        except OSError:
            pass
    if not texts:
        return None
    joined = "\n".join(texts)
    return "sha256:" + hashlib.sha256(joined.encode()).hexdigest()


def solution_loc(task_dir: Path) -> int:
    """Count non-blank, non-comment lines across all solution .va files."""
    total = 0
    for f in solution_files(task_dir):
        try:
            for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                s = line.strip()
                if s and not s.startswith("//") and not s.startswith("/*"):
                    total += 1
        except OSError:
            pass
    return total


def token_jaccard(a: str, b: str) -> float:
    """Token-level Jaccard similarity of two strings."""
    set_a = set(a.lower().split())
    set_b = set(b.lower().split())
    if not set_a and not set_b:
        return 1.0
    return len(set_a & set_b) / len(set_a | set_b)


# ─── Scan ──────────────────────────────────────────────────────

def scan_all_tasks() -> dict[str, dict]:
    """Return {task_dir_name: metadata} for all 300 v3 tasks."""
    tasks: dict[str, dict] = {}
    for task_dir in sorted(TASKS_DIR.iterdir()):
        if not task_dir.is_dir():
            continue
        meta = read_task_toml(task_dir)
        name = task_dir.name
        tasks[name] = {
            "name": name,
            "id": meta.get("id", ""),
            "title": meta.get("title", ""),
            "form": meta.get("form", "?"),
            "level": meta.get("level", "?"),
            "difficulty": meta.get("difficulty", "?"),
            "category": meta.get("category", "?"),
            "targets": meta.get("targets", []),
            "solution_loc": solution_loc(task_dir),
            "negative_count": negative_count(task_dir),
            "solution_sha256": solution_sha256(task_dir),
            "path": str(task_dir),
        }
    return tasks


# ─── Similarity analysis ──────────────────────────────────────

def build_sha256_groups(tasks: dict[str, dict]) -> dict[str, list[str]]:
    """Group task names by identical solution SHA-256."""
    groups: dict[str, list[str]] = defaultdict(list)
    for name, meta in tasks.items():
        h = meta.get("solution_sha256")
        if h and h != "sha256:" + "0" * 64:
            groups[h].append(name)
    return groups


def build_pair_metrics(
    a_name: str, a_meta: dict, b_name: str, b_meta: dict
) -> dict:
    """Compute similarity metrics between two tasks."""
    return {
        "task_a": a_name,
        "task_b": b_name,
        "same_form": a_meta.get("form") == b_meta.get("form"),
        "same_category": a_meta.get("category") == b_meta.get("category"),
        "same_level": a_meta.get("level") == b_meta.get("level"),
        "same_solution_sha256": a_meta.get("solution_sha256") == b_meta.get("solution_sha256"),
    }


# ─── Report generation ────────────────────────────────────────

def generate_report(tasks: dict[str, dict]) -> dict:
    sha256_groups = build_sha256_groups(tasks)

    # Classify groups
    identical_solution_groups = []
    source_import_pairs = []
    for h, members in sha256_groups.items():
        if len(members) < 2:
            continue
        members_sorted = sorted(members)
        if len(members_sorted) == 2:
            a, b = members_sorted
            a_meta, b_meta = tasks[a], tasks[b]
            pair_metrics = build_pair_metrics(a, a_meta, b, b_meta)
            # Different form → valid variant
            if not pair_metrics["same_form"]:
                classification = "valid_variant_needs_counting_policy"
                recommendation = (
                    "Same solution in different artifact forms. "
                    "Keep as separate skills but adjust counting labels."
                )
            else:
                classification = "exact_duplicate_needs_merge"
                recommendation = (
                    "Identical solution in same form. "
                    "Differentiate instruction/checker/negatives or merge."
                )
            source_import_pairs.append({
                "classification": classification,
                "pair": [a, b],
                "recommendation": recommendation,
                "metrics": pair_metrics,
            })
        else:
            identical_solution_groups.append({
                "members": members_sorted,
                "sha256": h,
            })

    # Stats
    neg_counts = [m["negative_count"] for m in tasks.values()]
    loc_counts = [m["solution_loc"] for m in tasks.values()]
    forms: dict[str, int] = defaultdict(int)
    for m in tasks.values():
        forms[m["form"]] += 1
    difficulties: dict[str, int] = defaultdict(int)
    for m in tasks.values():
        difficulties[m["difficulty"]] += 1
    categories: dict[str, int] = defaultdict(int)
    for m in tasks.values():
        categories[m["category"]] += 1

    return {
        "report_id": "issue29_duplicate_and_filler_audit",
        "release": "benchmark-vabench-release-v3",
        "task_count": len(tasks),
        "forms": dict(forms),
        "difficulties": dict(difficulties),
        "categories": dict(categories),
        "negative_count_stats": {
            "min": min(neg_counts),
            "median": sorted(neg_counts)[len(neg_counts) // 2],
            "max": max(neg_counts),
            "count_leq_1": sum(1 for c in neg_counts if c <= 1),
        },
        "solution_loc_stats": {
            "min": min(loc_counts),
            "median": sorted(loc_counts)[len(loc_counts) // 2],
            "max": max(loc_counts),
        },
        "identical_solution_groups": identical_solution_groups,
        "duplicate_or_variant_pairs": source_import_pairs,
        "weak_negative_tasks": [
            name for name, m in sorted(tasks.items())
            if m["negative_count"] <= 1
        ],
        "release_wording_recommendation": (
            "Until duplicate/high-overlap groups are resolved, describe v3 as "
            '"300 candidate task directories" rather than '
            '"300 high-quality independent tasks".'
        ),
    }


def write_markdown(report: dict, path: Path) -> None:
    lines = [
        "# Issue #29 — v3 Duplicate and Filler Audit Report",
        "",
        f"Generated: {report.get('report_id', '')}",
        f"Tasks scanned: {report['task_count']}",
        "",
        "## Overview",
        "",
        f"Forms: {report['forms']}",
        f"Difficulties: {report['difficulties']}",
        f"Negative count: min={report['negative_count_stats']['min']}, "
        f"median={report['negative_count_stats']['median']}, "
        f"max={report['negative_count_stats']['max']}",
        f"Tasks with ≤1 negative: {report['negative_count_stats']['count_leq_1']}",
        "",
        "## Identical Solution Groups",
        "",
    ]
    for grp in report.get("identical_solution_groups", []):
        for m in grp["members"]:
            lines.append(f"- {m}")
        lines.append("")
    lines.extend([
        "## Duplicate / Variant Pairs",
        "",
    ])
    for pair in report.get("duplicate_or_variant_pairs", []):
        lines.append(f"### {pair['pair'][0]} × {pair['pair'][1]}")
        lines.append(f"- Classification: {pair['classification']}")
        lines.append(f"- Recommendation: {pair['recommendation']}")
        lines.append("")
    lines.extend([
        "## Weak-Negative Tasks (≤1 negative)",
        "",
    ])
    for name in report.get("weak_negative_tasks", []):
        lines.append(f"- {name}")
    lines.extend([
        "",
        "## Release Wording Recommendation",
        "",
        report.get("release_wording_recommendation", ""),
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


# ─── Main ──────────────────────────────────────────────────────

def main() -> None:
    print(f"Scanning {TASKS_DIR} ...")
    tasks = scan_all_tasks()
    print(f"  Found {len(tasks)} tasks")

    print("Building report ...")
    report = generate_report(tasks)

    json_path = REPORT_DIR / "issue29_duplicate_and_filler_audit.json"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  JSON: {json_path}")

    md_path = REPORT_DIR / "issue29_duplicate_and_filler_audit.md"
    write_markdown(report, md_path)
    print(f"  MD:   {md_path}")

    # Summary
    print()
    print("=== Summary ===")
    print(f"  Identical-solution groups: {len(report.get('identical_solution_groups', []))}")
    dupe_pairs = report.get("duplicate_or_variant_pairs", [])
    dupe_count = sum(1 for p in dupe_pairs if p["classification"] == "exact_duplicate_needs_merge")
    variant_count = sum(1 for p in dupe_pairs if p["classification"] == "valid_variant_needs_counting_policy")
    print(f"  Duplicate pairs (same form): {dupe_count}")
    print(f"  Variant pairs (diff form):   {variant_count}")
    print(f"  Tasks with ≤1 negative:      {report['negative_count_stats']['count_leq_1']}")


if __name__ == "__main__":
    main()
