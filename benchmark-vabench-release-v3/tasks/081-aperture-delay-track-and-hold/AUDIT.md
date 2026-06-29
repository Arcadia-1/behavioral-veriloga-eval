# Two-Gate SOP Audit: Task 081 Aperture Delay Track And Hold

## Scope

Task 081 is the canonical aperture-delay sample/track-and-hold DUT row for the
081/285 high-overlap pair. It targets one Verilog-A artifact,
`sample_hold_aperture_ref.va`, with visible and hidden Spectre-compatible
testbenches.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: count 081 as the standalone L1 aperture-delay
  sample/track-and-hold function. Do not also count 285 as independent coverage
  unless 285 is rewritten to a genuinely different function or artifact role.
- Function boundary: the DUT captures `vin` at a delayed aperture instant after
  each rising clock crossing and holds the sampled analog value on `vout`.
- Evaluation alignment: the hidden stimulus is aperture-sensitive, with input
  transitions shortly after rising clock edges so edge-time sampling fails.
- Checker alignment: `v3_081_aperture_delay_track_and_hold` validates delayed
  sample values and held output behavior through the shared aperture checker.
- Negatives: four concrete variants are expected to compile and fail behavioral
  correctness: zero output, edge-time sampling, half-gain sampling, and
  rail-relative inverted sampling.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_lint_pending`.
- Prompt hygiene: public prompt no longer exposes hidden evaluator wording or
  the old migration id as the public title.
- Public contract: prompt declares the target artifact, module interface,
  public parameters `vth`, `taperture`, and `tedge`, visible testbench
  observables, and voltage-only modeling constraints.
- Gold quality: gold uses Spectre-compatible includes, electrical ports,
  overrideable parameters, `cross`, `timer`, and `transition` for delayed
  voltage-domain sampling.
- Cadence gap: Spectre hidden gold and negative evidence is attached, but AHDL
  linter evidence is not yet recorded.

## Evidence

- EVAS hidden gold smoke: PASS.
- EVAS hidden negatives: 4/4 FAIL_SIM_CORRECTNESS.
- Spectre hidden gold: PASS.
- Spectre hidden negatives: 4/4 NEGATIVE_REJECTED.
- Negative failures are behavioral checker failures, not syntax/setup failures.
