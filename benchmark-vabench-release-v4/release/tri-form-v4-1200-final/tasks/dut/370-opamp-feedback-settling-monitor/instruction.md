# Op-amp Feedback Settling Monitor

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `opamp_feedback_settling.va`: `opamp_feedback_settling`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_ENABLE_IS`: On reset or when `enable` is low, drive `vout` to `vcm`, clear `error_metric`, and clear `settled`.
- `P_DECODE_GAIN_2_GAIN_0_INTO`: Decode `gain_2..gain_0` into a closed-loop target gain of at least unity.
- `P_UPDATE_VOUT_ONCE_PER_RISING_CLK`: Update `vout` once per rising `clk` edge toward the target closed-loop output using `alpha`.
- `P_CLAMP_VOUT_TO_THE_RANGE_VSS`: Clamp `vout` to the range `vss` through `vdd`.
- `P_ERROR_METRIC_MUST_EXPOSE_THE_SIGNED`: `error_metric` must expose the signed difference between the current output and the target closed-loop value.
- `P_ASSERT_SETTLED_AFTER_THREE_CONSECUTIVE_UPDATES`: Assert `settled` after three consecutive updates where the absolute error is below `settle_tol`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `opamp_feedback_settling.va`.
Do not add or omit artifacts.
