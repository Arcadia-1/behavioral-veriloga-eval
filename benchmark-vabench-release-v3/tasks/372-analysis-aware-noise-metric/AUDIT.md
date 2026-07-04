# Audit: Analysis Aware Noise Metric

## Gate 1

This row is a support/L0 Verilog-A semantics task for combining `analysis("noise")`, a voltage-domain `white_noise()` contribution, and a deterministic sampled metric. It is useful for simulator compatibility and modeling coverage, but it should not be counted as an independent core circuit-function benchmark without a dedicated noise-analysis flow.

## Gate 2

The public prompt defines the module interface, public parameters, transient `V(ctrl)` output, noise-analysis guard, and clock-count metric. The reference source drives continuous `V(ctrl)` behavior directly as a branch contribution instead of passing it through `transition()`, avoiding the Cadence AHDL lint risk for transition filters on continuous signals.

## Validation

2026-07-04 batch validation for rows 361-372: EVAS2 reference runs passed 12/12; EVAS2 negative variants were rejected 60/60; Spectre reference runs passed 12/12; Spectre negative variants were rejected 60/60. Spectre read-in logs showed no task-specific `AHDLLINT-*`, `VACOMP-1116`, or AHDL compile errors; the remaining `VACOMP-2435` notice is a shared environment warning. EVAS AHDL-like lint reports zero diagnostics for the starter rows; solution rows with conditional noise, AC, or analysis branch contributions have static W5008/W5010 warnings that are triaged as acceptable for this support/L0 semantics surface.

## Status

Support semantics row. Spectral noise behavior is intentionally not claimed by this transient-oriented task.
