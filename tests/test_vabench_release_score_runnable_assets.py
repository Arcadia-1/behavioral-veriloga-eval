from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCORE_DENOMINATOR = ROOT / "benchmark-vabench-release-v1" / "reports" / "score_denominator_manifest.json"


def counted_form_rows() -> list[dict]:
    report = json.loads(SCORE_DENOMINATOR.read_text(encoding="utf-8"))
    return [row for row in report["form_rows"] if row["counted_in_score"]]


def gold_files(row: dict) -> list[Path]:
    manifest = ROOT / row["manifest"]
    return sorted((manifest.parent / "gold").glob("*"))


def test_counted_forms_have_score_runnable_counterpart_assets() -> None:
    missing: list[str] = []
    for row in counted_form_rows():
        files = gold_files(row)
        has_va = any(path.suffix == ".va" for path in files)
        has_scs = any(path.suffix == ".scs" for path in files)
        form = row["form"]
        if form in {"dut", "bugfix"} and not has_scs:
            missing.append(f"{row['task_id']}: missing reference testbench")
        if form == "tb" and not has_va:
            missing.append(f"{row['task_id']}: missing reference DUT")
        if form == "e2e" and (not has_va or not has_scs):
            missing.append(f"{row['task_id']}: missing complete e2e reference")

    assert missing == []


def test_counted_tb_prompts_state_supplied_dut_include_contract() -> None:
    missing: list[str] = []
    for row in counted_form_rows():
        if row["form"] != "tb":
            continue
        prompt = (ROOT / row["manifest"]).parent / "prompt.md"
        text = prompt.read_text(encoding="utf-8")
        if "Supplied/reference support artifact(s):" not in text:
            missing.append(f"{row['task_id']}: no supplied artifact line")
        if "co-located with the generated testbench" not in text or "ahdl_include" not in text:
            missing.append(f"{row['task_id']}: no supplied DUT include contract")

    assert missing == []


def test_counted_tb_and_e2e_prompts_explain_spectre_harness_syntax() -> None:
    missing: list[str] = []
    required = [
        "## Public Spectre Testbench Scaffold",
        "ahdl_include",
        "XNAME (node1 node2 ...) module_name",
        "Do not use module-first syntax",
    ]
    for row in counted_form_rows():
        if row["form"] not in {"tb", "e2e"}:
            continue
        prompt = (ROOT / row["manifest"]).parent / "prompt.md"
        text = prompt.read_text(encoding="utf-8")
        absent = [needle for needle in required if needle not in text]
        if absent:
            missing.append(f"{row['task_id']}: missing {absent}")

    assert missing == []
