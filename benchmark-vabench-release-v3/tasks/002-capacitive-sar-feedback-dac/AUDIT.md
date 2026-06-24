# Honest SOP Audit: Task 002 Capacitive SAR Feedback DAC

## Scope

Task boundary is one Verilog-A DUT, `cdac_cal.va`, plus Spectre-compatible `.scs` testbenches.

## Four Standards

- Useful scenario: a calibrated capacitive feedback DAC is a common SAR ADC behavioral primitive.
- Reasonable task: the public prompt states the exact port order, rising-clock sampling rule, 10-bit binary weighting, redundant calibration code, 0.45 V common-mode, and differential voltage formula.
- Complete tests: visible `.scs` checks basic code movement and calibration visibility; hidden `.scs` covers zero, individual bit weights, mixed large codes, all calibration states, polarity, and common-mode behavior across a 68 ns sequence.
- Fair evaluation: checker should derive expected `VDAC_P` and `VDAC_N` only from the public formula and the saved input/output traces. Concrete negatives preserve the interface but fail the required behavior.

Certification status: certified as an EVAS formal candidate on 2026-06-24. Gold PASS; 5/5 concrete negatives compile and fail with `FAIL_SIM_CORRECTNESS` under `v3_002_capacitive_weighted_sar_feedback_dac`.
