# Slew Rate DAC4 Audit

- Gate 1: `valid_variant_needs_counting_policy` as materialized replacement
  candidate. This row adds a Cadence-style slew-rate-limited DAC behavior,
  distinct from ideal transition-smoothed DAC rows because output slew is part
  of the circuit contract. It should not be counted as an appended `495`
  benchmark row; if accepted, upstream should assign it to a replacement slot in
  the original `001`-`300` surface.
- Gate 2: behavior-certified in the staging layer. Public prompt exposes bit
  order, threshold, endpoint mapping, and `slew()` rate limiting without
  leaking checker sample windows. Re-run Spectre/AHDL evidence after any final
  renumbering or replacement-slot edit.
- Cadence reference correspondence: Cadence Analog Modeling with Verilog-A lab
  material models a DAC by thresholding voltage-coded input bits, accumulating
  binary weights, and driving the analog output through `slew()`.
