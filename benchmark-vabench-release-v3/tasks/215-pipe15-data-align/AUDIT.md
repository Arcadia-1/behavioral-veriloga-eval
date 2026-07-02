# Pipe15 Data Align Audit

- Gate 1: independent L1 rework candidate retained. The row models grouped
  latency alignment across a 15-bit pipelined converter readout.
- Gate 2: EVAS-ready, Cadence lint/Spectre pending. Public prompt now states
  the full interface, sample threshold, transition timing, and latency per bit
  group.
- Hidden coverage: repaired to use distinct per-bit stimulus patterns. The
  top-latency group now toggles at sampled edges so top-bit stuck faults are
  observable.
- Checker: upgraded from a few fixed stable samples to per-edge checks for all
  15 outputs against the public latency contract.
- Negatives: zero output, incorrect top-group delay, incorrect middle-group
  delay, and stuck top output are rejected by the behavior checker.
- Cadence/Spectre: not rerun in this branch because the local bridge readiness
  check reports bridge setup missing; this is a validation-environment block,
  not a known model failure.
