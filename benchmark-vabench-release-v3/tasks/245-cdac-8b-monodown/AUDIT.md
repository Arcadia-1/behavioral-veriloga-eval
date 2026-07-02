# CDAC 8b Monodown Audit

- Gate 1: independent L1 rework candidate retained. The row models a
  monotonic-down SAR CDAC residue update, distinct from static weighted DAC
  rows because it has sampling and event-by-event residue evolution.
- Gate 2: EVAS-ready, Cadence lint/Spectre pending. Public prompt now states
  interface, sampling edge, normalized reference span, and binary-weighted
  downward switching contract.
- Hidden coverage: repaired to use non-sequential control edges, a resampling
  event, and a changed input residue.
- Checker: upgraded from fixed samples to event-derived residue tracking over
  `clks` falling and `dctrl` rising events.
- Negatives: zero output, wrong MSB weight, wrong sign, and half-output variants
  are rejected by the behavior checker.
- Cadence/Spectre: not rerun in this branch because the local bridge readiness
  check reports bridge setup missing; this is a validation-environment block,
  not a known model failure.
