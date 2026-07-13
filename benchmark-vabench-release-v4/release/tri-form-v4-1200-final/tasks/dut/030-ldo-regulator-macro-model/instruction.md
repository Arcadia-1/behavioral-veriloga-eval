# LDO Regulator Macro Model

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ldo_regulator_macro_model.va`: `ldo_regulator_macro_model`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_AND_RESET_STATE`: Initialization or active-high reset sets out to 0.60 V and metric to 0.9 V.
- `P_LOAD_TARGET`: At each eligible rising clock crossing, vin is clamped to 0 through 0.9 V and target equals 0.62 V minus 0.055 times that load.
- `P_FIRST_ORDER_REGULATION`: Out advances by 0.35 of the remaining target error on each eligible rising clock crossing.
- `P_REGULATED_OUTPUT_CLAMP`: The held output remains within 0.25 V through 0.75 V.
- `P_ERROR_METRIC`: Metric equals 0.9 V minus four times the absolute output-to-target error, clamped to 0 through 0.9 V.
- `P_CLOCKED_HOLD`: Out and metric hold between rising clock crossings except for transition smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ldo_regulator_macro_model.va`.
Do not add or omit artifacts.
