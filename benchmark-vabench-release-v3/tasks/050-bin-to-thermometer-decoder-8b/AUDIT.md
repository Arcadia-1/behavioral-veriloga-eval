# Task 050 Audit

Task: `050-bin-to-thermometer-decoder-8b`

## 2026-07 Testbench Utility Review

- Gate 1: retained as a meaningful support-formal converter utility. Binary-to-thermometer expansion is common in DAC arrays, element selection, and encoded stimulus/control paths, but the row should be counted under support/data-converter utility rather than as a standalone analog core.
- Gate 2: public prompt now states the vector Verilog-A interface, enable gating, unsigned 8-bit input code, cumulative low-to-high thermometer direction, boundary behavior, output levels, transition behavior, and voltage-only modeling constraints.
- Validation: the 24-row testbench-utility EVAS batch passed 24/24 gold cases and rejected 120/120 concrete negatives. Targeted Spectre gold coverage for this row passed. AHDL-like preflight produced only transition-on-voltage-coded-output warnings; no compatibility or linter failures were observed.
- Counting recommendation: keep as the representative thermometer-bus expansion row; task 020 should not be counted as an additional independent thermometer-function row.

Certification status: `cadence_modeling_ready` for support-formal scope.
