# Mode Latch Calibration Gate Audit

- Gate 1: issue #109 numbered replacement row `420`. This row fills a remaining v3 numbering hole with a Spectre-compatible AMS-facing helper/monitor contract rather than restoring the archived unsupported language syntax.
- Gate 2: `cadence_modeling_ready` for the issue #109 remaining-hole slice. Public prompt exposes an observable voltage-domain behavior, hidden testbenches vary the stimulus away from visible timing, and five concrete negative variants target common shortcut implementations.
- Validation: EVAS gold/negative matrix passed for visible and hidden splits; EVAS AHDL-like lint reported zero diagnostics for solution gold; targeted Spectre gold validation passed for visible and hidden splits.
- Cadence reference correspondence: Cadence behavioral-modeling guidance emphasizes portable Verilog-A abstractions with explicit electrical observables, analog events where needed, and smoothed voltage-coded outputs. This row keeps that boundary by avoiding unsupported SystemVerilog/wreal/connect/specify/generate constructs.
