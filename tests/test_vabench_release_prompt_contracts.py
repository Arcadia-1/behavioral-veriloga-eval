from __future__ import annotations

import json
from pathlib import Path

from runners.vabench_release_paths import release_form_dir


ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = ROOT / "benchmark-vabench-release-v1" / "tasks"
MANIFEST = ROOT / "benchmark-vabench-release-v1" / "MANIFEST.json"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _target_artifacts(form: str, names: list[str]) -> list[str]:
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


def _release_form_dirs() -> list[Path]:
    return sorted(path.parent for path in TASKS_ROOT.glob("*/vbr1_*/forms/*/release_task.json"))


def test_release_prompts_have_public_contract_scaffold() -> None:
    form_dirs = _release_form_dirs()
    manifest = _read_json(MANIFEST)
    assert len(form_dirs) == manifest["summary"]["form_count"]

    for form_dir in form_dirs:
        release_task = _read_json(form_dir / "release_task.json")
        prompt = (form_dir / "prompt.md").read_text(encoding="utf-8")
        form = form_dir.name

        assert prompt.startswith(f"# Task: {release_task['id']}\n"), form_dir
        assert "\n## Release Task Contract\n" in prompt, form_dir
        assert f"- Form: `{form}`" in prompt, form_dir
        assert "\n## Output Contract\n" in prompt, form_dir
        assert "\n## Task-Specific Public Description\n" in prompt, form_dir


def test_release_prompt_targets_match_gold_artifact_contract() -> None:
    for form_dir in _release_form_dirs():
        release_task = _read_json(form_dir / "release_task.json")
        prompt = (form_dir / "prompt.md").read_text(encoding="utf-8")
        gold_names = [Path(path).name for path in release_task["artifacts"]["gold"]]
        for target in _target_artifacts(form_dir.name, gold_names):
            assert f"`{target}`" in prompt, form_dir


def test_release_prompts_do_not_embed_runner_or_overdirect_repair_text() -> None:
    forbidden = [
        "Bug to fix:",
        "injected Strict EVAS Validation Contract",
        "Question:",
        "Answer:",
        "System:",
        "few-shot",
        "ICL",
        "[BEGIN file]",
        "[DONE file]",
        "Reference artifact name(s):",
        "Reference testbench artifact names:",
    ]
    for form_dir in _release_form_dirs():
        prompt = (form_dir / "prompt.md").read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in prompt, (form_dir, needle)


def test_converter_front_end_e2e_uses_release_testbench_artifact_name() -> None:
    prompt = (release_form_dir(TASKS_ROOT, "vbr1_l2_converter_front_end", "e2e") / "prompt.md").read_text(
        encoding="utf-8"
    )
    assert "`tb_sample_hold_droop_ref.scs`" in prompt
    assert "`tb_sample_hold_droop.scs`" not in prompt
