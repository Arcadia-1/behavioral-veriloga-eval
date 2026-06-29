# Two-Gate SOP Audit: Task 146 Smooth Comparator Tanh

## Scope

Task 146 is the canonical generic smooth tanh comparator in the reviewed
146/292 pair. It exposes the output levels, input offset, and slope as public
parameters.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: keep task 146 as the scored independent L1 smooth
  comparator row. Treat task 292 as a non-counted transfer-curve variant unless
  an explicit counting policy or rewrite makes it distinct.
- Function boundary: parameterized continuous comparator transfer from
  `V(sigin,sigref)` to `sigout`.
- Checker alignment: the checker samples the public tanh transfer at multiple
  operating points and rejects polarity, slope, and output-span errors.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for this audited artifact.
- Prompt hygiene: the public prompt now removes source-provenance wording and
  declares the public parameter contract required by the visible testbench.
- Gold quality: the gold model is a pure voltage-domain tanh contribution with
  declared ports and overrideable parameters.
- Negative strength: four concrete negatives reject zero output, inverted
  input difference, half slope, and half output span.

## Evidence

- Human confirmation: the reviewed 146/292 pair was confirmed as overlapping
  smooth-tanh-comparator coverage; different names, defaults, and sample points
  are not enough by themselves to make 292 a second independent function.
- Visible/hidden relationship: `test_visible/tests/tb_visible_smoke.scs` is a
  public smoke deck; `test_hidden/tests/tb_source_ref.scs` now uses different
  PWL input/reference timing and stop time while keeping the public
  high/low/offset/slope contract.
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
