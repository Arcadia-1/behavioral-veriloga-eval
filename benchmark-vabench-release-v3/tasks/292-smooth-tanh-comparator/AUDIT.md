# Two-Gate SOP Audit: Task 292 Smooth Tanh Comparator

## Scope

Task 292 is a fixed-default smooth tanh comparator variant that overlaps with
the generic smooth comparator covered by task 146.

## Gate 1: Admission And Counting

- Admission label: `valid_variant_needs_counting_policy`.
- Counting decision: keep task 292 as a non-counted transfer-curve variant in
  the current release unless the benchmark policy explicitly allows multiple
  parameterized tanh-comparator variants as separate coverage rows.
- Overlap evidence: tasks 146 and 292 are both DUT rows implementing a smooth
  tanh comparator from `sigin/sigref` to `sigout`.
- Distinguishing evidence: task 292 uses a different module name, parameter
  names, default offset, default slope, and checker sample points. This makes it
  a valid regression variant, but not clearly a second independent circuit
  function.

## Rewrite Path For Independent Coverage

Task 292 could become independent if rewritten to add a distinct comparator
function, such as hysteresis, rail-derived output levels, differential input
common-mode handling, offset calibration, noise-aware decision behavior, or a
measurement flow for extracting comparator smoothness.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for the artifact itself; non-counted
  for independent coverage unless counting policy changes.
- Prompt hygiene: the public prompt now removes source-provenance wording and
  declares the default `sigout_high`, `sigout_low`, `sigin_offset`, and
  `comp_slope` contract.
- Gold quality: the gold model is a pure voltage-domain tanh contribution with
  declared ports and overrideable parameters.
- Negative strength: four concrete negatives reject zero output, missing
  offset, wrong slope, and hard-comparator behavior.

## Evidence

- Human confirmation: the reviewed 146/292 pair was confirmed as overlapping
  smooth-tanh-comparator coverage; task 292 is a non-counted variant unless a
  future counting policy or rewrite makes it distinct.
- Visible/hidden relationship: `test_visible/tests/tb_visible_smoke.scs` is a
  public smoke deck; `test_hidden/tests/tb_source_ref.scs` now uses different
  input/reference timing and stop time while preserving the public transfer
  contract.
- EVAS gold: visible PASS and hidden PASS
  (`/private/tmp/v3_evas_phase1_5/gold_summary.json`).
- EVAS negatives: 4/4 behavioral rejections, all with DUT/TB compile and
  `FAIL_SIM_CORRECTNESS`
  (`/private/tmp/v3_evas_phase1_5/negative_summary.json`).
- Spectre gold: visible PASS and hidden PASS
  (`/private/tmp/v3_spectre_phase1_5_visible.json`,
  `/private/tmp/v3_spectre_phase1_5_hidden.json`).
- Spectre negatives: 4/4 `NEGATIVE_REJECTED`
  (`/private/tmp/v3_spectre_phase1_5_negatives.json`).
- AHDL lint/read-in triage: Spectre visible/hidden/negative logs were
  inspected for `AHDLLINT-*` messages; none were present. The remaining
  warnings are the shared `VACOMP-2435` environment notice and `SPECTRE-592`
  setup notice, not task-specific AHDL lint failures.
