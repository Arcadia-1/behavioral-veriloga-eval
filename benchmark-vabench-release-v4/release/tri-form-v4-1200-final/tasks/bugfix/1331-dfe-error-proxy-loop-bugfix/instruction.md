# DFE Error-proxy Loop Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dfe_error_proxy_loop_top.va`: `dfe_error_proxy_loop_top`
- `decision_history.va`: `decision_history`
- `feedback_correction_core.va`: `feedback_correction_core`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear taps, corrected output, error metric, and `converged`.
- `P_ON_EACH_ENABLED_DECISION_CLOCK_LATCH`: On each enabled decision clock, latch the sign of `sample_in - vcm` as the current decision.
- `P_USE_THE_PREVIOUS_DECISION_HISTORY_TO`: Use the previous decision history to subtract a two-tap feedback estimate from the live sample.
- `P_EXPOSE_THE_ABSOLUTE_RESIDUAL_ON_ERROR`: Expose the absolute residual on `error_metric`.
- `P_ASSERT_CONVERGED_WHEN_THE_RESIDUAL_REMAINS`: Assert `converged` when the residual remains below `residual_tol` for three decisions.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dfe_error_proxy_loop_top.va`, `decision_history.va`, `feedback_correction_core.va`.
Every supplied `.va` file is editable; do not add or omit files.
