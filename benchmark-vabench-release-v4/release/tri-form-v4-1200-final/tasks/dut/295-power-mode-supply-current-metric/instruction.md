# Power Mode Supply Current Metric

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `power_mode_supply_current_metric.va`: `power_mode_supply_current_metric`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DRIVE_ISUP_METRIC_AS_A_VOLTAGE`: Drive `isup_metric` as a voltage-coded supply-current estimate. The estimate must scale with the local supply ratio `V(vdd, vss) / vnom` clipped to the range `[0, 1.5]`. Normalize load as `V(load, vss) / vhi` clipped to `[0, 1]`. When the block is disabled or powered down, meaning `V(en) <= vth` or `V(pd) > vth`, drive `isup_metric = ipd * supply_scale`. Otherwise choose the active base metric as `iq1` when `V(mode) > vth` and `iq0` when `V(mode) <= vth`, then drive `isup_metric = (base_metric + load_gain * load_norm) * supply_scale`. The metric is not a real branch current; it is an observable behavioral macro-model output.
- `P_BUILD_A_VOLTAGE_DOMAIN_BIAS_REFERENCE`: Build a voltage-domain bias/reference/power-management macro-model metric. The module exposes an observable supply-current demand estimate as a voltage-coded output across enable, power-down, operating mode, load demand, and local supply conditions.
- `P_VTH_0_45_V_LOGIC_THRESHOLD`: `vth = 0.45 V`: logic threshold for `en`, `pd`, and `mode`.
- `P_VHI_0_9_V_FULL_SCALE`: `vhi = 0.9 V`: full-scale input level for `load`.
- `P_VNOM_0_9_V_NOMINAL_SUPPLY`: `vnom = 0.9 V`: nominal supply used for supply-ratio scaling.
- `P_IQ0_0_08_IQ1_0_14`: `iq0 = 0.08`, `iq1 = 0.14`: active quiescent metric levels for low and high

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `power_mode_supply_current_metric.va`.
Do not add or omit artifacts.
