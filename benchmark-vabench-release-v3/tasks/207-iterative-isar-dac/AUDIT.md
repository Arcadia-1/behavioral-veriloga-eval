# Iterative ISAR DAC Audit

- Gate 1: independent L1 rework candidate retained. The row models an
  iterative SAR-style DAC estimate generator with reset, comparator-polarity
  response, and shrinking search step.
- Gate 2: EVAS-ready, Cadence lint/Spectre pending. Public prompt now states
  interface, public parameters, reset behavior, update polarity, halving
  contract, and stop threshold.
- Hidden coverage: repaired to use a distinct reset sequence, clock spacing,
  comparator-decision pattern, and overridden search range.
- Checker: upgraded from fixed stable samples to reset, update-direction, and
  step-ratio checks derived from observed clock and reset events.
- Negatives: zero output, inverted comparator polarity, no step halving, and
  wrong reset-to-range behavior are rejected by the behavior checker.
- Cadence/Spectre: not rerun in this branch because the local bridge readiness
  check reports bridge setup missing; this is a validation-environment block,
  not a known model failure.
