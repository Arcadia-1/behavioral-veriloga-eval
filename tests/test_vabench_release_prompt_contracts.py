from __future__ import annotations

import json
from pathlib import Path

from runners.vabench_release_paths import release_form_dir


ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = ROOT / "benchmark-vabench-release-v1" / "tasks"
MANIFEST = ROOT / "benchmark-vabench-release-v1" / "MANIFEST.json"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _target_artifacts(form: str, names: list[str], explicit: list[str] | None = None) -> list[str]:
    if explicit:
        return [str(item) for item in explicit]
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
    manifest = _read_json(MANIFEST)
    return sorted(ROOT / row["release_task_manifest"] for row in manifest["forms"])


def test_release_prompts_have_public_contract_scaffold() -> None:
    form_dirs = _release_form_dirs()
    manifest = _read_json(MANIFEST)
    assert len(form_dirs) == manifest["summary"]["form_count"]

    for release_task_path in form_dirs:
        form_dir = release_task_path.parent
        release_task = _read_json(release_task_path)
        prompt = (form_dir / "prompt.md").read_text(encoding="utf-8")
        form = form_dir.name

        assert prompt.startswith(f"# Task: {release_task['id']}\n"), form_dir
        assert "\n## Release Task Contract\n" in prompt, form_dir
        assert f"- Form: `{form}`" in prompt, form_dir
        assert "\n## Output Contract\n" in prompt, form_dir
        assert "\n## Task-Specific Public Description\n" in prompt, form_dir


def test_release_prompt_targets_match_gold_artifact_contract() -> None:
    for release_task_path in _release_form_dirs():
        form_dir = release_task_path.parent
        release_task = _read_json(release_task_path)
        prompt = (form_dir / "prompt.md").read_text(encoding="utf-8")
        artifacts = release_task["artifacts"]
        gold_names = [Path(path).name for path in artifacts["gold"]]
        explicit = artifacts.get("submission_artifacts")
        for target in _target_artifacts(form_dir.name, gold_names, explicit if isinstance(explicit, list) else None):
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
        "Known defect:",
        "[BEGIN file]",
        "[DONE file]",
        "Reference artifact name(s):",
        "Reference testbench artifact names:",
    ]
    for release_task_path in _release_form_dirs():
        form_dir = release_task_path.parent
        prompt = (form_dir / "prompt.md").read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in prompt, (form_dir, needle)


def test_ct07_ct08_l1_prompts_expose_public_behavioral_targets() -> None:
    target_phrases = {
        "vbr1_l1_bandgap_reference_macro_model": "supply-insensitive reference",
        "vbr1_l1_bias_voltage_generator_with_enable_trim": "combined enable/trim control",
        "vbr1_l1_ptat_ctat_reference_generator": "opposing PTAT and CTAT",
        "vbr1_l1_power_on_reset_detector": "four rising clock updates",
        "vbr1_l1_uvlo_brownout_detector": "UVLO hysteresis band",
        "vbr1_l1_ldo_regulator_macro_model": "load/disturbance control",
        "vbr1_l1_lna_gain_compression_macro": "small-signal out should show gain",
        "vbr1_l1_rf_mixer_downconverter_macro": "LO-polarity waveform",
        "vbr1_l1_pa_compression_macro": "Large drive should compress",
        "vbr1_l1_log_rssi_power_detector": "compressed or piecewise approximation",
        "vbr1_l1_limiting_amplifier_frontend": "preserve signal polarity",
    }
    for entry_id, phrase in target_phrases.items():
        entry_dir = next(TASKS_ROOT.glob(f"*/{entry_id}"))
        for form_dir in sorted((entry_dir / "forms").iterdir()):
            if not form_dir.is_dir():
                continue
            prompt = (form_dir / "prompt.md").read_text(encoding="utf-8")
            assert "\n## Public Behavioral Targets\n" in prompt, form_dir
            assert phrase in prompt, form_dir


def test_converter_front_end_e2e_uses_release_testbench_artifact_name() -> None:
    prompt = (release_form_dir(TASKS_ROOT, "vbr1_l2_converter_front_end", "e2e") / "prompt.md").read_text(
        encoding="utf-8"
    )
    assert "`tb_sample_hold_droop_ref.scs`" in prompt
    assert "`tb_sample_hold_droop.scs`" not in prompt


def test_clock_divider_dut_targets_only_ref_artifact() -> None:
    form_dir = release_form_dir(TASKS_ROOT, "vbr1_l1_clock_divider", "dut")
    release_task = _read_json(form_dir / "release_task.json")
    prompt = (form_dir / "prompt.md").read_text(encoding="utf-8")

    assert release_task["artifacts"]["submission_artifacts"] == ["clk_divider_ref.va"]
    assert "- Target artifact(s): `clk_divider_ref.va`" in prompt
    assert "- Target artifact(s): `clk_divider.va`, `clk_divider_ref.va`" not in prompt
