#!/usr/bin/env python3
"""Runner-side prompt wrapper for vaBench release model baselines.

The release `forms/*/prompt.md` files are public benchmark contracts.  This
module deliberately keeps model invocation mechanics outside those public
prompts: answer markers, extraction protocol, and shared EVAS/Spectre syntax
rules live here so baseline runs can change wrapper policy without changing the
benchmark definition.
"""
from __future__ import annotations

from pathlib import Path
import re


RELEASE_RUNNER_WRAPPER_VERSION = "release-runner-wrapper-v6"

RELEASE_SYSTEM_PROMPT = """\
You are an expert Verilog-A behavioral modeling engineer.
Write simulation-ready voltage-domain Verilog-A and Spectre transient artifacts.
Follow the public task contract exactly. Do not add hidden checker logic,
explanatory prose, private reasoning, or unrequested files.
"""

EVAS_SPECTRE_RULES = [
    "Use voltage-domain behavioral Verilog-A only: electrical ports, V(...) <+ contributions, analog begin/end, real/integer/genvar state, and event controls such as @(initial_step), @(cross(...)), @(timer(...)), and transition(...).",
    "Every generated .va file must start with the literal lines `` `include \"constants.vams\" `` and `` `include \"disciplines.vams\" `` before the module declaration so Spectre can compile electrical disciplines.",
    "Do not use digital Verilog constructs in .va files: no reg, wire, logic, always, initial, assign, posedge/negedge sensitivity lists, or module instantiations written in RTL style.",
    "Do not use current-domain or unsupported analog operators unless the public task explicitly asks for them: no I(...) <+, ddt(), idt(), laplace_*, transistor devices, AC/noise analysis, or topology-level KCL/KVL modeling.",
    "Declare Verilog-A real, integer, genvar, and parameter symbols at module scope before analog begin; do not declare local variables inside analog begin, if/else bodies, loops, or event bodies.",
    "Keep event controls such as @(cross(...)) as top-level statements directly inside analog begin. Put reset/enable/branch logic inside the event body instead of wrapping the event control in an if/else block.",
    "Do not use unbounded Verilog-A event loops such as while (1) or forever. Model repeated events with independent top-level event controls and state variables.",
    "Keep transition(...) contributions unconditional at the analog-block level: compute target state with events/logic first, then drive smoothed voltages with V(out) <+ transition(target, delay, trise, tfall).",
    "For analog vectors, use fixed bit indices or genvar-generated contributions. Do not index electrical vectors with a runtime integer inside analog behavior.",
    "Every generated Spectre testbench must start with simulator lang=spectre and global 0, include required Verilog-A files with literal ahdl_include \"<file>.va\" lines, and instantiate AHDL modules as XNAME (node1 node2 ...) module_name.",
    "Do not use module-first Spectre syntax, vpulse, vpwl, or bare source-terminal syntax. Use vsource with parenthesized terminals, for example Vclk (clk 0) vsource type=pulse ...",
    "For Spectre PWL sources, prefer a single-line wave=[ t0 v0 t1 v1 ... ] vector. If a PWL vector spans multiple lines, every non-final line inside wave=[...] must end with a backslash line continuation.",
    "PWL source times must be strictly increasing. To make a step, use a small positive delta such as 10n followed by 10.1n; do not repeat the same timestamp.",
    "A generated testbench is a transient stimulus/save harness, not a checker. Save the public scalar observables requested by the task and do not create hidden pass/fail assertions.",
    "Use only the requested target filenames. Do not depend on unlisted support files or invented includes.",
]


_FENCE_RE = re.compile(r"^\s*```[A-Za-z0-9_.+-]*\s*\n(.*?)\n?```\s*$", re.DOTALL)
_BEGIN_RE = re.compile(
    r"^\s*\[BEGIN file:\s*([^\]\n]+?)\s*\]\s*\n(.*?)(?=^\s*\[DONE file:\s*\1\s*\]\s*$)",
    re.DOTALL | re.MULTILINE,
)
_DONE_LINE_RE = re.compile(r"^\s*\[DONE file:[^\]\n]+?\]\s*$", re.MULTILINE)


def artifact_language(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix == ".scs":
        return "spectre"
    if suffix == ".va":
        return "verilog-a"
    return "text"


def clean_artifact_text(text: str) -> str:
    """Strip optional fences and runner markers from one artifact body."""
    body = text.strip()
    match = _FENCE_RE.match(body)
    if match:
        body = match.group(1).strip()
    body = _DONE_LINE_RE.sub("", body).strip()
    return body


def extract_marked_artifacts(response_text: str) -> dict[str, str]:
    """Extract `[BEGIN file: name] ... [DONE file: name]` artifacts.

    The public benchmark prompt does not contain these markers.  They are a
    runner-only protocol inspired by VerilogEval-style answer extraction.
    """
    artifacts: dict[str, str] = {}
    for match in _BEGIN_RE.finditer(response_text):
        raw_name = match.group(1).strip()
        filename = Path(raw_name).name
        if not filename.endswith((".va", ".scs")):
            continue
        if filename in artifacts:
            continue
        body = clean_artifact_text(match.group(2))
        if body:
            artifacts[filename] = body
    return artifacts


def build_file_protocol(target_artifacts: list[str]) -> str:
    if not target_artifacts:
        return (
            "Return only the requested .va/.scs artifact contents. Use one file block per artifact:\n"
            "[BEGIN file: <filename>]\n```<language>\n<source>\n```\n[DONE file: <filename>]"
        )

    lines = [
        "Return exactly the target artifacts below, using this file-marker protocol:",
        "",
    ]
    for filename in target_artifacts:
        language = artifact_language(filename)
        lines.extend(
            [
                f"[BEGIN file: {filename}]",
                f"```{language}",
                f"<contents of {filename}>",
                "```",
                f"[DONE file: {filename}]",
                "",
            ]
        )
    lines.extend(
        [
            "Do not include prose before, between, or after file blocks.",
            "Do not rename target files. Do not emit additional files.",
        ]
    )
    return "\n".join(lines).strip()


def build_support_artifact_context(support_artifacts: dict[str, str] | None) -> str:
    """Render public read-only support artifacts for model invocation.

    These are not answer blocks.  They intentionally use a different marker
    from `[BEGIN file: ...]` so response extraction cannot confuse supplied
    inputs with generated target artifacts.
    """
    if not support_artifacts:
        return ""
    lines = [
        "Public support artifact contents:",
        "",
        "The following files are supplied public inputs. Use them as read-only context.",
        "Do not return these files unless a filename is also listed as a target artifact.",
        "",
    ]
    for filename, contents in support_artifacts.items():
        language = artifact_language(filename)
        lines.extend(
            [
                f"[BEGIN support file: {filename}]",
                f"```{language}",
                contents.strip(),
                "```",
                f"[END support file: {filename}]",
                "",
            ]
        )
    return "\n".join(lines).strip()


def build_release_generation_prompt(
    *,
    public_prompt: str,
    target_artifacts: list[str],
    form: str | None = None,
    support_artifacts: dict[str, str] | None = None,
) -> str:
    """Wrap a public vaBench prompt for model generation."""
    form_line = f"\nForm: `{form}`\n" if form else "\n"
    rules = "\n".join(f"{idx}. {rule}" for idx, rule in enumerate(EVAS_SPECTRE_RULES, start=1))
    sections = [
        f"Wrapper version: `{RELEASE_RUNNER_WRAPPER_VERSION}`",
        "Question:",
        public_prompt.strip(),
    ]
    support_context = build_support_artifact_context(support_artifacts)
    if support_context:
        sections.append(support_context)
    sections.extend(
        [
            "Runner-visible context:" + form_line + "These are public language, artifact, and simulator compatibility rules; they are not hidden checker criteria.",
            "EVAS/Spectre compatibility rules:",
            rules,
            "Answer:",
            build_file_protocol(target_artifacts),
        ]
    )
    return "\n\n".join(sections).strip() + "\n"
