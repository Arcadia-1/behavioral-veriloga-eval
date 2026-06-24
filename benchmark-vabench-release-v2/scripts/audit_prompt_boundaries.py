#!/usr/bin/env python3
"""Audit vaBench v2 prompt/public/private boundaries."""
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
            "prompt_protocol": {
                "public_support_dir": "public/support",
            }
        }
    return load_json(path)


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def load_renderer():
    script_path = Path(__file__).with_name("render_agent_prompt.py")
    spec = importlib.util.spec_from_file_location("render_agent_prompt", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load renderer from {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def resolve_task_path(task_dir: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return task_dir / path


def first_existing_path(task_dir: Path, filenames: list[str]) -> Path:
    for filename in filenames:
        path = task_dir / filename
        if path.exists():
            return path
    return task_dir / filenames[0]


def manifest_prompt_path(manifest: dict) -> str:
    return manifest.get("agent_prompt", "agent_prompt.md")


def manifest_spec_path(manifest: dict) -> str:
    return manifest.get("agent_visible_spec", "public/agent_visible_spec.md")


def visible_block(manifest: dict) -> dict:
    return manifest.get("agent_visible", {})


def visible_support_files(manifest: dict) -> list[dict]:
    visible = visible_block(manifest)
    return visible.get("support_files", [])


def hidden_files(manifest: dict) -> list[dict]:
    return manifest.get("agent_hidden", [])


def forbidden_hits(text: str, phrases: list[str]) -> list[str]:
    normalized = normalize(text)
    return [phrase for phrase in phrases if normalize(phrase) in normalized]


def missing_public_anchors(text: str, anchors: list[dict]) -> list[dict]:
    normalized = normalize(text)
    missing: list[dict] = []
    for anchor in anchors:
        required = anchor.get("all_of", [])
        missing_terms = [term for term in required if normalize(term) not in normalized]
        if missing_terms:
            missing.append({
                "id": anchor.get("id", "unnamed_anchor"),
                "missing": missing_terms,
            })
    return missing


def requires_saved_signal_contract(text: str) -> bool:
    return "- save `" in text or "\nsave `" in text


def has_saved_signal_contract(text: str) -> bool:
    normalized = normalize(text)
    return (
        "saved signal names are part of the public contract" in normalized
        and (
            "actual top-level spectre net" in normalized
            or "top-level spectre nets connected" in normalized
        )
    )


def unique_phrases(values: list[str]) -> list[str]:
    seen: set[str] = set()
    phrases: list[str] = []
    for value in values:
        normalized = normalize(value)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        phrases.append(value)
    return phrases


def private_forbidden_phrases(task_dir: Path, task_card: dict, manifest: dict) -> list[str]:
    phrases: list[str] = []
    phrases.extend(manifest.get("leak_audit", {}).get("forbidden_phrases", []))

    trace_raw_path = task_card.get("artifacts", {}).get(
        "invisible_spec_checker_map",
        "private/invisible_spec_checker_map.json",
    )
    trace_path = resolve_task_path(task_dir, trace_raw_path)
    if trace_path.exists():
        trace = load_json(trace_path)
        phrases.extend(trace.get("auditor", {}).get("forbidden_public_terms", []))
        for link in trace.get("requirement_links", []):
            phrases.extend(link.get("private_policy_terms", []))

    return unique_phrases(phrases)


def common_prompt_path(root: Path, config: dict) -> Path | None:
    raw_path = config.get("prompt_protocol", {}).get("common_agent_prompt", "")
    if not raw_path:
        return None
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return root / path


def common_prompt_text(root: Path, config: dict, errors: list[str]) -> str:
    path = common_prompt_path(root, config)
    if path is None:
        return ""
    if not path.exists():
        errors.append(f"missing common agent prompt: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def audit_manifest(manifest_path: Path, renderer, config: dict) -> dict:
    task_dir = manifest_path.parent
    root = Path(config.get("_root", Path(__file__).resolve().parents[1]))
    manifest = load_json(manifest_path)
    errors: list[str] = []
    task_card: dict = {}
    common_text = common_prompt_text(root, config, errors)

    public_prompt_path = resolve_task_path(task_dir, manifest_prompt_path(manifest))
    public_spec_path_raw = manifest_spec_path(manifest)
    public_spec_path = resolve_task_path(task_dir, public_spec_path_raw) if public_spec_path_raw else None
    private_task_card_path = first_existing_path(task_dir, ["task_release_card.json"])
    public_support_root = task_dir / config["prompt_protocol"].get("public_support_dir", "public/support")

    if not public_prompt_path.exists():
        errors.append(f"missing agent prompt: {public_prompt_path}")
        public_prompt_text = ""
    else:
        public_prompt_text = public_prompt_path.read_text(encoding="utf-8")

    if public_spec_path is None:
        errors.append("missing agent-visible spec field")
        public_spec_text = ""
    elif not public_spec_path.exists():
        errors.append(f"missing agent-visible spec: {public_spec_path}")
        public_spec_text = ""
    else:
        public_spec_text = public_spec_path.read_text(encoding="utf-8")
        if not is_relative_to(public_spec_path, task_dir / "public"):
            errors.append(f"public spec must live under public/: {public_spec_path}")

    public_contract_text = common_text + "\n\n" + public_prompt_text + "\n\n" + public_spec_text

    if not private_task_card_path.exists():
        errors.append(f"missing private task card: {private_task_card_path}")
    else:
        task_card = load_json(private_task_card_path)
        if task_card.get("visibility") != "internal_only":
            errors.append("task_release_card.json visibility must be internal_only")

    hidden_paths = {item.get("path") for item in hidden_files(manifest)}
    task_card_name = private_task_card_path.name
    if task_card_name not in hidden_paths:
        errors.append(f"{task_card_name} must be listed as agent_hidden")

    for item in visible_support_files(manifest):
        source_path = resolve_task_path(task_dir, item["source_path"])
        if not source_path.exists():
            errors.append(f"missing support artifact: {source_path}")
        if not is_relative_to(source_path, public_support_root):
            errors.append(f"support artifact must live under public/support: {source_path}")
        if item.get("writable_by_agent") is not False:
            errors.append(f"support file must be read-only for agent: {item.get('alias')}")

    for item in hidden_files(manifest):
        hidden_path = resolve_task_path(task_dir, item["path"])
        if not hidden_path.exists():
            errors.append(f"missing hidden artifact: {hidden_path}")
        if is_relative_to(hidden_path, task_dir / "public"):
            errors.append(f"hidden artifact cannot live under public/: {hidden_path}")

    phrases = private_forbidden_phrases(task_dir, task_card, manifest)
    public_hits = forbidden_hits(public_contract_text, phrases)
    if public_hits:
        errors.append(f"public prompt/spec leak phrases: {public_hits}")

    contract_anchors = manifest.get("contract_audit", {}).get("required_public_anchors", [])
    missing_anchors = missing_public_anchors(public_contract_text, contract_anchors)
    if missing_anchors:
        errors.append(f"public prompt/spec missing contract anchors: {missing_anchors}")

    if requires_saved_signal_contract(public_spec_text) and not has_saved_signal_contract(public_contract_text):
        errors.append(
            "public spec with saved waveforms must state that saved names are "
            "actual top-level Spectre nets, not unconnected aliases"
        )

    rendered = renderer.render_agent_prompt(manifest_path)
    if common_text.strip() and common_text.strip() not in rendered:
        errors.append("rendered agent prompt missing common agent prompt")
    rendered_hits = forbidden_hits(rendered, phrases)
    if rendered_hits:
        errors.append(f"rendered agent prompt leak phrases: {rendered_hits}")

    rendered_missing_anchors = missing_public_anchors(rendered, contract_anchors)
    if rendered_missing_anchors:
        errors.append(f"rendered agent prompt missing contract anchors: {rendered_missing_anchors}")

    return {
        "task_id": manifest.get("task_id"),
        "manifest": str(manifest_path),
        "status": "FAIL" if errors else "PASS",
        "errors": errors,
        "contract_anchor_count": len(contract_anchors),
        "forbidden_phrase_count": len(phrases),
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

    config = load_config(args.root, args.config)
    config["_root"] = str(args.root)
    renderer = load_renderer()
    manifests = sorted({
        *args.root.glob("tasks/**/agent_visible_files.json"),
    })
    results = [audit_manifest(path, renderer, config) for path in manifests]
    summary = {
        "root": str(args.root),
        "config": str(args.config or (args.root / "config" / "release_config.json")),
        "release": config.get("release", "vabench-release-v2"),
        "manifest_count": len(manifests),
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
