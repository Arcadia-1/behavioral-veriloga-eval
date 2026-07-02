# Slew Rate DAC4 Audit

- Gate 1: `independent_l1_ready` candidate. This row adds a Cadence-style
  slew-rate-limited DAC behavior, distinct from ideal transition-smoothed DAC
  rows because output slew is part of the circuit contract.
- Gate 2: `cadence_sim_pending` until fresh Spectre/AHDL evidence is attached.
  Public prompt exposes bit order, threshold, endpoint mapping, and `slew()`
  rate limiting without leaking checker sample windows.
- Cadence reference correspondence: Cadence Analog Modeling with Verilog-A lab
  material models a DAC by thresholding voltage-coded input bits, accumulating
  binary weights, and driving the analog output through `slew()`.
