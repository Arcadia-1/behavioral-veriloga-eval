# Calibration Affine Transform Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `calibration_affine_transform.va`: `calibration_affine_transform`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_EACH_RISING_CLOCK_CROSSING_COMPUTE`: On each rising clock crossing, compute a local affine calibration transform from raw, gain_ctrl, and offset_ctrl while reset is low and enable is high.
- `P_MAP_GAIN_CTRL_TO_A_PUBLIC`: Map gain_ctrl to a public gain range and offset_ctrl to a centered offset.
- `P_CLEAR_OUTPUT_AND_METRIC_WHILE_RESET`: Clear output and metric while reset is high or enable is low; otherwise clip the transformed output into the public voltage-coded range.
- `P_EXPOSE_A_BOUNDED_RESIDUAL_METRIC_FOR`: Expose a bounded residual metric for the transform magnitude.
- `P_USE_LOCAL_ANALOG_HELPER_FUNCTIONS_RATHER`: Use local analog helper functions rather than user task/endtask syntax.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `calibration_affine_transform.va`.
Every supplied `.va` file is editable; do not add or omit files.
