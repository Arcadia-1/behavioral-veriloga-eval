#!/usr/bin/env python3
"""Render a vaBench v2 agent-visible prompt from an allowlist manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


RENDERER_VERSION = "vabench-release-v2-renderer-v2"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_task_path(task_dir: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return task_dir / path


def release_root_for_manifest(manifest_path: Path) -> Path:
    for parent in [manifest_path.parent, *manifest_path.parents]:
        if (parent / "config" / "release_config.json").exists():
            return parent
    return Path(__file__).resolve().parents[1]


def load_release_config(release_root: Path) -> dict:
    config_path = release_root / "config" / "release_config.json"
    if not config_path.exists():
        return {}
    return load_json(config_path)


def common_prompt_text(manifest_path: Path) -> str:
    release_root = release_root_for_manifest(manifest_path)
    config = load_release_config(release_root)
    prompt_protocol = config.get("prompt_protocol", {})
    common_path_raw = prompt_protocol.get("common_agent_prompt", "config/common_agent_prompt.md")
    if not common_path_raw:
        return ""
    common_path = Path(common_path_raw)
    if not common_path.is_absolute():
        common_path = release_root / common_path
    if not common_path.exists():
        raise FileNotFoundError(f"common agent prompt not found: {common_path}")
    return common_path.read_text(encoding="utf-8").strip()


def artifact_language(filename: str) -> str:
    if filename.endswith(".va"):
        return "verilog"
    if filename.endswith(".scs"):
        return "spectre"
    return "text"


def manifest_prompt_path(manifest: dict) -> str:
    return manifest.get("agent_prompt", "agent_prompt.md")


def manifest_spec_path(manifest: dict) -> str:
    return manifest.get("agent_visible_spec", "public/agent_visible_spec.md")


def visible_block(manifest: dict) -> dict:
    return manifest.get("agent_visible", {})


def visible_support_files(manifest: dict) -> list[dict]:
    visible = visible_block(manifest)
    return visible.get("support_files", [])


def visible_target_files(manifest: dict) -> list[str]:
    visible = visible_block(manifest)
    return visible.get("target_files", [])


def render_agent_prompt(manifest_path: Path) -> str:
    manifest = load_json(manifest_path)
    task_dir = manifest_path.parent
    common_prompt = common_prompt_text(manifest_path)
    agent_prompt_path = resolve_task_path(task_dir, manifest_prompt_path(manifest))
    agent_prompt = agent_prompt_path.read_text(encoding="utf-8").strip()
    agent_visible_spec = ""
    agent_visible_spec_path_raw = manifest_spec_path(manifest)
    if agent_visible_spec_path_raw:
        agent_visible_spec_path = resolve_task_path(task_dir, agent_visible_spec_path_raw)
        agent_visible_spec = agent_visible_spec_path.read_text(encoding="utf-8").strip()

    lines = [
        f"Renderer version: `{RENDERER_VERSION}`",
        "",
    ]

    if common_prompt:
        lines.extend(
            [
                "Common agent rules:",
                "",
                common_prompt,
                "",
            ]
        )

    lines.extend(
        [
            "Question:",
            agent_prompt,
            "",
        ]
    )

    if agent_visible_spec:
        lines.extend(
            [
                "Agent-visible task specification:",
                "",
                agent_visible_spec,
                "",
            ]
        )

    support_artifacts = visible_support_files(manifest)
    rendered_support = [item for item in support_artifacts if item.get("render", False)]
    if rendered_support:
        lines.extend(
            [
                "Agent-visible support file contents:",
                "",
                "The following files are supplied agent-visible read-only inputs.",
                "Do not return these files unless also listed as target files.",
                "",
            ]
        )
        for item in rendered_support:
            alias = item["alias"]
            source_path = resolve_task_path(task_dir, item["source_path"])
            contents = source_path.read_text(encoding="utf-8").strip()
            language = artifact_language(alias)
            lines.extend(
                [
                    f"[BEGIN support file: {alias}]",
                    f"```{language}",
                    contents,
                    "```",
                    f"[END support file: {alias}]",
                    "",
                ]
            )

    target_files = visible_target_files(manifest)
    lines.extend(
        [
            "Target artifact contract:",
            "",
            *[f"- `{artifact}`" for artifact in target_files],
            "",
            "Return only the target artifact contents using the requested filenames.",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rendered = render_agent_prompt(args.manifest)
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
