# Unit Element Thermometer DAC Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `thermometer_dac_15seg.va`: `thermometer_dac_15seg`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ZERO_SCALE`: With no active segment inputs, aout equals the vss endpoint after transition settling.
- `P_FULL_SCALE`: With all fifteen segment inputs active, aout equals the vref endpoint after transition settling.
- `P_UNIT_ELEMENT_WEIGHT`: Each input above vth contributes exactly one fifteenth of the vref-minus-vss span, including seg14.
- `P_PERMUTATION_INVARIANCE`: Any two segment patterns with the same active count produce the same settled aout.
- `P_COUNT_MONOTONICITY`: Increasing the active segment count cannot reduce the settled DAC output for vref above vss.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `thermometer_dac_15seg.va`.
Every supplied `.va` file is editable; do not add or omit files.
