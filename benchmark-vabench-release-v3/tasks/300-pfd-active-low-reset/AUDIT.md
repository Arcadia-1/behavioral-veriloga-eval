# Two-Gate SOP Audit: Task 300 PFD Active Low Reset

## Scope

Task 300 is the canonical active-low-UP PFD delayed-reset row for the reviewed
282/300 pair.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: keep task 300 as the scored PFD delayed mutual-reset
  coverage row. Do not count task 282 as a second independent PFD row unless it
  is rewritten to a distinct function.
- Function boundary: standalone voltage-domain PFD/clock-timing component with
  REF/FB edge capture, active-low `upb`, active-high `down`, and delayed timer
  reset.
- Checker alignment: the checker samples both outputs before assertion, during
  isolated UP/DOWN phases, during both-active overlap, and after reset.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for this audited artifact.
- Prompt hygiene: the public prompt now removes source-provenance wording and
  exposes `vth`, `vh`, `reset_delay = 80 ps`, output polarity, and timer-reset
  semantics. The public `tr` transition parameter is also exposed.
- Gold quality: the gold model uses `initial_step`, `cross`, `timer`, and
  `transition` in a reviewable voltage-domain event model.
- Negative strength: four concrete negatives reject zero output, active-high
  UP behavior, immediate reset, and swapped edge handling.

## Evidence

- Human confirmation: task 300 is the canonical counted PFD delayed
  mutual-reset L1 row for the reviewed 282/300 pair; task 282 remains
  non-counted unless rewritten to a distinct PFD or flow function. A single PFD
  DUT is L1, not L2.
- Visible/hidden relationship: `test_visible/tests/tb_visible_smoke.scs` is a
  public smoke deck; `test_hidden/tests/tb_source_ref.scs` now uses different
  `ref/fb` edge ordering/timing, extra reset events, and stop time.
- EVAS gold: visible PASS and hidden PASS
  (`external-evidence/v3_evas_phase1_5/gold_summary.json`).
- EVAS negatives: 4/4 behavioral rejections, all with DUT/TB compile and
  `FAIL_SIM_CORRECTNESS`
  (`external-evidence/v3_evas_phase1_5/negative_summary.json`).
- Spectre gold: visible PASS and hidden PASS
  (`external-evidence/v3_spectre_phase1_5_visible.json`,
  `external-evidence/v3_spectre_phase1_5_hidden.json`).
- Spectre negatives: 4/4 `NEGATIVE_REJECTED`
  (`external-evidence/v3_spectre_phase1_5_negatives.json`).
- AHDL lint/read-in triage: Spectre visible/hidden/negative logs were
  inspected for `AHDLLINT-*` messages; none were present. The remaining
  warnings are the shared `VACOMP-2435` environment notice and `SPECTRE-592`
  setup notice, not task-specific AHDL lint failures.
