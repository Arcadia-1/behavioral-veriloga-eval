# Analog Mux Threshold

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `analog_mux_threshold.va`: `analog_mux_threshold`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_HIGH_SELECTS_VIN1`: When vsel is above vth, vout follows vin1 rather than vin2.
- `P_LOW_SELECTS_VIN2`: When vsel is at or below vth, vout follows vin2 rather than vin1.
- `P_BIDIRECTIONAL_SELECTION`: The selected input updates after both rising and falling crossings of vsel through vth.
- `P_INITIAL_SELECTION`: Before any select transition, vout is selected from the initial vsel level using the same strict-greater-than threshold rule.
- `P_NO_MIXING`: The output represents one selected input and does not average or sum vin1 and vin2.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `analog_mux_threshold.va`.
Do not add or omit artifacts.
