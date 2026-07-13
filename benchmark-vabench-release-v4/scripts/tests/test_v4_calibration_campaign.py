from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "operations" / "calibration_pilot" / "build_campaign.py"
SPEC = importlib.util.spec_from_file_location("build_v4_calibration_campaign", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_preregistered_campaign_has_180_cells_and_balanced_modes() -> None:
    campaign = MODULE.build_campaign(
        ROOT / "release" / "tri-form-v4-1200-final",
        ROOT / "operations" / "calibration_pilot" / "CALIBRATION_FAMILIES.json",
        model_provider="openai-compatible",
        model="test-model",
        max_working_tokens=8192,
        repetitions=1,
    )
    assert campaign["family_count"] == 10
    assert campaign["task_count"] == 30
    assert campaign["cell_count"] == 180
    assert {row["mode"] for row in campaign["cells"]} == {f"G{i}" for i in range(6)}
    assert campaign["max_output_tokens"] == 8192
    assert campaign["budget_metric"] == "provider_completion_tokens_including_reasoning"
    assert {row["max_output_tokens"] for row in campaign["cells"]} == {8192}
    assert sum(row["process"] == "direct_one_shot" for row in campaign["cells"]) == 60
    assert sum(row["process"] == "agentic" for row in campaign["cells"]) == 120


def test_agentic_and_direct_tool_boundaries_match_modes() -> None:
    campaign = MODULE.build_campaign(
        ROOT / "release" / "tri-form-v4-1200-final",
        ROOT / "operations" / "calibration_pilot" / "CALIBRATION_FAMILIES.json",
        model_provider="test",
        model="test-model",
        max_working_tokens=1,
        repetitions=1,
    )
    for row in campaign["cells"]:
        assert row["feedback_cli_available"] is (row["mode"] in {"G2", "G3", "G4", "G5"})
