from __future__ import annotations

import json
from pathlib import Path

from runners.run_vabench_release_minimax_baseline import release_support_artifacts


def test_release_support_artifacts_loads_bugfix_public_input_only(tmp_path: Path) -> None:
    task_dir = tmp_path / "forms" / "bugfix"
    gold_dir = task_dir / "gold"
    gold_dir.mkdir(parents=True)
    (task_dir / "release_task.json").write_text(
        json.dumps({"family": "bugfix"}),
        encoding="utf-8",
    )
    (task_dir / "meta.json").write_text(
        json.dumps({"inputs": ["prompt.md", "gold/dut_buggy.va"]}),
        encoding="utf-8",
    )
    (gold_dir / "dut_buggy.va").write_text("module buggy; endmodule\n", encoding="utf-8")
    (gold_dir / "dut_fixed.va").write_text("module fixed; endmodule\n", encoding="utf-8")

    support = release_support_artifacts(task_dir, ["dut_fixed.va"])

    assert support == {"dut_buggy.va": "module buggy; endmodule\n"}


def test_release_support_artifacts_falls_back_for_legacy_bugfix_meta(tmp_path: Path) -> None:
    task_dir = tmp_path / "forms" / "bugfix"
    gold_dir = task_dir / "gold"
    gold_dir.mkdir(parents=True)
    (task_dir / "release_task.json").write_text(
        json.dumps({"family": "bugfix"}),
        encoding="utf-8",
    )
    (task_dir / "meta.json").write_text(
        json.dumps({"inputs": ["prompt.md"]}),
        encoding="utf-8",
    )
    (gold_dir / "dut_buggy.va").write_text("module buggy; endmodule\n", encoding="utf-8")

    support = release_support_artifacts(task_dir, ["dut_fixed.va"])

    assert support == {"dut_buggy.va": "module buggy; endmodule\n"}
