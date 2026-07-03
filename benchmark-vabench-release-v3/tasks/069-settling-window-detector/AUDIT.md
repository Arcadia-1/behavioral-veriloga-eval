# Task 069 Audit

Task: `069-settling-window-detector`

## 2026-07 Testbench Utility Review

- Gate 1: retained as a measurement/instrumentation support component. It checks continuous settling inside a tolerance window and reports a quantized entry-time code, which is a real AMS validation helper.
- Gate 2: public prompt now states tolerance-window qualification, continuous hold time, reset-on-exit behavior, entry-time code scaling, bit order, thresholds, output levels, transition behavior, and voltage-domain constraints.
- Validation: the 24-row testbench-utility EVAS batch passed 24/24 gold cases and rejected 120/120 concrete negatives. Targeted Spectre gold coverage for this row passed after checker calibration. AHDL-like preflight produced one transition-related warning per deck; no compatibility or linter failures were observed.
- Checker note: Spectre adaptive transient output can place the nearest saved row slightly past a requested sample time. The checker now uses the requested sample time for region classification while still reading output voltages from the nearest row, preventing a boundary-only false failure without relaxing the DUT contract.
- Counting recommendation: keep as support/measurement utility; it has stronger AMS relevance than pure digital helpers.

Certification status: `cadence_modeling_ready` for support-formal scope.
