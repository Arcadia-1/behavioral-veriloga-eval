# Offset-cancellation Servo Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `offset_servo_top.va`: `offset_servo_top`
- `offset_sampler.va`: `offset_sampler`
- `trim_dac.va`: `trim_dac`
- `error_integrator.va`: `error_integrator`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: On reset, clear trim code, corrected output, error metric, and done; when calibration is disabled, do not advance trim search state.
- `P_TRIM_SEARCH_DIRECTION`: Update the signed 5-bit trim code in the direction that reduces sampled differential error.
- `P_CORRECTED_RESIDUAL`: Drive corrected_out as the differential input minus the signed trim correction.
- `P_ERROR_METRIC`: Expose the current residual offset on error_metric after each enabled trim update.
- `P_DONE_QUALIFICATION`: Assert done only after four consecutive calibration updates with residual magnitude within error_tol.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `offset_servo_top.va`, `offset_sampler.va`, `trim_dac.va`, `error_integrator.va`.
Every supplied `.va` file is editable; do not add or omit files.
