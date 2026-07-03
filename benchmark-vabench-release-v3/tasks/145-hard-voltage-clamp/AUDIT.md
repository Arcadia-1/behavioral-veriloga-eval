# Hard Voltage Clamp Audit

- Gate 1: `independent_l1_ready`. This is a hard ground-referenced voltage
  clamp with overridable clamp rails; it is distinct from supply-headroom
  limiter rows and from the soft exponential clamp in `158-soft-voltage-clamp`.
- Gate 2: `cadence_modeling_ready` after this revision's targeted
  EVAS/negative, Spectre, and AHDL-lint validation. The reference
  implementation computes the clamp target first and contributes once to avoid
  branch-switched voltage contributions.
- AHDL triage: EVAS AHDL-like lint reports zero diagnostics, and Spectre
  read-in reports no task-level AHDL errors; remaining notices are global setup
  notices.
- Public contract: use `vgnd` as the reference, pass through inside the rail
  interval, clamp below the lower rail, and clamp above the upper rail.
- Coverage: validation samples exercise lower clamp, pass-through, upper clamp, and
  return to pass-through; five behavior negatives reject zero, missing lower
  clamp, missing upper clamp, swapped rails, and scaling implementations.
