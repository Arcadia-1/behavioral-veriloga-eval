# Tool 4bit SAR Signed DAC Audit

- Gate 1: independent L1 rework candidate retained as a signed SAR helper DAC.
  It is counted only if the benchmark policy admits helper DAC/readout macros
  as standalone functions.
- Gate 2: EVAS-ready, Cadence lint/Spectre pending. Public prompt now states
  interface, threshold, gain, signed bit contribution, sample trigger, and
  hold behavior.
- Hidden coverage: repaired to use a distinct sample clock and bit pattern from
  the visible smoke deck.
- Checker: upgraded from fixed samples to sample-triggered signed weighted-sum
  checks derived from the observed decision bits.
- Negatives: zero output, unipolar interpretation, wrong gain, and falling-edge
  sampling variants are rejected by the behavior checker.
- Cadence/Spectre: not rerun in this branch because the local bridge readiness
  check reports bridge setup missing; this is a validation-environment block,
  not a known model failure.
