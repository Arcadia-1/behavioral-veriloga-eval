# Slew Rate DAC4 Audit

- Gate 1: `independent_l1_ready` as an issue #109 re-slot. This row adds a
  Cadence-style slew-rate-limited DAC behavior, distinct from ideal
  transition-smoothed DAC rows because output slew is part of the circuit
  contract.
- Gate 2: `cadence_modeling_ready`. Public prompt exposes bit order, threshold,
  endpoint mapping, and `slew()` rate limiting without leaking checker sample
  windows. Post-re-slot validation passes EVAS hidden gold and rejects all five
  EVAS hidden negative variants. Spectre bridge validation passes visible and
  hidden gold, and hidden Spectre negatives reject all five variants. AHDL log
  triage found no task-level AHDL compile errors; only shared setup warnings
  such as `VACOMP-2435` and `SPECTRE-592` appear.
- Cadence reference correspondence: Cadence Analog Modeling with Verilog-A lab
  material models a DAC by thresholding voltage-coded input bits, accumulating
  binary weights, and driving the analog output through `slew()`.
