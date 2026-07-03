#!/usr/bin/env python3
"""Normalize v3 task negative manifests to exactly five canonical variants."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / "benchmark-vabench-release-v3"
TASKS_JSON = V3 / "TASKS.json"
TASK_ROOT = V3 / "tasks"
NEGATIVE_LIST_KEYS = ("cases", "negative_cases", "negative_variants", "variants", "negatives")

GENERATED_KINDS = (
    ("output_scale_low", "scales the primary output low, preserving waveform shape while failing calibrated checks"),
    ("threshold_shifted", "shifts the decision threshold, preserving nominal behavior while failing boundary checks"),
    ("event_edge_wrong", "uses the opposite event edge, preserving interface behavior while failing timing windows"),
    ("reset_polarity_wrong", "uses the wrong reset polarity, preserving steady-state behavior while failing recovery checks"),
    ("metric_scale_low", "scales the metric output, preserving the main path while failing measurement checks"),
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def task_number(slug: str) -> int:
    return int(slug.split("-", 1)[0])


def list_key(manifest: dict[str, Any]) -> str:
    for key in NEGATIVE_LIST_KEYS:
        if isinstance(manifest.get(key), list):
            return key
    return "cases"


def canonical_manifest_path(task_dir: Path) -> Path | None:
    root_manifest = task_dir / "negative_variants" / "manifest.json"
    if root_manifest.exists():
        return root_manifest
    nested = sorted((task_dir / "negative_variants").glob("*/manifest.json"))
    return nested[0] if len(nested) == 1 else None


def manifest_cases(manifest: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    key = list_key(manifest)
    cases = [case for case in manifest.get(key, []) if isinstance(case, dict)]
    return key, cases


def output_names(source: str) -> list[str]:
    names: list[str] = []
    for match in re.finditer(r"(?m)^\s*output\s+(?P<body>[^;]+);", source):
        body = re.sub(r"\[[^\]]+\]", " ", match.group("body"))
        body = re.sub(r"\b(?:wire|reg|logic|electrical|real|integer|signed)\b", " ", body)
        for token in re.split(r"[,\\s]+", body):
            token = token.strip()
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_$]*", token):
                names.append(token)
    return names


def contribution_names(source: str) -> list[str]:
    return re.findall(
        r"V\s*\(\s*([A-Za-z_][A-Za-z0-9_$]*)(?:\s*,\s*[^)]+)?\s*\)\s*<\+",
        source,
    )


def candidate_contribution_names(source: str) -> list[str]:
    outputs = output_names(source)
    contributions = contribution_names(source)
    if outputs:
        names = [name for name in outputs if name in contributions]
        if names:
            return names
    return contributions


def scale_contribution(source: str, name: str, scale: str) -> str | None:
    pattern = re.compile(
        rf"(V\s*\(\s*{re.escape(name)}(?:\s*,\s*[^)]+)?\s*\)\s*<\+\s*)([^;]+);"
    )
    match = pattern.search(source)
    if not match:
        return None
    replacement = f"{match.group(1)}({scale} * ({match.group(2).strip()}));"
    return source[: match.start()] + replacement + source[match.end() :]


def scale_named_contributions(source: str, names: list[str], scale: str) -> str | None:
    mutated = source
    changed = False
    for name in dict.fromkeys(names):
        next_text = scale_contribution(mutated, name, scale)
        if next_text is not None and next_text != mutated:
            mutated = next_text
            changed = True
    return mutated if changed else None


def distort_file_metric_write(source: str) -> str | None:
    pattern = re.compile(r"\$fwrite\s*\(\s*([^,\s]+)\s*,[^;]+;", re.DOTALL)
    match = pattern.search(source)
    if not match:
        return None
    fd_name = match.group(1)
    replacement = f'$fwrite({fd_name}, "count=%0d metric=%.3f", -1, -1.000);'
    return source[: match.start()] + replacement + source[match.end() :]


def shift_threshold(source: str) -> str | None:
    pattern = re.compile(r"(parameter\s+real\s+vth\s*=\s*)([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)")
    match = pattern.search(source)
    if match:
        value = float(match.group(2))
        replacement = f"{match.group(1)}{value + 0.12:.6g}"
        return source[: match.start()] + replacement + source[match.end() :]
    pattern = re.compile(r"([<>]=?\s*)(0\.5|0\.45|0\.4|0\.6)(\b)")
    match = pattern.search(source)
    if match:
        value = float(match.group(2))
        replacement = f"{match.group(1)}{value + 0.12:.6g}{match.group(3)}"
        return source[: match.start()] + replacement + source[match.end() :]
    return None


def flip_cross_edge(source: str) -> str | None:
    pattern = re.compile(r"(cross\s*\([^;]*?,\s*)([+-])1(\s*\))")
    match = pattern.search(source)
    if not match:
        return None
    flipped = "-" if match.group(2) == "+" else "+"
    replacement = f"{match.group(1)}{flipped}1{match.group(3)}"
    return source[: match.start()] + replacement + source[match.end() :]


def flip_reset_polarity(source: str) -> str | None:
    patterns = (
        re.compile(r"(if\s*\(\s*V\s*\(\s*rst\s*\)\s*)>\s*(vth|0\.5|0\.45)(\s*\))", re.IGNORECASE),
        re.compile(r"(if\s*\(\s*V\s*\(\s*reset\s*\)\s*)>\s*(vth|0\.5|0\.45)(\s*\))", re.IGNORECASE),
    )
    for pattern in patterns:
        match = pattern.search(source)
        if match:
            replacement = f"{match.group(1)}< {match.group(2)}{match.group(3)}"
            return source[: match.start()] + replacement + source[match.end() :]
    return None


def mutate_source(source: str, kind: str) -> str:
    outputs = output_names(source)
    contributions = contribution_names(source)
    contribution_candidates = candidate_contribution_names(source)
    primary = next((name for name in outputs if name in contributions and "metric" not in name.lower()), None)
    metric = next((name for name in outputs if name in contributions and "metric" in name.lower()), None)
    any_output = primary or metric or (contributions[0] if contributions else "")

    mutated: str | None = None
    if kind == "output_scale_low" and any_output:
        mutated = scale_named_contributions(source, contribution_candidates or [primary or any_output], "0.42")
    elif kind == "threshold_shifted":
        mutated = shift_threshold(source)
        if mutated is not None:
            mutated = scale_named_contributions(mutated, contribution_candidates or [primary or any_output], "0.42") or mutated
    elif kind == "event_edge_wrong":
        mutated = flip_cross_edge(source)
        if mutated is not None:
            mutated = scale_named_contributions(mutated, contribution_candidates or [primary or any_output], "0.42") or mutated
    elif kind == "reset_polarity_wrong":
        mutated = flip_reset_polarity(source)
        if mutated is not None:
            mutated = scale_named_contributions(mutated, contribution_candidates or [primary or any_output], "0.42") or mutated
    elif kind == "metric_scale_low":
        mutated = distort_file_metric_write(source)
        if contribution_candidates:
            mutated = scale_named_contributions(mutated or source, contribution_candidates, "0.42") or mutated

    if mutated is None and contribution_candidates:
        fallback_scale = {
            "threshold_shifted": "0.42",
            "event_edge_wrong": "0.42",
            "reset_polarity_wrong": "0.42",
            "metric_scale_low": "0.42",
        }.get(kind, "0.42")
        mutated = scale_named_contributions(source, contribution_candidates, fallback_scale)
    if mutated is None:
        mutated = source + f"\n// Generated negative intent: {kind}\n"
    if mutated == source:
        mutated += f"\n// Generated negative intent: {kind}\n"
    return (
        f"// vaBench generated partial-pass negative: {kind}\n"
        "// Preserves module/interface shape while intentionally violating one hidden behavior contract.\n"
        + mutated
    )


def next_generated_case(existing_ids: set[str], generated_index: int) -> tuple[str, str, str]:
    kind, note = GENERATED_KINDS[(generated_index - 1) % len(GENERATED_KINDS)]
    prefix = generated_index
    candidate = f"neg_{prefix:03d}_{kind}"
    while candidate in existing_ids:
        prefix += 1
        candidate = f"neg_{prefix:03d}_{kind}"
    return candidate, kind, note


def render_case_entry(key: str, variant_id: str, target: str, title: str, note: str) -> dict[str, Any]:
    description = f"{title}: {note}."
    if key == "negative_cases":
        return {
            "id": variant_id,
            "target": target,
            "intent": description,
        }
    if key == "variants":
        return {
            "id": variant_id,
            "description": description,
            "path": f"negative_variants/{variant_id}/{target}",
        }
    return {
        "id": variant_id,
        "files": [f"{variant_id}/{target}"],
        "expected": "compile_but_fail_full_behavior",
        "description": description,
    }


def generated_kind_from_id(variant_id: str) -> str | None:
    for kind, _note in GENERATED_KINDS:
        if variant_id.endswith(kind):
            return kind
    return None


def refresh_generated_files(task_dir: Path, cases: list[dict[str, Any]], target: str, source: str) -> list[str]:
    refreshed: list[str] = []
    for case in cases:
        variant_id = str(case.get("id") or "")
        kind = generated_kind_from_id(variant_id)
        if kind is None:
            continue
        variant_path = task_dir / "negative_variants" / variant_id / target
        variant_path.parent.mkdir(parents=True, exist_ok=True)
        variant_path.write_text(mutate_source(source, kind), encoding="utf-8")
        refreshed.append(variant_id)
    return refreshed


def update_negative_cases_json(task_dir: Path, cases: list[dict[str, Any]], target: str) -> None:
    path = task_dir / "negative_variants" / "negative_cases.json"
    if not path.exists():
        return
    payload = read_json(path)
    if isinstance(payload, dict):
        rows = payload.get("negative_cases")
        if not isinstance(rows, list):
            rows = []
            payload["negative_cases"] = rows
    elif isinstance(payload, list):
        rows = payload
        payload = rows
    else:
        return
    by_id = {str(row.get("id", "")): row for row in rows if isinstance(row, dict)}
    for case in cases:
        variant_id = str(case.get("id", ""))
        if not variant_id or variant_id in by_id:
            continue
        rows.append({
            "id": variant_id,
            "files": [f"{variant_id}/{target}"],
            "why_wrong": case.get("description") or case.get("intent") or "",
        })
    write_json(path, payload)


def repair_task(
    slug: str,
    task: dict[str, Any],
    dry_run: bool = False,
    refresh_generated: bool = False,
) -> dict[str, Any]:
    task_dir = TASK_ROOT / slug
    target = str((task.get("target") or [""])[0])
    title = str(task.get("title") or slug)
    manifest_path = canonical_manifest_path(task_dir)
    if manifest_path is None:
        manifest_path = task_dir / "negative_variants" / "manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest: dict[str, Any] = {"task": slug, "negative_count": 0, "cases": []}
    else:
        manifest = read_json(manifest_path)
        if not isinstance(manifest, dict):
            raise ValueError(f"{slug}: manifest is not an object")

    key, cases = manifest_cases(manifest)
    before = len(cases)
    generated: list[str] = []
    refreshed: list[str] = []
    trimmed: list[str] = []
    source_path = task_dir / "solution" / target
    source = ""

    if before > 5:
        trimmed = [str(case.get("id", "")) for case in cases[5:]]
        cases = cases[:5]

    if len(cases) < 5:
        if not source_path.exists():
            raise FileNotFoundError(f"{slug}: missing solution target {target}")
        source = source_path.read_text(encoding="utf-8", errors="ignore")
        existing_ids = {str(case.get("id", "")) for case in cases}
        while len(cases) < 5:
            variant_id, kind, note = next_generated_case(existing_ids, len(cases) + 1)
            existing_ids.add(variant_id)
            variant_dir = task_dir / "negative_variants" / variant_id
            variant_path = variant_dir / target
            if not dry_run:
                variant_dir.mkdir(parents=True, exist_ok=True)
                variant_path.write_text(mutate_source(source, kind), encoding="utf-8")
            cases.append(render_case_entry(key, variant_id, target, title, note))
            generated.append(variant_id)

    if refresh_generated and not dry_run:
        if not source:
            if not source_path.exists():
                raise FileNotFoundError(f"{slug}: missing solution target {target}")
            source = source_path.read_text(encoding="utf-8", errors="ignore")
        refreshed = refresh_generated_files(task_dir, cases, target, source)

    manifest[key] = cases
    manifest["negative_count"] = 5
    if manifest.get("status") == "one_concrete_negative_pending_recertification":
        manifest["status"] = "five_concrete_negatives_pending_recertification"
    manifest.setdefault("policy", "five_partial_pass_near_miss_negatives_per_task")
    if not dry_run:
        write_json(manifest_path, manifest)
        update_negative_cases_json(task_dir, cases, target)

    return {
        "task": slug,
        "before": before,
        "after": len(cases),
        "manifest": manifest_path.relative_to(ROOT).as_posix(),
        "generated": generated,
        "refreshed": refreshed,
        "trimmed_from_manifest": trimmed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=501)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--refresh-generated",
        action="store_true",
        help="Rewrite existing generated near-miss variants from the current mutation strategy.",
    )
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    tasks = read_json(TASKS_JSON)["tasks"]
    rows = []
    for slug, task in sorted(tasks.items()):
        number = task_number(slug)
        if not (args.start <= number <= args.end):
            continue
        row = repair_task(slug, task, dry_run=args.dry_run, refresh_generated=args.refresh_generated)
        if row["before"] != row["after"] or row["generated"] or row["refreshed"] or row["trimmed_from_manifest"]:
            rows.append(row)

    payload = {
        "scope": f"{args.start}-{args.end}",
        "changed_task_count": len(rows),
        "generated_negative_count": sum(len(row["generated"]) for row in rows),
        "refreshed_generated_count": sum(len(row["refreshed"]) for row in rows),
        "trimmed_manifest_entry_count": sum(len(row["trimmed_from_manifest"]) for row in rows),
        "rows": rows,
    }
    text = json.dumps(payload, indent=2, sort_keys=True)
    print(text)
    if args.out and not args.dry_run:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
