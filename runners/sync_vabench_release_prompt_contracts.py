#!/usr/bin/env python3
"""Normalize vaBench release prompts around public benchmark contracts.

This script rewrites release `forms/*/prompt.md` files into three explicit
layers:

- a public release task contract derived from `release_task.json` and gold
  artifact names;
- task-specific public description preserved from the existing prompt; and
- no runner-only wrapper, ICL, or repair-feedback text.

It intentionally exposes only evaluator-facing constraints such as artifact
names, module interfaces, saved observables, and transient settings. It does
not copy gold implementation code or hidden checker logic.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = RELEASE_ROOT / "tasks"

SECTION_RE = re.compile(
    r"\n## (?:Output Contract(?:\s*\([^)]*\))?|Deliverables?|Public Evaluation Contract \(Non-Gold\))\n.*?(?=\n## |\Z)",
    re.DOTALL,
)
REFERENCE_LINE_RE = re.compile(r"^Reference (?:testbench )?artifact name\(s\):.*$\n?", re.MULTILINE)
REFERENCE_NAMES_RE = re.compile(r"^Reference (?:testbench )?artifact names:.*$\n?", re.MULTILINE)
BUG_TO_FIX_RE = re.compile(r"^Bug to fix:.*$\n?", re.MULTILINE)
BUG_TO_FIX_INLINE_RE = re.compile(r"\s*Bug to fix:.*?(?=\n|$)", re.MULTILINE)
PUBLIC_CHECKS_SECTION_RE = re.compile(r"\n?Public behavior checks:\n(?:\n?- .*)+", re.MULTILINE)
INJECTED_STRICT_RE = re.compile(
    r"^\s*- Use the final transient setting provided by the injected Strict EVAS Validation Contract\.\n?",
    re.MULTILINE,
)
MODULE_RE = re.compile(r"\bmodule\s+([A-Za-z_]\w*)\s*\((.*?)\)\s*;", re.DOTALL)
SAVE_RE = re.compile(r"^\s*save\s+(.+)$", re.IGNORECASE | re.MULTILINE)
TRAN_RE = re.compile(r"^\s*tran\s+\w+.*$", re.IGNORECASE | re.MULTILINE)
SOURCE_RE = re.compile(r"^\s*[VI]\w*\s+\(([^)\s]+)\s+0\)\s+\w+source\b", re.IGNORECASE | re.MULTILINE)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def task_dirs() -> list[Path]:
    return sorted(path.parent for path in TASKS_ROOT.glob("CT*/vbr1_*/forms/*/release_task.json"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def artifact_paths(release_task: dict) -> list[Path]:
    return [ROOT / str(item) for item in release_task.get("artifacts", {}).get("gold", [])]


def target_artifacts(form: str, gold_paths: list[Path]) -> list[str]:
    names = [path.name for path in gold_paths]
    if form == "dut":
        return [name for name in names if name.endswith(".va") and not name.startswith("tb_")]
    if form == "tb":
        return [name for name in names if name.endswith(".scs")]
    if form == "bugfix":
        fixed = [name for name in names if name == "dut_fixed.va"]
        return fixed or [name for name in names if name.endswith(".va") and "buggy" not in name]
    if form == "e2e":
        return [name for name in names if name.endswith((".va", ".scs"))]
    return [name for name in names if name.endswith((".va", ".scs"))]


def support_artifacts(form: str, gold_paths: list[Path], targets: list[str]) -> list[str]:
    target_set = set(targets)
    names = [path.name for path in gold_paths]
    support = [name for name in names if name not in target_set and name.endswith((".va", ".scs"))]
    if form == "bugfix":
        support = [name for name in support if name != "dut_fixed.va"]
    return support


def normalize_port_name(raw: str) -> str | None:
    item = re.sub(r"\[[^\]]+\]", " ", raw)
    tokens = [token for token in re.split(r"\s+", item.strip()) if token]
    for token in reversed(tokens):
        if re.fullmatch(r"[A-Za-z_]\w*", token):
            return token
    return None


def module_signatures(va_paths: list[Path]) -> list[tuple[str, list[str], str]]:
    rows: list[tuple[str, list[str], str]] = []
    seen: set[tuple[str, str]] = set()
    for path in sorted(va_paths):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in MODULE_RE.finditer(text):
            module = match.group(1)
            ports = [port for part in match.group(2).replace("\n", " ").split(",") if (port := normalize_port_name(part))]
            key = (path.name, module)
            if ports and key not in seen:
                seen.add(key)
                rows.append((path.name, module, ports))
    return rows


def save_columns(scs_paths: list[Path]) -> list[str]:
    columns: list[str] = []
    seen: set[str] = set()
    for path in sorted(scs_paths):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in SAVE_RE.finditer(text):
            body = match.group(1).strip()
            if body.lower().startswith(("all", "none")):
                continue
            for token in re.split(r"\s+", body):
                token = token.strip().strip(",")
                if not token:
                    continue
                token = re.sub(r"^v\(([^)]+)\)$", r"\1", token, flags=re.IGNORECASE)
                token = token.split(":")[-1].split(".")[-1]
                if token and token not in seen:
                    seen.add(token)
                    columns.append(token)
    return columns


def tran_lines(scs_paths: list[Path]) -> list[str]:
    lines: list[str] = []
    seen: set[str] = set()
    for path in sorted(scs_paths):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in TRAN_RE.finditer(text):
            line = re.sub(r"\s+", " ", match.group(0).strip())
            if line not in seen:
                seen.add(line)
                lines.append(line)
    return lines


def source_nodes(scs_paths: list[Path]) -> list[str]:
    nodes: list[str] = []
    seen: set[str] = set()
    for path in sorted(scs_paths):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in SOURCE_RE.finditer(text):
            node = match.group(1).strip()
            if node and node not in seen:
                seen.add(node)
                nodes.append(node)
    return nodes


def behavior_checks(checks_path: Path) -> list[str]:
    if not checks_path.exists():
        return []
    checks: list[str] = []
    in_checks = False
    for line in checks_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if stripped == "checks:":
            in_checks = True
            continue
        if in_checks:
            if stripped.startswith("- "):
                checks.append(stripped[2:].strip().strip('"'))
                continue
            if stripped:
                in_checks = False
    return checks


def strip_existing_scaffold(text: str) -> str:
    marker = "## Task-Specific Public Description"
    if marker in text:
        return text.split(marker, 1)[1].strip()
    return text.strip()


def clean_original(text: str) -> str:
    text = strip_existing_scaffold(text)
    text = SECTION_RE.sub("", text)
    text = REFERENCE_LINE_RE.sub("", text)
    text = REFERENCE_NAMES_RE.sub("", text)
    text = BUG_TO_FIX_RE.sub("", text)
    text = BUG_TO_FIX_INLINE_RE.sub("", text)
    text = PUBLIC_CHECKS_SECTION_RE.sub("", text)
    text = INJECTED_STRICT_RE.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def form_instruction(form: str, targets: list[str]) -> list[str]:
    if form == "dut":
        return [
            "Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.",
            "Preserve the public module names, port order, parameters, and waveform observable names.",
        ]
    if form == "tb":
        return [
            "Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.",
            "Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.",
        ]
    if form == "bugfix":
        return [
            "Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.",
            "Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.",
        ]
    if form == "e2e":
        joined = ", ".join(f"`{name}`" for name in targets)
        return [
            f"Generate all target artifacts: {joined}.",
            "The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.",
        ]
    return ["Preserve the public artifact and evaluator-facing contract."]


def build_prompt(form_dir: Path) -> str:
    release_task = read_json(form_dir / "release_task.json")
    prompt_path = form_dir / "prompt.md"
    original = clean_original(prompt_path.read_text(encoding="utf-8", errors="ignore"))
    form = form_dir.name
    gold_paths = artifact_paths(release_task)
    targets = target_artifacts(form, gold_paths)
    support = support_artifacts(form, gold_paths, targets)
    va_paths = [path for path in gold_paths if path.name.endswith(".va")]
    scs_paths = [path for path in gold_paths if path.name.endswith(".scs")]
    modules = module_signatures(va_paths)
    columns = save_columns(scs_paths)
    trans = tran_lines(scs_paths)
    nodes = source_nodes(scs_paths)
    checks_path = ROOT / str(release_task.get("artifacts", {}).get("checks", ""))
    checks = behavior_checks(checks_path)

    lines: list[str] = [
        f"# Task: {release_task.get('id', form_dir.parent.parent.name + ':' + form)}",
        "",
        "## Release Task Contract",
        "",
        f"- Form: `{form}`",
        f"- Level: `{release_task.get('level', 'unknown')}`",
        f"- Category: {release_task.get('category', 'unknown')}",
        f"- Base function: {release_task.get('base_function', 'unknown')}",
        f"- Domain: `{release_task.get('domain', 'voltage')}`",
    ]
    if targets:
        lines.append("- Target artifact(s): " + ", ".join(f"`{name}`" for name in targets))
    if support:
        lines.append("- Supplied/reference support artifact(s): " + ", ".join(f"`{name}`" for name in support))
    lines.extend(
        [
            "- Visible context: public task, interface, artifact, stimulus, and observable contract only.",
            "- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.",
            "",
            "## Form-Specific Requirements",
            "",
        ]
    )
    for item in form_instruction(form, targets):
        lines.append(f"- {item}")

    if modules:
        if form == "tb":
            heading = "## Public DUT Interface To Instantiate"
        elif form == "bugfix":
            heading = "## Public Interface To Preserve"
        else:
            heading = "## Public Verilog-A Interface"
        lines.extend(["", heading, ""])
        for filename, module, ports in modules:
            lines.append(f"- `{filename}` declares module `{module}` with positional ports: `" + "`, `".join(ports) + "`.")

    if trans or columns or nodes:
        lines.extend(["", "## Public Testbench And Observable Contract", ""])
        if trans:
            lines.append("Public transient setting used by the release harness:")
            lines.append("")
            lines.append("```spectre")
            lines.extend(trans)
            lines.append("```")
            lines.append("")
        if columns:
            lines.append("The release harness expects these exact public scalar observables:")
            lines.append("")
            for column in columns:
                lines.append(f"- `{column}`")
            lines.append("")
            lines.append("When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.")
        if nodes and form in {"tb", "e2e"}:
            if columns:
                lines.append("")
            lines.append("Public stimulus/source nodes visible in the reference harness include:")
            lines.append("")
            for node in nodes[:16]:
                lines.append(f"- `{node}`")

    if checks:
        lines.extend(["", "## Public Behavior Checks", ""])
        for check in checks:
            lines.append(f"- `{check}`")

    if form == "bugfix":
        lines.extend(
            [
                "",
                "## Observed Mismatch Framing",
                "",
                "The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.",
                "Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.",
            ]
        )

    lines.extend(
        [
            "",
            "## Output Contract",
            "",
        ]
    )
    if targets:
        if len(targets) == 1:
            lines.append(f"Return exactly one source artifact named `{targets[0]}`.")
        else:
            lines.append("Return exactly these source artifacts:")
            lines.append("")
            for target in targets:
                lines.append(f"- `{target}`")
            lines.append("")
    else:
        lines.append("Return exactly the requested source artifact(s).")
    lines.append("Do not include explanatory prose outside the source artifact contents.")
    lines.extend(["", "## Task-Specific Public Description", "", original, ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize vaBench release public prompts.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--entry-prefix",
        action="append",
        default=[],
        help="Only normalize entries whose release_entry_id starts with this prefix. May be repeated.",
    )
    args = parser.parse_args()

    changed: list[str] = []
    for form_dir in task_dirs():
        if args.entry_prefix:
            release_task = read_json(form_dir / "release_task.json")
            entry_id = str(release_task.get("release_entry_id", ""))
            if not any(entry_id.startswith(prefix) for prefix in args.entry_prefix):
                continue
        prompt_path = form_dir / "prompt.md"
        old = prompt_path.read_text(encoding="utf-8", errors="ignore")
        new = build_prompt(form_dir)
        if new != old:
            changed.append(rel(prompt_path))
            if not args.dry_run:
                prompt_path.write_text(new, encoding="utf-8")

    print(f"[release-prompt-sync] changed={len(changed)} dry_run={args.dry_run}")
    for path in changed[:20]:
        print(f"  - {path}")
    if len(changed) > 20:
        print(f"  ... {len(changed) - 20} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
