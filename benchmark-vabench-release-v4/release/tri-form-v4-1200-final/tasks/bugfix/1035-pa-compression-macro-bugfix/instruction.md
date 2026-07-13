# PA Compression Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pa_compression_macro.va`: `pa_compression_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_COMMON_MODE`: Initialization or active reset returns out to 0.45 V common mode and clears metric to 0 V.
- `P_CLOCKED_UPDATE`: Out and metric update from the sampled signed drive vin - 0.45 V on rising clk crossings and hold between updates.
- `P_LINEAR_REGION`: When 0.45 V + gain*(vin - 0.45 V) lies from 0.12 V through 0.78 V, out equals that target and metric is 0.1 V.
- `P_SYMMETRIC_COMPRESSION`: Targets above 0.78 V or below 0.12 V are compressed with slope 0.18 about the corresponding boundary, and metric is 0.85 V.
- `P_OUTPUT_CLAMP`: The compressed output remains within 0.02 V through 0.88 V with finite transition smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pa_compression_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.
