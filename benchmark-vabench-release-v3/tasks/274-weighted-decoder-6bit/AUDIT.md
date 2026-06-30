# Two-Gate SOP Audit: Task 274 Weighted Decoder 6bit

## Scope

Task 274 implements a 6-bit binary-weighted voltage decoder. It is related to
task 294 by the general weighted-DAC theme, but the width, radix, bit order, and
normalization contract are different.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: keep task 274 as an independent L1 data-converter
  weighting row.
- Function boundary: six voltage-coded inputs are thresholded and mapped to a
  binary weighted output where the all-ones input code maps to full scale.
- Distinctness from 294: task 274 is a 6-bit binary weighted decoder; task 294
  is a 10-bit sub-radix DAC with radix 1.8 and a different full-scale code
  normalization.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for this audited artifact.
- Prompt hygiene: the public prompt now removes source-provenance wording and
  exposes `vth`, `vref`, bit order, and the observable full-scale convention
  without spelling out private implementation arithmetic.
- Gold quality: the gold model is a pure voltage-domain thresholded weighted
  sum with declared electrical ports. Its binary full-scale denominator is the
  all-ones 6-bit code, not the MSB weight alone.
- Negative strength: four concrete negatives reject zero output, wrong
  denominator, half scale, and too-high threshold behavior.

## Evidence

- Human confirmation: the reviewed 274/294 pair was confirmed as a legitimate
  split: task 274 is binary 6-bit decoder weighting, while task 294 is 10-bit
  radix-1.8 sub-radix weighting.
- Cadence reference check: the local Cadence Verilog-AMS data-converter lesson
  uses code/full-scale style normalization for ideal converter examples. This
  supports the public all-ones full-scale convention while keeping concrete
  arithmetic out of the prompt.
- Visible/hidden relationship: `test_visible/tests/tb_visible_smoke.scs` is a
  public smoke deck; `test_hidden/tests/tb_source_ref.scs` now uses different
  bit PWL patterns and stop time for private bit-order/weight coverage.
- EVAS gold after normalization repair: visible PASS and hidden PASS
  (`external-evidence/v3_evas_phase1_5_normfix_r2_summary.json`).
- EVAS negatives after normalization repair: 4/4 behavioral rejections, all
  with DUT/TB compile and `FAIL_SIM_CORRECTNESS`
  (`external-evidence/v3_evas_phase1_5_normfix_r2_summary.json`).
- Spectre gold after normalization repair: visible PASS and hidden PASS
  (`external-evidence/v3_spectre_normfix_visible.json`,
  `external-evidence/v3_spectre_normfix_hidden.json`).
- Spectre negatives after normalization repair: 4/4 `NEGATIVE_REJECTED`
  (`external-evidence/v3_spectre_normfix_negatives.json`).
- AHDL lint/read-in triage: Spectre visible/hidden/negative logs were
  inspected for `AHDLLINT-*` messages; none were present. The remaining
  warnings are the shared `VACOMP-2435` environment notice and `SPECTRE-592`
  setup notice, not task-specific AHDL lint failures.
