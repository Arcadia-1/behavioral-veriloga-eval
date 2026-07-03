# Task 045 Audit

Task: `045-soft-hysteretic-limiter`

Status: `independent_l1_ready`. Gate 2 status is
`cadence_modeling_ready` for the reviewed gold after EVAS, targeted Spectre,
and AHDL warning triage.

## Gate 1

- Function boundary: baseband soft limiter with hysteresis memory and a
  voltage-coded state monitor.
- Counting decision: keep as an independent L1 signal-conditioning primitive.
  It is distinct from plain limiting/gain rows because the required state
  memory preserves high/low history through mid-level intervals.
- Category relation: complements gain-compression and limiting-differential
  rows, but the hysteretic memory behavior is the independent circuit function.

## Gate 2

- Public prompt: rewritten into the standard public interface, parameter
  contract, functional contract, and modeling constraints format.
- Boundary: the visible testbench is treated as a public wiring/smoke scenario;
  transient stop time and waveform windows are not DUT implementation
  constants.
- Gold behavior: uses event-updated state on rising clock crossings, active-high
  reset, bounded output compression, preserved high/low hysteresis, and
  transition-smoothed voltage contributions.
- Checker behavior: verifies bounded high/low limiting, visible hysteresis
  memory, state-coded metric polarity, and metric span.
- Reference correspondence: local Cadence/Verilog-A notes for event detection
  and transition-shaped piecewise-constant outputs support the modeling pattern;
  no direct Cadence RF/baseband soft-limiter example was found in the targeted
  sweep.

## Evidence

- EVAS hidden gold: PASS.
- Concrete negatives: 5/5 rejected with behavioral failures.
- Visible smoke: PASS after saving all public observables.
- Targeted Spectre hidden gold: PASS.
- AHDL lint/read-in triage: EVAS AHDL-like lint reports zero diagnostics for
  the hidden solution deck and visible starter smoke deck. Spectre read-in
  reports no task-specific AHDL lint, AHDL compile, or VACOMP errors.

## Residual Risk

- The checker validates a deterministic transient voltage-domain macromodel. It
  does not claim transistor-level limiter accuracy, noise behavior, or RF/PSS
  readiness.
