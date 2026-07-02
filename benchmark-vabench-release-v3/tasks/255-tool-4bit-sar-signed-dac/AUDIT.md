# Tool 4bit SAR Signed DAC Audit

- Gate 1: `independent_l1_ready`. This is a signed SAR reconstruction
  DAC/readout component. Human review confirmed that reusable converter
  readout/calibration macros with standalone public behavior should count as
  independent benchmark components.
- Gate 2: EVAS-ready, Cadence lint/Spectre pending. Public prompt now states
  interface, threshold, gain, transition time, signed bit contribution, sample
  trigger, and hold behavior. Starter and gold both expose the public `tr`
  parameter, and gold uses it for the output transition.
- Hidden coverage: repaired to use a distinct sample clock and bit pattern from
  the visible smoke deck.
- Checker: upgraded from fixed samples to sample-triggered signed weighted-sum
  checks derived from the observed decision bits.
- Negatives: zero output, unipolar interpretation, wrong gain, and falling-edge
  sampling variants are rejected by the behavior checker.
- Cadence/Spectre: not rerun in this branch because the local bridge readiness
  check reports bridge setup missing; this is a validation-environment block,
  not a known model failure.
