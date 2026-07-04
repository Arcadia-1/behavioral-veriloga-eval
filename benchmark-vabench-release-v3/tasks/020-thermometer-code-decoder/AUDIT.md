# Task 020 Audit

Task: `020-thermometer-code-decoder`

## 2026-07 Testbench Utility Review

- Gate 1: support utility, not an independent core AMS benchmark as written. The guarded two-bit thermometer decoder is useful as a small converter/helper primitive, but it overlaps the broader 8-bit thermometer decoder coverage in task 050.
- Gate 2: public prompt now uses the mandatory vaBench v3 instruction shape and states module boundary, thresholding, enable behavior, invalid-code guarding, bit order, and voltage-domain constraints.
- Validation: the 24-row testbench-utility EVAS batch passed 24/24 gold cases and rejected 120/120 concrete negatives. Targeted Spectre gold coverage for this row passed. AHDL-like preflight reported no diagnostics for this row.
- Counting recommendation: keep as a support-formal candidate or small smoke utility; do not count separately as a representative data-converter function when task 050 is counted.

Certification status: `cadence_modeling_ready` for support-formal scope.
