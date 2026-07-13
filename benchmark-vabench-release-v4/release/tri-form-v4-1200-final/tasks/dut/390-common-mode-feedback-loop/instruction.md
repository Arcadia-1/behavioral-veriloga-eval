# Common-mode Feedback Loop

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cmfb_loop_top.va`: `cmfb_loop_top`
- `cm_sensor.va`: `cm_sensor`
- `trim_controller.va`: `trim_controller`
- `output_balancer.va`: `output_balancer`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or disable clears trim and lock, reports zero residual error, and bypasses correction.
- `P_COMMON_MODE_ERROR`: The reported common-mode error equals the corrected output average minus vcm.
- `P_TRIM_DIRECTION`: At enabled rising clock edges the bounded unsigned trim code moves in the direction that reduces representable positive common-mode error.
- `P_DIFFERENTIAL_PRESERVATION`: Common-mode correction preserves input differential polarity and differential magnitude unless a supply clamp is reached.
- `P_LOCK_QUALIFICATION`: Lock asserts only after two consecutive enabled updates within lock_tol.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cmfb_loop_top.va`, `cm_sensor.va`, `trim_controller.va`, `output_balancer.va`.
Do not add or omit artifacts.
