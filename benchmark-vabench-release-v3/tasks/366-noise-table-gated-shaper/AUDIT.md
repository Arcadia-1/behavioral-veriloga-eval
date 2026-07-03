# Audit: Noise Table Gated Shaper

## Gate 1

This row is a support/L0 Verilog-A semantics task for threshold-gating a voltage-domain `noise_table()` source using a supplied table file. It is useful for simulator compatibility and modeling coverage, but it should not be counted as an independent core circuit-function benchmark without a dedicated noise-analysis flow.

## Gate 2

The public prompt defines the module interface, public parameters, exact support table filename, gate condition, direct branch contribution form, and deterministic transient-observable `metric` sideband. The modeling contract keeps `noise_table()` in a voltage branch contribution and keeps the table dependency explicit.

## Validation

2026-07-04 batch validation for rows 361-372: EVAS2 reference runs passed 12/12; EVAS2 negative variants were rejected 60/60; Spectre reference runs passed 12/12; Spectre negative variants were rejected 60/60. Spectre read-in logs showed no task-specific `AHDLLINT-*`, `VACOMP-1116`, or AHDL compile errors; the remaining `VACOMP-2435` notice is a shared environment warning. EVAS AHDL-like lint reports zero diagnostics for the starter rows; solution rows with conditional noise, AC, or analysis branch contributions have static W5008/W5010 warnings that are triaged as acceptable for this support/L0 semantics surface.

## Status

Support semantics row. Spectral noise-table behavior is intentionally not claimed by this transient-oriented task.
