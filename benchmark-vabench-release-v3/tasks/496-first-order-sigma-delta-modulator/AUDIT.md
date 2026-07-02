# First Order Sigma Delta Modulator Audit

- Gate 1: `valid_variant_needs_counting_policy` as materialized replacement
  candidate. A first-order sigma-delta modulator is a converter architecture,
  not a weighted DAC/ADC variant, and is a strong backfill candidate for a
  duplicate or weak converter row. It should not be counted as an appended `496`
  benchmark row; if accepted, upstream should assign it to a replacement slot in
  the original `001`-`300` surface.
- Gate 2: behavior-certified in the staging layer. Public prompt exposes clock
  edge, normalized input/reference, feedback semantics, output logic level, and
  transition timing. Re-run Spectre/AHDL evidence after any final renumbering or
  replacement-slot edit.
- Cadence reference correspondence: Cadence Verilog-A Language Reference 25.1
  includes a first-order sigma-delta converter model with analog input, clock,
  one-bit output, threshold, output level, and transition timing parameters.
