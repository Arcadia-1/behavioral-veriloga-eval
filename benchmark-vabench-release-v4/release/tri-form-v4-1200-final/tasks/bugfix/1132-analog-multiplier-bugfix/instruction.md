# Analog Multiplier Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `analog_multiplier_gain.va`: `analog_multiplier_gain`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ANALOG_PRODUCT`: Drive `sigout` to `V(sigin1) * V(sigin2)` scaled by `gain`, preserving product sign.
- `P_GAIN_PARAMETER_APPLIED`: Apply the overridable `gain` parameter multiplicatively to the input product.
- `P_MULTIPLICATIVE_NOT_ADDITIVE`: The transfer must be multiplicative and must not replace the product with addition or a square of one input.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `analog_multiplier_gain.va`.
Every supplied `.va` file is editable; do not add or omit files.
