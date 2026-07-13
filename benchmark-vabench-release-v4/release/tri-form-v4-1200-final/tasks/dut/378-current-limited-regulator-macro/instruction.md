# Current-limited Regulator Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `current_limited_regulator_macro.va`: `current_limited_regulator_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation drives vout, limit_metric, and regulation_ok low.
- `P_NORMAL_REGULATION`: With adequate headroom and sub-limit demand, vout equals vref and regulation_ok is asserted.
- `P_DROPOUT_CLAMP`: When input headroom is insufficient, vout is clamped to max(vss, vin minus dropout).
- `P_CURRENT_LIMITING`: Demand above demand_limit produces limit_metric equal to the overload and reduces vout by that overload subject to rails and dropout.
- `P_REGULATION_FLAG`: regulation_ok is high only for enabled, non-reset, non-limited operation with enough input headroom.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `current_limited_regulator_macro.va`.
Do not add or omit artifacts.
