#!/usr/bin/env python3
"""Audit vaBench v2 agent-visible specs against invisible checker configs."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_config(root: Path, config_path: Path | None) -> dict:
    path = config_path or (root / "config" / "release_config.json")
    if not path.exists():
        return {
            "task_discovery": {
                "task_card_globs": ["tasks/**/task_release_card.json"],
            }
        }
    return load_json(path)


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def rel(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def resolve_task_path(task_dir: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return task_dir / path


def task_card_paths(root: Path, config: dict) -> list[Path]:
    discovery = config.get("task_discovery", {})
    globs = discovery.get("task_card_globs") or ["tasks/**/task_release_card.json"]
    paths: set[Path] = set()
    for pattern in globs:
        paths.update(root.glob(pattern))
    return sorted(paths)


def artifact_path(artifacts: dict, *keys: str, default: str) -> str:
    for key in keys:
        value = artifacts.get(key)
        if value:
            return value
    return default


def manifest_prompt_path(manifest: dict) -> str:
    return manifest.get("agent_prompt", "agent_prompt.md")


def manifest_spec_path(manifest: dict) -> str:
    return manifest.get("agent_visible_spec", "public/agent_visible_spec.md")


def visible_block(manifest: dict) -> dict:
    return manifest.get("agent_visible", {})


def visible_target_files(manifest: dict) -> list[str]:
    visible = visible_block(manifest)
    return visible.get("target_files", [])


def hidden_files(manifest: dict) -> list[dict]:
    return manifest.get("agent_hidden", [])


def load_renderer():
    script_path = Path(__file__).with_name("render_agent_prompt.py")
    spec = importlib.util.spec_from_file_location("render_agent_prompt", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load renderer from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def forbidden_hits(text: str, phrases: list[str]) -> list[str]:
    normalized = normalize(text)
    return [phrase for phrase in phrases if normalize(phrase) in normalized]


def missing_terms(text: str, terms: list[str]) -> list[str]:
    normalized = normalize(text)
    return [term for term in terms if normalize(term) not in normalized]


def extract_yaml_list_after_key(text: str, key: str) -> list[str]:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip() != f"{key}:":
            continue
        base_indent = len(line) - len(line.lstrip())
        items: list[str] = []
        for raw in lines[idx + 1 :]:
            stripped = raw.strip()
            if not stripped:
                continue
            indent = len(raw) - len(raw.lstrip())
            if indent <= base_indent and not stripped.startswith("- "):
                break
            if stripped.startswith("- "):
                item = stripped[2:].strip().strip('"').strip("'")
                items.append(item)
        return items
    return []


def extract_yaml_scalar_after_parent(text: str, parent: str, key: str) -> str | None:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip() != f"{parent}:":
            continue
        base_indent = len(line) - len(line.lstrip())
        for raw in lines[idx + 1 :]:
            stripped = raw.strip()
            if not stripped:
                continue
            indent = len(raw) - len(raw.lstrip())
            if indent <= base_indent:
                break
            prefix = f"{key}:"
            if stripped.startswith(prefix):
                return stripped[len(prefix):].strip().strip('"').strip("'")
    return None


def rendered_support_paths(manifest: dict) -> list[str]:
    visible = visible_block(manifest)
    support = visible.get("support_files") or visible.get("support_artifacts", [])
    return [item.get("source_path", "") for item in support]


def audit_form(release_task_path: Path, root: Path, repo_root: Path, renderer) -> dict:
    task_dir = release_task_path.parent
    release_task = load_json(release_task_path)
    artifacts = release_task.get("artifacts", {})
    errors: list[str] = []
    warnings: list[str] = []

    manifest_path = resolve_task_path(
        task_dir,
        artifact_path(
            artifacts,
            "agent_visible_files",
            default="agent_visible_files.json",
        ),
    )
    if not manifest_path.exists():
        return {
            "task_id": release_task.get("id"),
            "release_task": rel(release_task_path, repo_root),
            "status": "FAIL",
            "errors": [f"missing agent visible files manifest: {manifest_path}"],
            "warnings": [],
            "requirement_link_count": 0,
        }
    manifest = load_json(manifest_path)

    trace_raw = artifact_path(
        artifacts,
        "invisible_spec_checker_map",
        default="",
    )
    if not trace_raw:
        errors.append("task release card artifacts missing invisible_spec_checker_map")
        trace_path = task_dir / "private" / "invisible_spec_checker_map.json"
    else:
        trace_path = resolve_task_path(task_dir, trace_raw)

    public_prompt_path = resolve_task_path(
        task_dir,
        artifact_path(artifacts, "agent_prompt", default=manifest_prompt_path(manifest)),
    )
    public_spec_path = resolve_task_path(
        task_dir,
        artifact_path(artifacts, "agent_visible_spec", default=manifest_spec_path(manifest)),
    )
    checks_path = resolve_task_path(
        task_dir,
        artifact_path(
            artifacts,
            "invisible_checker_config",
            default="private/invisible_checker_config.yaml",
        ),
    )

    required_paths = {
        "agent_prompt": public_prompt_path,
        "agent_visible_spec": public_spec_path,
        "invisible_checker_config": checks_path,
        "invisible_spec_checker_map": trace_path,
    }
    for label, path in required_paths.items():
        if not path.exists():
            errors.append(f"missing {label}: {path}")

    support_paths = [resolve_task_path(task_dir, path) for path in artifacts.get("public_support", [])]
    private_gold_paths = [resolve_task_path(task_dir, path) for path in artifacts.get("private_gold", [])]
    for path in support_paths:
        if not path.exists():
            errors.append(f"missing public support artifact: {path}")
    for path in private_gold_paths:
        if not path.exists():
            errors.append(f"missing private gold artifact: {path}")

    manifest_targets = sorted(visible_target_files(manifest))
    private_gold_basenames = sorted(path.name for path in private_gold_paths)
    if manifest_targets != private_gold_basenames:
        errors.append(
            "target_files do not match private gold basenames: "
            f"manifest={manifest_targets} private_gold={private_gold_basenames}"
        )

    manifest_support = sorted(rendered_support_paths(manifest))
    release_support = sorted(artifacts.get("public_support", []))
    if manifest_support != release_support:
        errors.append(f"public support mismatch: manifest={manifest_support} task_release_card={release_support}")

    hidden_paths = {item.get("path") for item in hidden_files(manifest)}
    if trace_raw and trace_raw not in hidden_paths:
        errors.append(f"invisible spec-checker map not listed as agent_hidden: {trace_raw}")
    for gold in artifacts.get("private_gold", []):
        if gold not in hidden_paths:
            errors.append(f"private gold not listed as agent_hidden: {gold}")

    public_prompt_text = public_prompt_path.read_text(encoding="utf-8") if public_prompt_path.exists() else ""
    public_spec_text = public_spec_path.read_text(encoding="utf-8") if public_spec_path.exists() else ""
    public_contract_text = public_prompt_text + "\n\n" + public_spec_text
    checks_text = checks_path.read_text(encoding="utf-8") if checks_path.exists() else ""
    rendered_text = renderer.render_agent_prompt(manifest_path)

    runner_text = ""
    trace: dict = {}
    if trace_path.exists():
        trace = load_json(trace_path)
        if trace.get("schema_version") != "vabench-release-v2-invisible-spec-checker-map":
            errors.append("invisible spec-checker map schema_version mismatch")
        if trace.get("task_id") != release_task.get("id"):
            errors.append(f"invisible spec-checker map task_id mismatch: {trace.get('task_id')} != {release_task.get('id')}")
        trace_spec = trace.get("source_agent_visible_spec")
        expected_spec = artifact_path(
            artifacts,
            "agent_visible_spec",
            default=manifest_spec_path(manifest),
        )
        if trace_spec != expected_spec:
            errors.append("spec-checker map source spec does not match task release artifact")
        trace_checks = trace.get("source_invisible_checker_config")
        expected_checks = artifact_path(
            artifacts,
            "invisible_checker_config",
            default="private/invisible_checker_config.yaml",
        )
        if trace_checks != expected_checks:
            errors.append("spec-checker map source checker config does not match task release artifact")

        checker_file = trace.get("source_checker", {}).get("file")
        if checker_file:
            checker_path = repo_root / checker_file
            if not checker_path.exists():
                errors.append(f"missing source checker file: {checker_file}")
            else:
                runner_text = checker_path.read_text(encoding="utf-8")
        else:
            errors.append("invisible spec-checker map missing source_checker.file")

    checker_task_id = extract_yaml_scalar_after_parent(checks_text, "checker", "task_id")
    if not checker_task_id:
        errors.append("private invisible_checker_config.yaml missing checker.task_id consumed by evaluator")
    elif checker_task_id not in trace.get("source_checker", {}).get("task_aliases", []):
        errors.append(f"invisible_checker_config.yaml checker.task_id not present in spec-checker aliases: {checker_task_id}")

    requirement_links = trace.get("requirement_links", [])
    if not requirement_links:
        errors.append("invisible spec-checker map has no requirement_links")

    checker_function = extract_yaml_scalar_after_parent(checks_text, "checker", "function")
    trace_checker_functions = {
        function
        for link in requirement_links
        for function in link.get("checker_functions", [])
    }
    if not checker_function:
        errors.append("private invisible_checker_config.yaml missing checker.function consumed by evaluator")
    elif checker_function not in trace_checker_functions:
        errors.append(f"invisible_checker_config.yaml checker.function not linked in spec-checker map: {checker_function}")
    elif runner_text and checker_function not in runner_text:
        errors.append(f"invisible_checker_config.yaml checker.function not present in runner: {checker_function}")

    forbidden_terms: list[str] = list(trace.get("auditor", {}).get("forbidden_public_terms", []))
    for link in requirement_links:
        link_id = link.get("id", "unnamed_requirement_link")
        anchors = link.get("public_anchor_terms", [])
        missing_anchor_terms = missing_terms(public_contract_text, anchors)
        if missing_anchor_terms:
            errors.append(f"{link_id}: public spec missing anchors {missing_anchor_terms}")

        check_ids = link.get("checker_config_ids", [])
        missing_check_ids = [item for item in check_ids if item not in checks_text]
        if missing_check_ids:
            errors.append(f"{link_id}: invisible checker config missing IDs {missing_check_ids}")
        forbidden_terms.extend(check_ids)

        checker_functions = link.get("checker_functions", [])
        missing_checker_functions = [item for item in checker_functions if item not in runner_text]
        if missing_checker_functions:
            errors.append(f"{link_id}: runner missing checker functions {missing_checker_functions}")
        forbidden_terms.extend(checker_functions)

    public_hits = forbidden_hits(public_contract_text, sorted(set(forbidden_terms)))
    if public_hits:
        errors.append(f"agent prompt/spec leaked private requirement/checker terms: {public_hits}")
    rendered_hits = forbidden_hits(rendered_text, sorted(set(forbidden_terms)))
    if rendered_hits:
        errors.append(f"rendered agent prompt leaked private requirement/checker terms: {rendered_hits}")

    observables = extract_yaml_list_after_key(checks_text, "public_observables")
    for observable in observables:
        if observable == "time":
            if "implicit transient waveform axis" not in normalize(public_contract_text):
                warnings.append("public_observables includes time; public spec should describe it as the implicit waveform axis")
            continue
        if normalize(observable) not in normalize(rendered_text):
            errors.append(f"public observable not present in rendered agent prompt: {observable}")

    aliases = trace.get("source_checker", {}).get("task_aliases", [])
    if aliases and runner_text and not any(alias in runner_text for alias in aliases):
        warnings.append(f"none of source_checker.task_aliases appears literally in runner: {aliases}")

    return {
        "task_id": release_task.get("id"),
        "release_task": rel(release_task_path, repo_root),
        "invisible_spec_checker_map": rel(trace_path, repo_root) if trace_path.exists() else str(trace_path),
        "status": "FAIL" if errors else "PASS",
        "errors": errors,
        "warnings": warnings,
        "requirement_link_count": len(requirement_links),
        "public_observable_count": len(observables),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="benchmark-vabench-release-v2 root directory",
    )
    parser.add_argument("--config", type=Path, help="optional v2 release_config.json path")
    parser.add_argument("--output", type=Path, help="optional JSON report path")
    args = parser.parse_args()

    root = args.root
    repo_root = root.resolve().parent
    config = load_config(root, args.config)
    renderer = load_renderer()
    release_tasks = task_card_paths(root, config)
    results = [audit_form(path, root, repo_root, renderer) for path in release_tasks]
    summary = {
        "root": str(root),
        "config": str(args.config or (root / "config" / "release_config.json")),
        "release": config.get("release", "vabench-release-v2"),
        "form_count": len(release_tasks),
        "spec_checker_map_count": sum(1 for item in results if item.get("requirement_link_count", 0) > 0),
        "requirement_link_count": sum(item.get("requirement_link_count", 0) for item in results),
        "status": "FAIL" if any(item["status"] == "FAIL" for item in results) else "PASS",
        "results": results,
    }
    payload = json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 1 if summary["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
