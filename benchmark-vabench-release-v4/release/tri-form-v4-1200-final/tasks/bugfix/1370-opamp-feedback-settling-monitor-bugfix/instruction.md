# Op-amp Feedback Settling Monitor Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `opamp_feedback_settling.va`: `opamp_feedback_settling`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_ENABLE_IS`: On reset or when `enable` is low, drive `vout` to `vcm`, clear `error_metric`, and clear `settled`.
- `P_DECODE_GAIN_2_GAIN_0_INTO`: Decode `gain_2..gain_0` into a closed-loop target gain of at least unity.
- `P_UPDATE_VOUT_ONCE_PER_RISING_CLK`: Update `vout` once per rising `clk` edge toward the target closed-loop output using `alpha`.
- `P_CLAMP_VOUT_TO_THE_RANGE_VSS`: Clamp `vout` to the range `vss` through `vdd`.
- `P_ERROR_METRIC_MUST_EXPOSE_THE_SIGNED`: `error_metric` must expose the signed difference between the current output and the target closed-loop value.
- `P_ASSERT_SETTLED_AFTER_THREE_CONSECUTIVE_UPDATES`: Assert `settled` after three consecutive updates where the absolute error is below `settle_tol`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `opamp_feedback_settling.va`.
Every supplied `.va` file is editable; do not add or omit files.
