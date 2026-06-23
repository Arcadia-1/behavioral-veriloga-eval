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
PACKAGE_MANIFEST = RELEASE_ROOT / "MANIFEST.json"

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
SOURCE_LINE_RE = re.compile(r"^\s*[VI]\w*\s+\(([^)\s]+)\s+0\)\s+\w+source\b.*$", re.IGNORECASE)

PUBLIC_BEHAVIOR_TARGETS: dict[str, tuple[str, ...]] = {
    "vbr1_l1_bandgap_reference_macro_model": (
        "Treat logic low/high as 0 V/0.9 V with a 0.45 V threshold.",
        "Treat vin as a sub-1 V supply ramp. Start regulation above about 0.65 V and reset below about 0.50 V.",
        "During reset or below-threshold supply, hold out near 0 V and keep metric low.",
        "After startup, regulate out near a supply-insensitive reference around 0.55 V.",
        "During higher supply, keep the reference nearly constant instead of supply-tracking.",
        "During brownout, reset out near 0 V and mark the output invalid.",
    ),
    "vbr1_l1_bias_voltage_generator_with_enable_trim": (
        "Treat logic low/high as 0 V/0.9 V with a 0.45 V threshold.",
        "Treat vin as the combined enable/trim control. vin below about 0.25 V disables the bias: out near 0 V and metric low.",
        "When enabled, map vin from about 0.25-0.90 V to a bounded bias target around 0.28-0.82 V.",
        "out should move smoothly toward the trim target on clocked updates, not jump to rails.",
        "Higher trim/control voltage should increase out monotonically.",
        "metric should be high only while the bias generator is enabled and driving a valid bias.",
    ),
    "vbr1_l1_ptat_ctat_reference_generator": (
        "Treat vin as a voltage-coded temperature/control value in the 0-0.9 V range.",
        "Build opposing PTAT and CTAT internal trends; metric should expose a PTAT-like increasing branch.",
        "Combine PTAT and CTAT so out stays near a bounded reference around mid-scale instead of strongly tracking vin.",
        "Reset should initialize out near mid-scale and keep metric low until valid updates occur.",
        "Clamp out and metric to the public 0-0.9 V voltage-domain range.",
    ),
    "vbr1_l1_power_on_reset_detector": (
        "Treat vin as a supply ramp. Keep out reset-asserted high while reset input is high or vin is below about 0.62 V.",
        "After vin is power-good and reset is released, wait about four rising clock updates before deasserting out low.",
        "During the release delay, metric may indicate partial release; after release, metric should be high.",
        "If supply falls below threshold or reset asserts again, immediately assert out high and clear the release delay.",
    ),
    "vbr1_l1_uvlo_brownout_detector": (
        "Treat vin as the supply. Assert power-good out high only after vin rises above about 0.65 V.",
        "Keep out high while vin remains between about 0.55 V and 0.65 V; this is the UVLO hysteresis band.",
        "Clear out low on brownout below about 0.55 V or reset.",
        "metric should distinguish fault/lockout from the valid power-good state.",
    ),
    "vbr1_l1_ldo_regulator_macro_model": (
        "Treat vin as a voltage-coded load/disturbance control, not as the regulator supply rail.",
        "Regulated out should remain bounded near about 0.60 V under light load.",
        "Higher load/disturbance should cause visible droop from the nominal target, not rail-to-rail tracking.",
        "After a load reduction, out should recover gradually toward the regulation target over clocked updates.",
        "metric should be high when regulation error is small and lower during droop/recovery.",
        "Keep all outputs in the 0-0.9 V voltage-domain range.",
    ),
    "vbr1_l1_lna_gain_compression_macro": (
        "Treat vin around 0.45 V common mode; small-signal out should show gain greater than 1 around that common mode.",
        "For large drive, compress incremental gain and keep output bounded.",
        "Compression should be reasonably symmetric for positive and negative excursions.",
        "metric should be low or small in the linear region and high during compression.",
    ),
    "vbr1_l1_rf_mixer_downconverter_macro": (
        "Treat clk as the LO-polarity waveform with a 0.45 V logic threshold.",
        "Convert the input envelope around 0.45 V common mode to baseband by flipping sign with LO polarity.",
        "Preserve output common mode near 0.45 V and keep out bounded.",
        "metric should indicate active conversion or LO polarity state.",
    ),
    "vbr1_l1_pa_compression_macro": (
        "Treat vin as PA drive around 0.45 V common mode.",
        "Moderate drive should show gain above unity.",
        "Large drive should compress toward bounded high/low output limits rather than continuing linear gain.",
        "metric should rise when the output is near compression or limiting.",
        "Keep out and metric within the 0-0.9 V voltage-domain range.",
    ),
    "vbr1_l1_log_rssi_power_detector": (
        "Treat vin as an envelope around 0.45 V common mode and estimate amplitude as abs(vin - 0.45).",
        "Use a Spectre/EVAS-friendly compressed or piecewise approximation; do not rely on unsupported log10, round, integer casts, or digital Verilog.",
        "out should be monotonic with amplitude, but large-amplitude steps should be compressed rather than linear.",
        "Keep a low-input floor near the bottom of the RSSI range.",
        "metric should expose normalized envelope magnitude and remain bounded within 0-0.9 V.",
    ),
    "vbr1_l1_limiting_amplifier_frontend": (
        "Treat vin around 0.45 V common mode and preserve signal polarity around that common mode.",
        "For small input excursions, apply gain around common mode.",
        "For large positive or negative excursions, limit/compress output toward bounded high/low levels instead of continuing linearly.",
        "Assert metric high only when limiting/compression is active.",
        "Keep out in the 0-0.9 V range and avoid hard digital switching for small signals.",
    ),
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def task_dirs() -> list[Path]:
    if PACKAGE_MANIFEST.exists():
        manifest = read_json(PACKAGE_MANIFEST)
        rows = manifest.get("forms", [])
        form_dirs: list[Path] = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            value = row.get("release_task_manifest")
            if not isinstance(value, str) or not value:
                continue
            path = ROOT / value
            if path.exists():
                form_dirs.append(path.parent)
        if form_dirs:
            return sorted(form_dirs)
    return sorted(path.parent for path in TASKS_ROOT.glob("*/vbr1_*/forms/*/release_task.json"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def artifact_paths(release_task: dict) -> list[Path]:
    return [ROOT / str(item) for item in release_task.get("artifacts", {}).get("gold", [])]


def target_artifacts(form: str, gold_paths: list[Path], explicit: list[str] | None = None) -> list[str]:
    if explicit:
        return [str(item) for item in explicit]
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


def module_signatures(va_paths: list[Path]) -> list[tuple[str, str, list[str]]]:
    rows: list[tuple[str, str, list[str]]] = []
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
        logical_lines: list[str] = []
        pending = ""
        for raw_line in text.splitlines():
            line = raw_line.rstrip()
            if line.endswith("\\"):
                pending += line[:-1] + " "
                continue
            logical_lines.append(pending + line)
            pending = ""
        if pending:
            logical_lines.append(pending)

        for line in logical_lines:
            match = SAVE_RE.match(line)
            if not match:
                continue
            body = match.group(1).strip()
            if body.lower().startswith(("all", "none")):
                continue
            for token in re.split(r"\s+", body):
                token = token.strip().strip(",")
                if not token or token == "\\":
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


def supply_source_lines(scs_paths: list[Path]) -> list[str]:
    """Expose fixed public supply sources without copying full stimulus waveforms."""
    lines: list[str] = []
    seen: set[str] = set()
    for path in sorted(scs_paths):
        for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = re.sub(r"\s+", " ", raw_line.strip())
            match = SOURCE_LINE_RE.match(line)
            if not match:
                continue
            node = match.group(1).strip()
            node_l = node.lower()
            if node_l not in {"vdd", "vss"}:
                continue
            if "type=pwl" in line.lower() or "type=pulse" in line.lower() or "type=sine" in line.lower():
                continue
            if line not in seen:
                seen.add(line)
                lines.append(line)
    return lines[:4]


def logical_spectre_lines(text: str) -> list[str]:
    lines: list[str] = []
    pending = ""
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        if stripped.endswith("\\"):
            pending += stripped[:-1] + " "
            continue
        lines.append(re.sub(r"\s+", " ", pending + stripped).strip())
        pending = ""
    if pending:
        lines.append(re.sub(r"\s+", " ", pending).strip())
    return lines


def public_instance_lines(scs_paths: list[Path], modules: list[tuple[str, str, list[str]]]) -> list[str]:
    module_names = {module for _, module, _ in modules}
    if not module_names:
        return []
    lines: list[str] = []
    seen: set[str] = set()
    for path in sorted(scs_paths):
        for line in logical_spectre_lines(path.read_text(encoding="utf-8", errors="ignore")):
            if not re.match(r"^[A-Za-z]\w*\s+\(", line):
                continue
            if re.match(r"^[VI]\w*\s+\([^)]*\)\s+\w+source\b", line, flags=re.IGNORECASE):
                continue
            for module in module_names:
                if re.search(rf"\)\s+{re.escape(module)}(?:\s|$)", line):
                    if line not in seen:
                        seen.add(line)
                        lines.append(line)
                    break
    return lines


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


def public_behavior_targets(entry_id: str) -> list[str]:
    return list(PUBLIC_BEHAVIOR_TARGETS.get(entry_id, ()))


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


def va_files_for_generated_testbench(form: str, support: list[str], targets: list[str]) -> list[str]:
    files: list[str] = []
    if form == "tb":
        files.extend(name for name in support if name.endswith(".va"))
    elif form == "e2e":
        files.extend(name for name in targets if name.endswith(".va"))
        files.extend(name for name in support if name.endswith(".va"))
    seen: set[str] = set()
    ordered: list[str] = []
    for name in files:
        if name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def include_contract_lines(form: str, support: list[str], targets: list[str]) -> list[str]:
    va_support = [name for name in support if name.endswith(".va")]
    va_targets = [name for name in targets if name.endswith(".va")]
    lines: list[str] = []
    if va_support:
        joined = ", ".join(f"`{name}`" for name in va_support)
        lines.append(
            f"The supplied DUT/support Verilog-A file(s) {joined} will be co-located with the generated testbench by the evaluation harness."
        )
        if len(va_support) == 1:
            lines.append(f'Include it exactly with `ahdl_include "{va_support[0]}"` in the generated Spectre `.scs` netlist.')
        else:
            lines.append('Include each supplied Verilog-A support file exactly with a matching `ahdl_include "<file>.va"` line in the generated Spectre `.scs` netlist.')
    elif va_targets and any(name.endswith(".scs") for name in targets):
        joined = ", ".join(f"`{name}`" for name in va_targets)
        lines.append(
            f"The generated Verilog-A file(s) {joined} must be co-located with the generated Spectre testbench."
        )
        if len(va_targets) == 1:
            lines.append(f'Include the generated DUT exactly with `ahdl_include "{va_targets[0]}"` in the generated testbench.')
        else:
            lines.append('Include each generated Verilog-A file exactly with a matching `ahdl_include "<file>.va"` line in the generated testbench.')
    if form in {"tb", "e2e"}:
        lines.append("Use Spectre AHDL instance syntax with the instance name first and module name last: `XNAME (node1 node2 ...) module_name`.")
        lines.append("Never write module-first syntax such as `module_name instance_name (...)`; that is not the release Spectre testbench syntax.")
    return lines


def form_instruction(form: str, targets: list[str], support: list[str]) -> list[str]:
    if form == "dut":
        return [
            "Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.",
            "Preserve the public module names, port order, parameters, and waveform observable names.",
        ]
    if form == "tb":
        return [
            "Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.",
            "Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.",
        ] + include_contract_lines(form, support, targets)
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
        ] + include_contract_lines(form, support, targets)
    return ["Preserve the public artifact and evaluator-facing contract."]


def spectre_harness_scaffold(
    form: str,
    support: list[str],
    targets: list[str],
    modules: list[tuple[str, str, list[str]]],
    trans: list[str],
    columns: list[str],
    supply_lines: list[str],
    instance_lines: list[str],
) -> list[str]:
    if form not in {"tb", "e2e"}:
        return []
    include_files = va_files_for_generated_testbench(form, support, targets)
    if not include_files and not modules:
        return []

    example_lines: list[str] = [
        "simulator lang=spectre",
        "global 0",
    ]
    example_lines.extend(f'ahdl_include "{name}"' for name in include_files)
    if supply_lines:
        example_lines.append("")
        example_lines.extend(supply_lines)
    if instance_lines:
        example_lines.append("")
        example_lines.extend(instance_lines)
    elif modules:
        example_lines.append("")
        for _, module, ports in modules:
            joined_ports = " ".join(ports)
            example_lines.append(f"X{module} ({joined_ports}) {module}")
    if trans:
        example_lines.append("")
        example_lines.append(trans[0])
    if columns:
        example_lines.append("save " + " ".join(columns))

    return [
        "",
        "## Public Spectre Testbench Scaffold",
        "",
        "When this form generates a `.scs` testbench, use the following public skeleton shape. "
        "Fill in only the public stimulus details required by the task; do not copy or emit hidden checker logic.",
        "",
        "```spectre",
        *example_lines,
        "```",
        "",
        "Critical syntax rules:",
        "",
        "- Every Verilog-A DUT/support file used by the testbench must have a literal `ahdl_include \"<file>.va\"` line in the `.scs` artifact.",
        "- Spectre AHDL instances use instance-first/module-last syntax: `XNAME (node1 node2 ...) module_name`.",
        "- Do not use module-first syntax such as `module_name instance_name (...)`.",
        "- Keep saved names as plain scalar public observables, not instance-qualified aliases.",
    ]


def l2_background_lines(release_task: dict) -> list[str]:
    if release_task.get("level") != "L2":
        return []

    base_function = str(release_task.get("base_function", "the listed function"))
    track = str(release_task.get("track", "core"))
    if track == "support":
        role_line = (
            f"This Level-2 row is a reusable measurement/stimulus support flow for {base_function}. "
            "It is certified as release content but remains outside the core circuit score denominator."
        )
        claim_line = (
            "Paper-facing claims for this row are limited to support-flow behavior and must be "
            "reported separately from core analog/mixed-signal circuit-function coverage."
        )
    else:
        role_line = (
            f"This Level-2 row is a behavioral composition/flow task for {base_function}. "
            "It should expose intermediate state, multi-stage behavior, or a closed-loop relation "
            "through the public observables below."
        )
        claim_line = (
            "Paper-facing claims for this row are limited to the public behavior checks below; "
            "do not broaden the task into full silicon implementation, layout, device physics, "
            "or unlisted performance metrics."
        )

    return [
        "",
        "## L2 Background And Claim Boundary",
        "",
        role_line,
        "Stay within the listed voltage-domain/event-driven contract. Do not use transistor-level devices, "
        "current-domain loads, AC/noise analysis, S-parameters, or hidden checker logic unless the public "
        "contract explicitly lists them.",
        claim_line,
    ]


def build_prompt(form_dir: Path) -> str:
    release_task = read_json(form_dir / "release_task.json")
    prompt_path = form_dir / "prompt.md"
    original = clean_original(prompt_path.read_text(encoding="utf-8", errors="ignore"))
    form = form_dir.name
    gold_paths = artifact_paths(release_task)
    explicit = release_task.get("artifacts", {}).get("submission_artifacts")
    targets = target_artifacts(form, gold_paths, explicit if isinstance(explicit, list) else None)
    support = support_artifacts(form, gold_paths, targets)
    va_paths = [path for path in gold_paths if path.name.endswith(".va")]
    scs_paths = [path for path in gold_paths if path.name.endswith(".scs")]
    modules = module_signatures(va_paths)
    columns = save_columns(scs_paths)
    trans = tran_lines(scs_paths)
    nodes = source_nodes(scs_paths)
    supplies = supply_source_lines(scs_paths)
    instances = public_instance_lines(scs_paths, modules)
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
        ]
    )
    lines.extend(l2_background_lines(release_task))
    lines.extend(["", "## Form-Specific Requirements", ""])
    for item in form_instruction(form, targets, support):
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

    lines.extend(spectre_harness_scaffold(form, support, targets, modules, trans, columns, supplies, instances))

    if checks:
        lines.extend(["", "## Public Behavior Checks", ""])
        for check in checks:
            lines.append(f"- `{check}`")
    target_lines = public_behavior_targets(str(release_task.get("release_entry_id", "")))
    if target_lines:
        lines.extend(["", "## Public Behavioral Targets", ""])
        for target in target_lines:
            lines.append(f"- {target}")

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
