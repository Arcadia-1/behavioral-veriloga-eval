# Two-Gate SOP Audit: Task 294 Subradix DAC10

## Scope

Task 294 implements a 10-bit sub-radix weighted DAC. It is related to task 274
by the general weighted-DAC theme, but it has a different width, radix, bit
order, and normalization contract.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: keep task 294 as an independent L1 data-converter
  sub-radix weighting row.
- Function boundary: ten voltage-coded inputs are thresholded and mapped to a
  radix-1.8 weighted output where the all-ones sub-radix code maps to full
  scale.
- Distinctness from 274: task 294 is not a binary 6-bit decoder; it validates
  sub-radix weights and MSB/LSB ordering over a 10-bit interface.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for this audited artifact.
- Prompt hygiene: the public prompt now removes source-provenance wording and
  exposes `vth`, `vref`, bit order, radix-1.8 adjacency, and the observable
  full-scale convention without spelling out private implementation arithmetic.
- Gold quality: the gold model is a pure voltage-domain thresholded weighted
  sum with declared electrical ports. Its full-scale denominator is the
  all-ones radix-1.8 weight sum, not a binary-code denominator.
- Negative strength: four concrete negatives reject zero output, ordinary
  binary weights, wrong normalization, and reversed MSB/LSB ordering.

## Evidence

- Human confirmation: the reviewed 274/294 pair was confirmed as a legitimate
  split: task 294 is 10-bit radix-1.8 sub-radix weighting, not the same
  function as task 274's binary 6-bit decoder.
- Cadence reference check: the local Cadence Verilog-AMS data-converter lesson
  uses code/full-scale style normalization for ideal converter examples. This
  supports the public all-ones full-scale convention while keeping concrete
  arithmetic out of the prompt.
- Visible/hidden relationship: `test_visible/tests/tb_visible_smoke.scs` is a
  public smoke deck; `test_hidden/tests/tb_source_ref.scs` now uses different
  bit PWL patterns and stop time for private radix/bit-order coverage.
- EVAS gold after normalization repair: visible PASS and hidden PASS
  (`/private/tmp/v3_evas_phase1_5_normfix_r2_summary.json`).
- EVAS negatives after normalization repair: 4/4 behavioral rejections, all
  with DUT/TB compile and `FAIL_SIM_CORRECTNESS`
  (`/private/tmp/v3_evas_phase1_5_normfix_r2_summary.json`).
- Spectre gold after normalization repair: visible PASS and hidden PASS
  (`/private/tmp/v3_spectre_normfix_visible.json`,
  `/private/tmp/v3_spectre_normfix_hidden.json`).
- Spectre negatives after normalization repair: 4/4 `NEGATIVE_REJECTED`
  (`/private/tmp/v3_spectre_normfix_negatives.json`).
- AHDL lint/read-in triage: Spectre visible/hidden/negative logs were
  inspected for `AHDLLINT-*` messages; none were present. The remaining
  warnings are the shared `VACOMP-2435` environment notice and `SPECTRE-592`
  setup notice, not task-specific AHDL lint failures.
