# QTZ Differential 2level Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `qtz_differential_2level.va`: `qtz_differential_2level`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_SIGNED_CODE`: Initialize the signed output code to `-0.5`.
- `P_DIFFERENTIAL_MIDPOINT_DECISION`: On each rising `clk`, compare `vinp-vinn` with the midpoint between `vrefn` and `vrefp`.
- `P_BIPOLAR_TWO_LEVEL_OUTPUT`: Drive `dout` to the signed `+0.5` or `-0.5` level rather than a unipolar code.
- `P_CLOCKED_OUTPUT_HOLD`: Between rising clock decisions, hold the previous quantized output value.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `qtz_differential_2level.va`.
Every supplied `.va` file is editable; do not add or omit files.
