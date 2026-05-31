from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from report_deepseek_failure_attribution import classify, is_incomplete_generation  # noqa: E402
from run_vabench_release_model_dual_judge import (  # noqa: E402
    is_incomplete_generation as is_runner_incomplete_generation,
)
from score import find_va_file_for_tb, rewrite_tb_save_signals  # noqa: E402


def test_find_va_file_for_tb_prefers_exact_ahdl_include(tmp_path: Path) -> None:
    sample_dir = tmp_path / "sample"
    sample_dir.mkdir()
    (sample_dir / "clk_divider.va").write_text(
        "module clk_divider(CLK_IN, RST_N, CLK_OUT, LOCK); endmodule\n",
        encoding="utf-8",
    )
    (sample_dir / "clk_divider_ref.va").write_text(
        "module clk_divider_ref(clk_in, rst_n, div_code_0, clk_out, lock); endmodule\n",
        encoding="utf-8",
    )
    tb_path = tmp_path / "tb_clk_divider_ref.scs"
    tb_path.write_text(
        'ahdl_include "clk_divider_ref.va"\n'
        "XDUT (clk_in rst_n div_code_0 clk_out lock) clk_divider_ref\n",
        encoding="utf-8",
    )

    assert find_va_file_for_tb(sample_dir, tb_path) == sample_dir / "clk_divider_ref.va"


def test_length_capped_empty_generation_is_model_incomplete() -> None:
    row = {"status": "SKIPPED", "skip_reason": "missing_candidate_files"}
    meta = {"status": "no_code_extracted", "finish_reason": "length"}

    result = classify(row, "", meta)

    assert is_incomplete_generation(meta)
    assert is_runner_incomplete_generation(meta)
    assert result["primary_attribution"] == "model_incomplete_generation"
    assert result["root_cause_family"] == "model_output_budget_exhausted"
    assert result["root_cause_detail"] == "incomplete_no_code_extracted_finish_reason_length"
    assert result["counts_as_direct_model_failure"] is True


def test_rewrite_save_removes_multiline_continuations(tmp_path: Path) -> None:
    tb_path = tmp_path / "tb.scs"
    tb_path.write_text(
        "simulator lang=spectre\n"
        "save clk_in rst_n clk_out lock \\\n"
        "  div_code_0 div_code_1 div_code_2 div_code_3 \\\n"
        "  div_code_4 div_code_5 div_code_6 div_code_7\n"
        "tran tran stop=80n\n",
        encoding="utf-8",
    )

    removed, inserted = rewrite_tb_save_signals(tb_path, ["clk_in", "rst_n", "clk_out", "lock"])

    assert (removed, inserted) == (3, 1)
    assert tb_path.read_text(encoding="utf-8").splitlines() == [
        "simulator lang=spectre",
        "save clk_in rst_n clk_out lock",
        "tran tran stop=80n",
    ]
