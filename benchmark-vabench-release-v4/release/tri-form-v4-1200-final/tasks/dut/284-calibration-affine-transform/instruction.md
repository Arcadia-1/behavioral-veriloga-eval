# Calibration Affine Transform

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `calibration_affine_transform.va`: `calibration_affine_transform`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_EACH_RISING_CLOCK_CROSSING_COMPUTE`: On each rising clock crossing, compute a local affine calibration transform from raw, gain_ctrl, and offset_ctrl while reset is low and enable is high.
- `P_MAP_GAIN_CTRL_TO_A_PUBLIC`: Map gain_ctrl to a public gain range and offset_ctrl to a centered offset.
- `P_CLEAR_OUTPUT_AND_METRIC_WHILE_RESET`: Clear output and metric while reset is high or enable is low; otherwise clip the transformed output into the public voltage-coded range.
- `P_EXPOSE_A_BOUNDED_RESIDUAL_METRIC_FOR`: Expose a bounded residual metric for the transform magnitude.
- `P_USE_LOCAL_ANALOG_HELPER_FUNCTIONS_RATHER`: Use local analog helper functions rather than user task/endtask syntax.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `calibration_affine_transform.va`.
Do not add or omit artifacts.
