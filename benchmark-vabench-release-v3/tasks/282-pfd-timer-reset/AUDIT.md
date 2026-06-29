# Two-Gate SOP Audit: Task 282 PFD Timer Reset

## Scope

Task 282 implements the same delayed mutual-reset PFD behavior as task 300,
with different signal names and a `100 ps` default reset delay.

## Gate 1: Admission And Counting

- Admission label: `hard_duplicate_rewrite_or_remove`.
- Counting decision: keep task 282 only as a non-counted duplicate/migration
  artifact while task 300 carries the canonical active-low-UP PFD delayed-reset
  coverage.
- Duplicate evidence: both tasks are DUT rows for a two-input PFD with
  active-low UP output, active-high DOWN output, and timer-based mutual reset
  after both sides have occurred.
- Independent value: task 282 remains useful as a regression fixture for the
  `a/b/ub/d` interface and `100 ps` delay, but not as a second independent PFD
  benchmark in the current release.

## Rewrite Path For Independent Coverage

Task 282 should stay non-counted unless rewritten to cover a distinct PFD
function, such as reset-pulse width measurement, dead-zone behavior, no-overlap
race handling, tri-state charge-pump interface behavior, or a composed PLL
timing/reacquisition flow.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for the artifact itself; non-counted
  for independent coverage.
- Prompt hygiene: the public prompt now removes source-provenance wording and
  exposes `vth`, `vh`, `reset_delay`, active-low `ub`, active-high `d`, and
  timer-reset behavior. The public `tr` transition parameter is also exposed.
- Gold quality: the gold model uses `initial_step`, `cross`, `timer`, and
  `transition` in a reviewable voltage-domain event model.
- Negative strength: four concrete negatives reject zero output, missing
  delayed reset, active-high UP output, and zero reset delay.

## Evidence

- Human confirmation: the reviewed 282/300 pair was confirmed as duplicate PFD
  delayed mutual-reset coverage; a single PFD DUT is L1, not L2, and the
  100 ps vs 80 ps default delay difference is not independent benchmark
  coverage by itself.
- Visible/hidden relationship: `test_visible/tests/tb_visible_smoke.scs` is a
  public smoke deck; `test_hidden/tests/tb_source_ref.scs` now uses different
  `a/b` edge ordering/timing, extra reset events, and stop time.
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
