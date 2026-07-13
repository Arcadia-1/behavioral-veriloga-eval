# Sampled Error Update Monitor

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sampled_error_update_monitor.va`: `sampled_error_update_monitor`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_CLEARS_STATE_AND_OBSERVABLES`: While rst is high at a rising clock edge, clear the stable count, out, err_metric, and progress.
- `P_CORRECTED_OUTPUT_USES_SAMPLE_TARGET_AND_COEF`: At each enabled rising clock edge, compute the clipped coefficient and drive the clamped corrected sample from sample, target, and coef.
- `P_ERROR_METRIC_REPORTS_ABSOLUTE_ERROR`: Drive err_metric from the bounded absolute target-minus-sample error.
- `P_PROGRESS_COUNTS_CONSECUTIVE_IN_WINDOW_SAMPLES`: Increment progress only for consecutive in-window sampled errors, clear it on an out-of-window sample, and saturate at ready_count.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sampled_error_update_monitor.va`.
Do not add or omit artifacts.
