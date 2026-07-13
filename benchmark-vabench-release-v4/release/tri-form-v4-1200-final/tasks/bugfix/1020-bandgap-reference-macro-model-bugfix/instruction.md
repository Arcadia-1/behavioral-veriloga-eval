# Bandgap Reference Macro Model Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `bandgap_reference_macro_model.va`: `bandgap_reference_macro_model`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_AND_BROWNOUT`: Reset or vin below vstart forces out and metric to 0 V.
- `P_CLOCKED_FIRST_ORDER_SETTLING`: On eligible rising clock crossings, the held reference advances by 0.35 of the remaining error to the clamped line-corrected target.
- `P_TARGET_AND_OUTPUT_CLAMPS`: The line-corrected target is clamped to 0 through vin minus 0.05 V, and driven out remains within 0 through 0.9 V.
- `P_VALIDITY_ENCODING`: Metric is 0 V in reset or brownout, 0.2 V during startup below the 0.48 V validity threshold, and 0.9 V after the held reference exceeds it.
- `P_CLOCKED_HOLD`: Above startup, the reference state changes only on rising clock crossings and holds between samples.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `bandgap_reference_macro_model.va`.
Every supplied `.va` file is editable; do not add or omit files.
