# DFE Error-proxy Loop

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dfe_error_proxy_loop_top.va`: `dfe_error_proxy_loop_top`
- `decision_history.va`: `decision_history`
- `feedback_correction_core.va`: `feedback_correction_core`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear taps, corrected output, error metric, and `converged`.
- `P_ON_EACH_ENABLED_DECISION_CLOCK_LATCH`: On each enabled decision clock, latch the sign of `sample_in - vcm` as the current decision.
- `P_USE_THE_PREVIOUS_DECISION_HISTORY_TO`: Use the previous decision history to subtract a two-tap feedback estimate from the live sample.
- `P_EXPOSE_THE_ABSOLUTE_RESIDUAL_ON_ERROR`: Expose the absolute residual on `error_metric`.
- `P_ASSERT_CONVERGED_WHEN_THE_RESIDUAL_REMAINS`: Assert `converged` when the residual remains below `residual_tol` for three decisions.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dfe_error_proxy_loop_top.va`, `decision_history.va`, `feedback_correction_core.va`.
Do not add or omit artifacts.
