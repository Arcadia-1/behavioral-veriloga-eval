# Rail Normalized Metric Mapper Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `rail_normalized_metric_mapper.va`: `rail_normalized_metric_mapper`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_NORMALIZE_MEAS_RELATIVE_TO_THE_LOCAL`: Normalize meas relative to the local V(vdd,vss) span and vss rail.
- `P_CLIP_THE_NORMALIZED_METRIC_TO_THE`: Clip the normalized metric to the public voltage-coded range.
- `P_ASSERT_VALID_ONLY_WHEN_ENABLE_IS`: Assert valid only when enable is high, supply span is valid, and the measurement lies inside the local rail window.
- `P_CLEAR_NORM_AND_VALID_WHILE_DISABLED`: Clear norm and valid while disabled or under the minimum supply span.
- `P_USE_LOCAL_ANALOG_HELPER_FUNCTIONS_RATHER`: Use local analog helper functions rather than user task/endtask syntax.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `rail_normalized_metric_mapper.va`.
Every supplied `.va` file is editable; do not add or omit files.
