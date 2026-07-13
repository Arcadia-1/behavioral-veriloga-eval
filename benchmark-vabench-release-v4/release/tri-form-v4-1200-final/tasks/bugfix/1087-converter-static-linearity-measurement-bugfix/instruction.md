# Converter Static Linearity Measurement Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `converter_static_linearity_measurement_flow.va`: `converter_static_linearity_measurement_flow`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_STATE`: Active-high reset clears the retained conversion and previous-step state to the public reset values.
- `P_FOUR_BIT_QUANTIZATION`: On each non-reset rising clk edge, vin clips to 0 through vfs and quantizes monotonically to one of 16 codes represented as code_index times vfs/15.
- `P_PUBLIC_RECONSTRUCTION_TABLE`: For each code 0 through 15, recon equals the corresponding value in the public monotonic non-ideal reconstruction table, with default table voltages scaled by vfs/0.9 for legal vfs overrides.
- `P_INL_METRIC`: INL encodes reconstruction error from the vfs/15-per-code ideal ramp using the public gain and 0.05 V through 0.85 V clamp.
- `P_DNL_INCREASING_STEP`: For a valid increasing code step, dnl encodes actual reconstruction-step error relative to vfs/15 per code step with the public scaling and clamp.
- `P_DNL_NO_STEP_BASELINE`: Before a valid increasing step, or when code does not increase, dnl is held at the 0.45 V baseline.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `converter_static_linearity_measurement_flow.va`.
Every supplied `.va` file is editable; do not add or omit files.
