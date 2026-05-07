#!/usr/bin/env python3
"""Materialize the draft bpack-v1 benchmark from the pack inventory.

The inventory is intentionally conservative: some packs are exact four-form
packs, while others still need contract review or authoring.  This script turns
the existing task references into a runnable benchmark root without pretending
that draft packs are already frozen.
"""
from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INVENTORY = ROOT / "docs" / "BPACK_V1_INVENTORY.json"
DEFAULT_SOURCE_BENCH = ROOT / "benchmark-balanced"
DEFAULT_OUTPUT_BENCH = ROOT / "benchmark-bpack-v1"

FORM_SUFFIX = {
    "bugfix": "bugfix",
    "spec-to-va": "dut",
    "end-to-end": "e2e",
    "tb-generation": "tb",
}

SOURCE_FORM_NORMALIZATION = {
    "dut-only/spec-to-va": "spec-to-va",
    "spec-to-va": "spec-to-va",
    "bugfix": "bugfix",
    "end-to-end": "end-to-end",
    "tb-generation": "tb-generation",
}

AUTHORED_OVERRIDES: dict[tuple[str, str], dict[str, str]] = {
    ("sample_hold", "spec-to-va"): {
        "source_task_id": "original92_sample_hold_smoke",
        "source_behavior_task_id": "sample_hold_smoke",
        "kind": "spec",
    },
    ("pfd_updn", "spec-to-va"): {
        "source_task_id": "original92_pfd_updn_smoke",
        "source_behavior_task_id": "pfd_updn_smoke",
        "kind": "spec",
    },
    ("pfd_updn", "tb-generation"): {
        "source_task_id": "original92_pfd_updn_smoke",
        "source_behavior_task_id": "pfd_updn_smoke",
        "kind": "tb",
    },
    ("binary_dac_4b", "bugfix"): {
        "source_task_id": "original92_dac_binary_clk_4b_smoke",
        "source_behavior_task_id": "dac_binary_clk_4b_smoke",
        "kind": "bugfix",
    },
    ("binary_dac_4b", "spec-to-va"): {
        "source_task_id": "original92_dac_binary_clk_4b_smoke",
        "source_behavior_task_id": "dac_binary_clk_4b_smoke",
        "kind": "spec",
    },
    ("clock_divider", "bugfix"): {
        "source_task_id": "original92_clk_div_smoke",
        "source_behavior_task_id": "clk_div_smoke",
        "kind": "bugfix",
    },
    ("clock_divider", "spec-to-va"): {
        "source_task_id": "original92_clk_div_smoke",
        "source_behavior_task_id": "clk_div_smoke",
        "kind": "spec",
    },
    ("clock_divider", "tb-generation"): {
        "source_task_id": "original92_clk_div_smoke",
        "source_behavior_task_id": "clk_div_smoke",
        "kind": "tb",
    },
    ("hysteresis_comparator", "bugfix"): {
        "source_task_id": "original92_comparator_hysteresis_smoke",
        "source_behavior_task_id": "comparator_hysteresis_smoke",
        "kind": "bugfix",
    },
    ("hysteresis_comparator", "spec-to-va"): {
        "source_task_id": "original92_comparator_hysteresis_smoke",
        "source_behavior_task_id": "comparator_hysteresis_smoke",
        "kind": "spec",
    },
    ("hysteresis_comparator", "tb-generation"): {
        "source_task_id": "original92_comparator_hysteresis_smoke",
        "source_behavior_task_id": "comparator_hysteresis_smoke",
        "kind": "tb",
    },
    ("flash_adc_3b", "bugfix"): {
        "source_task_id": "original92_flash_adc_3b_smoke",
        "source_behavior_task_id": "flash_adc_3b_smoke",
        "kind": "bugfix",
    },
    ("flash_adc_3b", "spec-to-va"): {
        "source_task_id": "original92_flash_adc_3b_smoke",
        "source_behavior_task_id": "flash_adc_3b_smoke",
        "kind": "spec",
    },
    ("flash_adc_3b", "tb-generation"): {
        "source_task_id": "original92_flash_adc_3b_smoke",
        "source_behavior_task_id": "flash_adc_3b_smoke",
        "kind": "tb",
    },
    ("dwa_pointer", "bugfix"): {
        "source_task_id": "original92_dwa_ptr_gen_smoke",
        "source_behavior_task_id": "dwa_ptr_gen_smoke",
        "kind": "bugfix",
    },
    ("dwa_pointer", "spec-to-va"): {
        "source_task_id": "original92_dwa_ptr_gen_smoke",
        "source_behavior_task_id": "dwa_ptr_gen_smoke",
        "kind": "spec",
    },
    ("dwa_pointer", "tb-generation"): {
        "source_task_id": "original92_dwa_ptr_gen_smoke",
        "source_behavior_task_id": "dwa_ptr_gen_smoke",
        "kind": "tb",
    },
    ("prbs7_lfsr", "bugfix"): {
        "source_task_id": "original92_prbs7",
        "source_behavior_task_id": "prbs7",
        "kind": "bugfix",
    },
    ("prbs7_lfsr", "end-to-end"): {
        "source_task_id": "original92_prbs7",
        "source_behavior_task_id": "prbs7",
        "kind": "e2e",
    },
    ("prbs7_lfsr", "tb-generation"): {
        "source_task_id": "original92_prbs7",
        "source_behavior_task_id": "prbs7",
        "kind": "tb",
    },
}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _copytree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def _task_id_for(pack_id: str, form: str) -> str:
    return f"bpack_{pack_id}_{FORM_SUFFIX[form]}"


def _promotion_status(pack_status: str, missing_forms: list[str]) -> str:
    if missing_forms:
        return "bpack_v1_draft_missing_forms"
    if pack_status == "existing_exact_pack":
        return "bpack_v1_candidate_needs_gold_validation"
    if pack_status == "existing_needs_contract_review":
        return "bpack_v1_draft_needs_contract_review_and_gold_validation"
    return "bpack_v1_draft_needs_authoring_or_contract_split"


def _first_tb_text(task_dir: Path) -> str:
    tbs = sorted((task_dir / "gold").glob("*.scs"))
    return tbs[0].read_text(encoding="utf-8", errors="ignore") if tbs else ""


def _gold_includes(task_dir: Path) -> list[str]:
    import re

    return [Path(item).name for item in re.findall(r'ahdl_include\s+"([^"]+\.va)"', _first_tb_text(task_dir))]


def _gold_module_names(task_dir: Path) -> list[str]:
    import re

    modules: list[str] = []
    for va_path in sorted((task_dir / "gold").glob("*.va")):
        text = va_path.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"\bmodule\s+(\w+)\s*\(", text)
        if match:
            modules.append(match.group(1))
    return modules


def _gold_save_line(task_dir: Path) -> str:
    for line in _first_tb_text(task_dir).splitlines():
        if line.strip().lower().startswith("save "):
            return line.strip()
    return "save <public observables>"


def _gold_tran_line(task_dir: Path) -> str:
    for line in _first_tb_text(task_dir).splitlines():
        if line.strip().lower().startswith("tran "):
            return line.strip()
    return "tran tran stop=<public-window>"


def _authored_prompt(pack_id: str, form: str, source_task_dir: Path, source_meta: dict[str, Any]) -> str:
    modules = _gold_module_names(source_task_dir)
    includes = _gold_includes(source_task_dir)
    module_text = ", ".join(f"`{m}`" for m in modules) or "`<module>`"
    include_text = ", ".join(f"`{name}`" for name in includes) or "the referenced DUT file"
    save_line = _gold_save_line(source_task_dir)
    tran_line = _gold_tran_line(source_task_dir)
    source_prompt = (source_task_dir / "prompt.md").read_text(encoding="utf-8", errors="ignore")
    public_contract = (
        "## Public Evaluation Contract (Non-Gold)\n\n"
        f"Final EVAS transient setting:\n\n```spectre\n{tran_line}\n```\n\n"
        f"Required public save statement:\n\n```spectre\n{save_line}\n```\n\n"
        "Use plain scalar save names for public observables; do not rely on instance-qualified or aliased save names.\n"
    )

    if form == "spec-to-va":
        return (
            f"Create only the DUT Verilog-A model for the `{pack_id}` circuit function.\n"
            "Do not generate a testbench; the evaluator will use a fixed public harness.\n\n"
            f"Required module(s): {module_text}.\n"
            f"The verifier harness includes: {include_text}.\n\n"
            "Preserve the public port names and behavior described below.  Use pure voltage-domain Verilog-A, "
            "`electrical` ports, event handling through `@(cross(...))` where needed, and `transition(...)` on driven outputs.\n\n"
            "## Source Functional Specification\n\n"
            f"{source_prompt}\n\n"
            f"{public_contract}"
            "Return exactly one complete Verilog-A code block unless the source specification explicitly requires multiple modules.\n"
        )
    if form == "tb-generation":
        return (
            f"Generate only the Spectre testbench for the `{pack_id}` circuit function.\n"
            "Do not generate Verilog-A modules.  The evaluator provides the DUT Verilog-A file(s).\n\n"
            f"Required DUT include(s): {include_text}.\n"
            f"Required module(s): {module_text}.\n\n"
            "The testbench must instantiate the provided DUT, drive the public inputs through the validation behavior, "
            "run exactly one transient analysis, and save the public observables.\n\n"
            "## Source Functional Specification\n\n"
            f"{source_prompt}\n\n"
            f"{public_contract}"
            "Return exactly one fenced `spectre` code block and no prose outside the code block.\n"
        )
    if form == "bugfix":
        return (
            f"Fix a buggy Verilog-A implementation of the `{pack_id}` circuit function without changing its public behavior.\n"
            f"The corrected implementation must provide module(s): {module_text}.\n"
            f"The verifier harness includes: {include_text}.\n\n"
            "Typical bug class for this task form: wrong edge/update condition, swapped state transition, missing clamp, "
            "or stale output state.  Produce the corrected Verilog-A artifact requested by the harness.\n\n"
            "## Intended Functional Specification\n\n"
            f"{source_prompt}\n\n"
            f"{public_contract}"
            "Return exactly one complete Verilog-A code block unless the source specification explicitly requires multiple modules.\n"
        )
    return (
        f"Create the full end-to-end Verilog-A DUT and Spectre testbench for `{pack_id}`.\n\n"
        f"Required module(s): {module_text}.\n\n"
        "## Source Functional Specification\n\n"
        f"{source_prompt}\n\n"
        f"{public_contract}"
        "Return one or more fenced `verilog-a` blocks plus one fenced `spectre` testbench block.\n"
    )


def _load_source_task(source_bench: Path, source_task_id: str) -> tuple[Path, dict[str, Any]]:
    task_dir = source_bench / "tasks" / source_task_id
    meta_path = task_dir / "meta.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"source task missing meta.json: {source_task_id}")
    return task_dir, _read_json(meta_path)


def materialize(inventory_path: Path, source_bench: Path, output_bench: Path) -> dict[str, Any]:
    inventory = _read_json(inventory_path)
    task_forms = list(inventory.get("task_forms", FORM_SUFFIX))

    if output_bench.exists():
        shutil.rmtree(output_bench)
    (output_bench / "tasks").mkdir(parents=True)
    shutil.copy2(source_bench / "common_checker.py", output_bench / "common_checker.py")

    manifest_tasks: list[dict[str, Any]] = []
    manifest_packs: list[dict[str, Any]] = []
    missing_source_tasks: list[dict[str, str]] = []
    form_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()

    for pack in inventory["packs"]:
        pack_id = pack["circuit_function_id"]
        pack_status = pack["status"]
        forms = pack.get("forms", {})
        missing_forms = [form for form in task_forms if not forms.get(form) and (pack_id, form) not in AUTHORED_OVERRIDES]
        promotion_status = _promotion_status(pack_status, missing_forms)
        pack_tasks: dict[str, str | None] = {}

        for form in task_forms:
            authored = AUTHORED_OVERRIDES.get((pack_id, form))
            source_task_id = authored["source_task_id"] if authored else forms.get(form)
            if not source_task_id:
                pack_tasks[form] = None
                continue
            try:
                src_dir, source_meta = _load_source_task(source_bench, source_task_id)
            except FileNotFoundError:
                missing_source_tasks.append({"pack_id": pack_id, "form": form, "source_task_id": source_task_id})
                pack_tasks[form] = None
                continue

            task_id = _task_id_for(pack_id, form)
            dst_dir = output_bench / "tasks" / task_id
            _copytree(src_dir, dst_dir)
            if authored:
                (dst_dir / "prompt.md").write_text(
                    _authored_prompt(pack_id, form, src_dir, source_meta),
                    encoding="utf-8",
                )

            source_task_form = SOURCE_FORM_NORMALIZATION.get(str(source_meta.get("task_form") or source_meta.get("family") or ""))
            source_family = str(source_meta.get("family") or form)
            behavior_source_task_id = (
                authored["source_behavior_task_id"]
                if authored
                else str(source_meta.get("source_task_id") or source_meta.get("id") or source_task_id)
            )
            task_promotion_status = (
                "bpack_v1_authored_candidate_needs_gold_validation"
                if authored
                else promotion_status
            )
            meta = dict(source_meta)
            meta.update(
                {
                    "task_id": task_id,
                    "family": "spec-to-va" if form == "spec-to-va" else form,
                    "benchmark": "bpack-v1",
                    "benchmark_split": "benchmark-bpack-v1",
                    "source_benchmark": "benchmark-balanced",
                    "bpack_source_task_id": source_task_id,
                    "source_task_id": behavior_source_task_id,
                    "source_task_form": source_task_form,
                    "source_family": source_family,
                    "circuit_function_id": pack_id,
                    "core_function": pack["core_function"],
                    "task_form": form,
                    "pack_id": pack_id,
                    "pack_version": "v1",
                    "bpack_inventory_status": pack_status,
                    "bpack_authored": bool(authored),
                    "bpack_authored_kind": authored["kind"] if authored else None,
                    "bpack_notes": pack.get("notes", ""),
                    "promotion_status": task_promotion_status,
                }
            )
            _write_json(dst_dir / "meta.json", meta)

            has_gold = (dst_dir / "gold").is_dir()
            has_checker = (dst_dir / "checker.py").exists()
            entry = {
                "task_id": task_id,
                "pack_id": pack_id,
                "circuit_function_id": pack_id,
                "core_function": pack["core_function"],
                "task_form": form,
                "family": meta["family"],
                "bpack_source_task_id": source_task_id,
                "source_task_id": behavior_source_task_id,
                "source_task_form": source_task_form,
                "source_family": source_family,
                "bpack_inventory_status": pack_status,
                "bpack_authored": bool(authored),
                "bpack_authored_kind": authored["kind"] if authored else None,
                "promotion_status": task_promotion_status,
                "gold_required": has_gold,
                "checker_required": has_checker,
            }
            manifest_tasks.append(entry)
            pack_tasks[form] = task_id
            form_counts[form] += 1
            status_counts[pack_status] += 1

        manifest_packs.append(
            {
                "pack_id": pack_id,
                "circuit_function_id": pack_id,
                "core_function": pack["core_function"],
                "inventory_status": pack_status,
                "promotion_status": promotion_status,
                "missing_forms": missing_forms,
                "tasks": pack_tasks,
                "authored_forms": sorted(form for form in task_forms if (pack_id, form) in AUTHORED_OVERRIDES),
                "notes": pack.get("notes", ""),
            }
        )

    manifest: dict[str, Any] = {
        "benchmark": "bpack-v1",
        "target_size": inventory.get("target_size", "bpack48"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "inventory": str(inventory_path.resolve()),
        "source_benchmark": str(source_bench.resolve()),
        "output_benchmark": str(output_bench.resolve()),
        "task_forms": task_forms,
        "pack_count": len(manifest_packs),
        "materialized_task_count": len(manifest_tasks),
        "complete_pack_count": sum(1 for pack in manifest_packs if not pack["missing_forms"]),
        "exact_pack_count": sum(1 for pack in manifest_packs if pack["inventory_status"] == "existing_exact_pack"),
        "authored_task_count": sum(1 for task in manifest_tasks if task.get("bpack_authored")),
        "form_counts": dict(form_counts),
        "inventory_status_counts_by_task": dict(status_counts),
        "missing_source_tasks": missing_source_tasks,
        "packs": manifest_packs,
        "tasks": manifest_tasks,
    }
    _write_json(output_bench / "manifest.json", manifest)
    _write_readme(output_bench, manifest)
    return manifest


def _write_readme(output_bench: Path, manifest: dict[str, Any]) -> None:
    lines = [
        "# bpack-v1 Benchmark Draft",
        "",
        "This benchmark root is materialized from `docs/BPACK_V1_INVENTORY.json`.",
        "Its unit of balance is a concrete `circuit_function_id` pack with four task forms:",
        "`bugfix`, `spec-to-va`, `end-to-end`, and `tb-generation`.",
        "",
        "## Current Status",
        "",
        f"- Packs in inventory: {manifest['pack_count']}",
        f"- Materialized tasks: {manifest['materialized_task_count']}",
        f"- Authored bpack tasks: {manifest['authored_task_count']}",
        f"- Complete packs by referenced forms: {manifest['complete_pack_count']}",
        f"- Exact seed packs: {manifest['exact_pack_count']}",
        "",
        "This is a draft benchmark root.  Tasks whose `promotion_status` contains",
        "`draft` or `needs_contract_review` must not be treated as frozen bpack-v1",
        "tasks until gold validation and contract review pass.",
        "",
        "## Form Counts",
        "",
        "| form | tasks |",
        "| --- | ---: |",
    ]
    for form, count in manifest["form_counts"].items():
        lines.append(f"| `{form}` | {count} |")
    lines.extend(["", "## Packs", "", "| pack | status | missing forms |", "| --- | --- | --- |"])
    for pack in manifest["packs"]:
        missing = ", ".join(pack["missing_forms"]) if pack["missing_forms"] else "-"
        authored = ", ".join(pack.get("authored_forms", [])) if pack.get("authored_forms") else "-"
        lines.append(f"| `{pack['pack_id']}` | `{pack['inventory_status']}` | {missing}; authored={authored} |")
    output_bench.joinpath("README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--source-bench", type=Path, default=DEFAULT_SOURCE_BENCH)
    parser.add_argument("--output-bench", type=Path, default=DEFAULT_OUTPUT_BENCH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = materialize(args.inventory, args.source_bench, args.output_bench)
    print(
        json.dumps(
            {
                "output_benchmark": str(args.output_bench),
                "packs": manifest["pack_count"],
                "materialized_tasks": manifest["materialized_task_count"],
                "complete_packs": manifest["complete_pack_count"],
                "form_counts": manifest["form_counts"],
                "missing_source_tasks": manifest["missing_source_tasks"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
