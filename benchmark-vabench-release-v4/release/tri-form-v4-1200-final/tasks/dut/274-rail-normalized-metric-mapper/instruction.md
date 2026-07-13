# Rail Normalized Metric Mapper

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `rail_normalized_metric_mapper.va`: `rail_normalized_metric_mapper`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_NORMALIZE_MEAS_RELATIVE_TO_THE_LOCAL`: Normalize meas relative to the local V(vdd,vss) span and vss rail.
- `P_CLIP_THE_NORMALIZED_METRIC_TO_THE`: Clip the normalized metric to the public voltage-coded range.
- `P_ASSERT_VALID_ONLY_WHEN_ENABLE_IS`: Assert valid only when enable is high, supply span is valid, and the measurement lies inside the local rail window.
- `P_CLEAR_NORM_AND_VALID_WHILE_DISABLED`: Clear norm and valid while disabled or under the minimum supply span.
- `P_USE_LOCAL_ANALOG_HELPER_FUNCTIONS_RATHER`: Use local analog helper functions rather than user task/endtask syntax.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `rail_normalized_metric_mapper.va`.
Do not add or omit artifacts.
