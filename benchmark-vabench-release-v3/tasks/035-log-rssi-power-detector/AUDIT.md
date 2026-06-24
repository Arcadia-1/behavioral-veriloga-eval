# Honest SOP Audit: Task 035 Log RSSI Power Detector

## Scope

Task boundary is one Verilog-A DUT, `log_rssi_power_detector.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A log RSSI/power detector is a useful RF receiver behavioral macro.
- Reasonable task: pass. The public prompt fixes floor behavior, monotonic log-like response, compressed large-step behavior, metric output, and voltage-domain constraints.
- Complete tests: pass for EVAS. Hidden samples check floor, small/mid/high response, log-like monotonicity, compression of large input steps, and metric output. Five concrete negatives cover flat output, linear response, wrong floor, nonmonotonic response, and missing metric.
- Fair evaluation: pass for EVAS. The checker evaluates public RSSI transfer behavior with tolerant windows.

## Checker And Evidence

- Checker id: `v3_035_log_rssi_power_detector`
- Runner mapping: `CHECKS["v3_035_log_rssi_power_detector"] = check_log_rssi_power_detector`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
