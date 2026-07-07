# Voltage Match Window Audit

- Gate 1: `independent_l1_ready`.
- Duplicate resolution: this row was rewritten from pure voltage-coded XNOR logic into an analog voltage-coincidence detector, so the behavior now depends on absolute analog voltage difference rather than Boolean threshold equality.
- Cadence/VA modeling rationale: voltage-domain monitor/helper models are useful in calibration, lock-detect, and mixed-signal decision flows when they expose an analog tolerance window and a rail-coded status output.
- Public contract: `voltage_match_window(vin1, vin2, vout)` with public `match_tol = 0.05 V`, `vh = 0.9 V`, and `tr = 20 ps`; output is high when `abs(V(vin1)-V(vin2)) <= match_tol`.
- Checker alignment: checker requires both within-window and outside-window coverage and rejects thresholded logic substitutes.
- Validation status: fresh local EVAS2 gold/negative, Spectre visible/hidden gold, Spectre hidden negative, and EVAS AHDL-like preflight validation completed after this rewrite. Generated evidence reports are intentionally not committed.
