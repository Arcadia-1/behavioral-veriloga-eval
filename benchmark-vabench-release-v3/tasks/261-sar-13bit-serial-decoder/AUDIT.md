# SAR 13bit Serial Decoder Audit

- Gate 1: independent L1 rework candidate retained. The row models an
  MSB-first serial SAR decision decoder with frame publication and high-decision
  count monitoring.
- Gate 2: EVAS-ready, Cadence lint/Spectre pending. Public prompt now states
  interface, ready/clock semantics, bit order, bipolar normalization, and reset
  after publication.
- Hidden coverage: repaired to use distinct frame timing and serial data
  pattern from the visible smoke deck.
- Checker: upgraded from fixed samples to event-derived ready-bit accumulation,
  `dnum` count checks, and `clks` frame publication checks.
- Negatives: zero output, counting low decisions, wrong initial counter, and
  unipolar result variants are rejected by the behavior checker.
- Cadence/Spectre: not rerun in this branch because the local bridge readiness
  check reports bridge setup missing; this is a validation-environment block,
  not a known model failure.
