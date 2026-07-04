# Task 071 Audit

Task: `071-active-high-reset-synchronizer`

## 2026-07 Testbench Utility Review

- Gate 1: support utility only. The row is the active-high polarity variant of task 070 and should not be counted as an independent core function by name/polarity alone.
- Gate 2: public prompt now states active-high asynchronous assertion, synchronous release, two-stage behavior, thresholds, output levels, transition behavior, and voltage-domain constraints.
- Validation: the 24-row testbench-utility EVAS batch passed 24/24 gold cases and rejected 120/120 concrete negatives. Targeted Spectre gold coverage for this row passed. AHDL-like preflight reported no diagnostics for this row.
- Counting recommendation: keep as support-formal if reset polarity coverage is desired; under strict counting, choose one reset-synchronizer polarity or keep both as non-core support variants.

Certification status: `cadence_modeling_ready` for support-formal scope.
