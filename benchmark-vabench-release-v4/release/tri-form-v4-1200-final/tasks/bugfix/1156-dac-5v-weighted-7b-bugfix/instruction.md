# DAC 5V Weighted 7b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dac_5v_weighted_7b.va`: `dac_5v_weighted_7b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLOCKED_SEVEN_BIT_WEIGHTED_SUM`: Each rising `clks` crossing samples `din0` through `din6` into the declared seven-bit weighted DAC sum.
- `P_MSB_AND_TERMINATION_CONTRIBUTIONS`: `din0` contributes the largest switched weight and the fixed termination contribution is included.
- `P_REFERENCE_ENDPOINTS_AND_SCALE`: The output uses the declared `refp` and `refn` endpoints and full DAC scale.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dac_5v_weighted_7b.va`.
Every supplied `.va` file is editable; do not add or omit files.
