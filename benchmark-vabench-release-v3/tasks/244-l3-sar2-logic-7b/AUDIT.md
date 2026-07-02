# L3 SAR2 Logic 7b Audit

- Gate 1: independent L1 rework candidate retained. The row models a
  converter-facing SAR2 controller with active-low comparator pulses, `cmpck`,
  final code bits, and CDAC control outputs.
- Gate 2: EVAS-ready, Cadence lint/Spectre pending. Public prompt now states
  interface, logic levels, reset/start behavior, active-low decision semantics,
  and final publication behavior.
- Hidden coverage: repaired to use a distinct active-low decision sequence and
  conversion timing relative to the visible smoke deck.
- Checker: upgraded from fixed samples to event-derived active-low decision,
  final-code, `sp`/`sn`, and `cmpck` checks.
- Negatives: zero output, inverted decision, no step decrement, and half-level
  `cmpck` variants are rejected by the behavior checker.
- Cadence/Spectre: not rerun in this branch because the local bridge readiness
  check reports bridge setup missing; this is a validation-environment block,
  not a known model failure.
