# Audit: Param Given Gain Select

- Task id: `v3_464_param_given_gain_select`
- Category: `veriloga_environment_function_semantics`
- Required syntax focus: `Use $param_given() to choose behavior based on parameter override presence.`
- EVAS status: `gold PASS and 5/5 negative variants rejected by EVAS2 behavior checker`
- Former blocking issue: `https://github.com/Arcadia-1/EVAS/issues/49`

## Current Review Status

- Counting label: L0/support Verilog-A environment-function semantic row.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation failures in the current S3 environment-helper batch.
- Acceptance basis: EVAS tracks explicit Spectre instance parameter names separately from default parameter values, so `$param_given(gain)` returns 0 for the default instance and 1 for the instance with `gain=0.5`.
