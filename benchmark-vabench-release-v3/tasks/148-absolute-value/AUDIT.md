# Two-Gate SOP Audit: Task 148 Absolute Value

## Scope

Task 148 implements the same absolute-value transfer function as task 288, with
only the target module/file name changed from `absolute_value.va` to
`absolute_value_behavior.va`.

## Gate 1: Admission And Counting

- Admission label: `hard_duplicate_rewrite_or_remove`.
- Counting decision: keep task 148 only as a non-counted duplicate/migration
  artifact while task 288 carries the canonical independent absolute-value L1
  coverage.
- Duplicate evidence: both tasks are DUT rows, both implement
  `sigout = abs(sigin)`, and both use the same `v3_source_absolute_value`
  checker.
- Independent value: current task 148 assets are useful as a regression fixture
  for the legacy module name, but not as a second circuit-function benchmark.

## Rewrite Path For Independent Coverage

Task 148 should stay non-counted unless it is rewritten to cover a distinct
absolute-value-related function, such as a differential absolute-value front end,
rail-clamped magnitude detector, signed-magnitude splitter, or precision
rectifier model with explicit common-mode/rail behavior.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for the artifact itself; non-counted
  for benchmark coverage.
- Prompt hygiene: the public prompt now describes only the module interface,
  behavior, and modeling constraints, with no historical source-provenance
  wording.
- Checker alignment: the checker evaluates `sigout` against `abs(sigin)` over
  stable sampled transient rows.
- Negative strength: four concrete negatives reject zero output, signed
  passthrough, negative absolute value, and half-scale behavior.

## Evidence

- Human confirmation: the reviewed 148/288 pair was confirmed as duplicate
  absolute-value coverage; task 148 remains useful only as a non-counted
  migration/regression artifact unless rewritten to a distinct rectifier or
  magnitude function.
- Visible/hidden relationship: `test_visible/tests/tb_visible_smoke.scs` is a
  public smoke deck; `test_hidden/tests/tb_source_ref.scs` now uses a different
  input waveform and stop time for private coverage.
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
