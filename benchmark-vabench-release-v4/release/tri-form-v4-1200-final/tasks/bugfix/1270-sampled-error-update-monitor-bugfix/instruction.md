# Sampled Error Update Monitor Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sampled_error_update_monitor.va`: `sampled_error_update_monitor`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_CLEARS_STATE_AND_OBSERVABLES`: While rst is high at a rising clock edge, clear the stable count, out, err_metric, and progress.
- `P_CORRECTED_OUTPUT_USES_SAMPLE_TARGET_AND_COEF`: At each enabled rising clock edge, compute the clipped coefficient and drive the clamped corrected sample from sample, target, and coef.
- `P_ERROR_METRIC_REPORTS_ABSOLUTE_ERROR`: Drive err_metric from the bounded absolute target-minus-sample error.
- `P_PROGRESS_COUNTS_CONSECUTIVE_IN_WINDOW_SAMPLES`: Increment progress only for consecutive in-window sampled errors, clear it on an out-of-window sample, and saturate at ready_count.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sampled_error_update_monitor.va`.
Every supplied `.va` file is editable; do not add or omit files.
