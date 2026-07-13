# Differential Common Mode Window Monitor

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `differential_common_mode_window_monitor.va`: `differential_common_mode_window_monitor`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CONTINUOUSLY_COMPUTE_VDIFF_V_VIP_V`: Continuously compute `vdiff = V(vip) - V(vin)` and `vcm = 0.5 * (V(vip) + V(vin))`. Drive `diff_ok` high only while `en` is high and `abs(vdiff)` is no larger than `diff_max`. Drive `cm_ok` high only while `en` is high and `abs(vcm - V(vcm_ref))` is no larger than `cm_tol`. Drive `valid` high only when both `diff_ok` and `cm_ok` would be high. Drive `diff_metric` as `vhi * clip(abs(vdiff) / diff_fullscale, 0, 1)` and `cm_metric` as `vhi * clip(abs(vcm - V(vcm_ref)) / cm_fullscale, 0, 1)`. Smooth the voltage-coded Boolean outputs with `transition()`.
- `P_BUILD_A_VOLTAGE_DOMAIN_INPUT_VALIDITY`: Build a voltage-domain input-validity monitor for a differential analog front-end. The module checks whether the differential input magnitude remains inside a public linear range, whether the instantaneous common-mode level stays near a reference, and whether the enabled input pair is valid for downstream behavioral processing.
- `P_VTH_0_45_V_LOGIC_THRESHOLD`: `vth = 0.45 V`: logic threshold for `en`.
- `P_VHI_0_9_V_HIGH_LEVEL`: `vhi = 0.9 V`: high level for voltage-coded outputs.
- `P_DIFF_MAX_0_30_V_MAXIMUM`: `diff_max = 0.30 V`: maximum allowed `abs(V(vip) - V(vin))`.
- `P_DIFF_FULLSCALE_0_45_V_FULL`: `diff_fullscale = 0.45 V`: full-scale value for `diff_metric`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `differential_common_mode_window_monitor.va`.
Do not add or omit artifacts.
