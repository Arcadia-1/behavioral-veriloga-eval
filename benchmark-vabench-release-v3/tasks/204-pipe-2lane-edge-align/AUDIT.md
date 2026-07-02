# Pipe 2-Lane Edge Align Audit

- Gate 1: independent L1 rework candidate retained. The row models a reusable
  two-lane time-interleaved converter alignment selector, not just a parameter
  variant.
- Gate 2: EVAS-ready, Cadence lint/Spectre pending. Public prompt now states
  interface, threshold, edge-polarity behavior, and modeling constraints.
- Hidden coverage: repaired to use non-identical lane values and non-uniform
  alignment edge timing relative to the visible smoke deck.
- Checker: upgraded from fixed stable samples to event-derived lane selection
  checks after rising and falling alignment-clock crossings.
- Negatives: zero output, swapped edge polarity, always-first-lane, and
  half-output-level variants are rejected by the behavior checker.
- Cadence/Spectre: not rerun in this branch because the local bridge readiness
  check reports bridge setup missing; this is a validation-environment block,
  not a known model failure.
