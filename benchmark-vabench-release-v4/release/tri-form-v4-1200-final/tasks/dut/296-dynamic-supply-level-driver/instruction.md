# Dynamic Supply Level Driver

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dynamic_supply_level_driver.va`: `dynamic_supply_level_driver`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_MODEL_A_DYNAMIC_SUPPLY_ELECTRICAL_LEVEL`: Model a dynamic-supply electrical level driver. Compute the input level relative to the local rails, not global ground. When `V(vdd, vss)` is at least `vsup_min`, drive `out` to the local low or high rail-derived level according to whether the normalized input exceeds `vth_frac`. When the supply is below `vsup_min`, drive `out` to the local low level. Smooth the output with `transition()`.
- `P_BUILD_A_DYNAMIC_SUPPLY_VOLTAGE_DOMAIN`: Build a dynamic-supply voltage-domain level driver. The module thresholds its input relative to local supply rails, drives its output relative to those same rails, and falls back to the local low level when the supply is invalid.
- `P_VSUP_MIN_0_55_V_MINIMUM`: `vsup_min = 0.55 V`: minimum `V(vdd, vss)` required for normal operation.
- `P_VTH_FRAC_0_5_INPUT_THRESHOLD`: `vth_frac = 0.5`: input threshold expressed as a fraction of the local supply
- `P_VLO_FRAC_0_0_VHI_FRAC`: `vlo_frac = 0.0`, `vhi_frac = 1.0`: output low and high levels expressed as
- `P_TR_40P_OUTPUT_TRANSITION_SMOOTHING_TIME`: `tr = 40p`: output transition smoothing time.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dynamic_supply_level_driver.va`.
Do not add or omit artifacts.
