# Two-Gate SOP Audit: Task 288 Absolute Value

## Scope

Task 288 is the canonical absolute-value voltage primitive for the reviewed
148/288 pair.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: keep task 288 as the scored independent L1 absolute-value
  primitive. Do not count task 148 as a second independent absolute-value row
  unless it is rewritten into a distinct function.
- Function boundary: memoryless voltage primitive that maps `sigin` to
  `abs(V(sigin))` at `sigout`.
- Checker alignment: the local checker directly evaluates the claimed
  absolute-value transfer.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for this audited artifact.
- Prompt hygiene: the public prompt now avoids source-import provenance and
  exposes only the public interface, behavior, output artifact, and modeling
  constraints.
- Gold quality: the gold model is a small pure voltage-domain contribution with
  declared electrical ports and no unsupported operators.
- Negative strength: four concrete negatives reject zero output, signed
  passthrough, half-scale magnitude, and squared-magnitude behavior.

## Evidence

- Human confirmation: task 288 is the canonical counted absolute-value L1 row
  for the reviewed 148/288 pair; task 148 stays non-counted unless rewritten.
- Visible/hidden relationship: `test_visible/tests/tb_visible_smoke.scs` is a
  public smoke deck; `test_hidden/tests/tb_source_ref.scs` now uses a different
  input waveform and stop time for private coverage.
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
