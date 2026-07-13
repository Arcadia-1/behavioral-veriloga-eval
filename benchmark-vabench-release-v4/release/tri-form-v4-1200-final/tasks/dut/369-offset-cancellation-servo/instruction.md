# Offset-cancellation Servo

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `offset_servo_top.va`: `offset_servo_top`
- `offset_sampler.va`: `offset_sampler`
- `trim_dac.va`: `trim_dac`
- `error_integrator.va`: `error_integrator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: On reset, clear trim code, corrected output, error metric, and done; when calibration is disabled, do not advance trim search state.
- `P_TRIM_SEARCH_DIRECTION`: Update the signed 5-bit trim code in the direction that reduces sampled differential error.
- `P_CORRECTED_RESIDUAL`: Drive corrected_out as the differential input minus the signed trim correction.
- `P_ERROR_METRIC`: Expose the current residual offset on error_metric after each enabled trim update.
- `P_DONE_QUALIFICATION`: Assert done only after four consecutive calibration updates with residual magnitude within error_tol.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `offset_servo_top.va`, `offset_sampler.va`, `trim_dac.va`, `error_integrator.va`.
Do not add or omit artifacts.
