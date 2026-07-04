# Task 070 Audit

Task: `070-active-low-reset-synchronizer`

## 2026-07 Testbench Utility Review

- Gate 1: support utility only. The row is useful for clocked AMS control wrappers, but as written it is a reset-polarity synchronizer primitive and overlaps task 071.
- Gate 2: public prompt now states active-low asynchronous assertion, synchronous release, two-stage behavior, thresholds, output levels, transition behavior, and voltage-domain constraints.
- Validation: the 24-row testbench-utility EVAS batch passed 24/24 gold cases and rejected 120/120 concrete negatives. Targeted Spectre gold coverage for this row passed. AHDL-like preflight reported no diagnostics for this row.
- Counting recommendation: keep as support-formal if reset polarity coverage is desired; do not count both 070 and 071 as independent core AMS functions under strict de-duplication.

Certification status: `cadence_modeling_ready` for support-formal scope.
