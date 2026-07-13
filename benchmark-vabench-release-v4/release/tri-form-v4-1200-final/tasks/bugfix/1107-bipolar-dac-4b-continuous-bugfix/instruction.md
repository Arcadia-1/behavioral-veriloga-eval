# Bipolar DAC 4b Continuous Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `bipolar_dac_4b_continuous.va`: `bipolar_dac_4b_continuous`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_UNSIGNED_BIT_DECODE`: Each input is decoded continuously as one only when its voltage exceeds vtrans, with vd3 as MSB and vd0 as LSB.
- `P_NEGATIVE_FULL_SCALE`: Unsigned code 0 produces approximately negative vref.
- `P_POSITIVE_FULL_SCALE`: Unsigned code 15 produces approximately positive vref.
- `P_UNIFORM_CODE_STEP`: Every one-code increase raises the output target by the same voltage increment across codes 0 through 15.
- `P_MONOTONIC_TRANSFER`: The output is strictly monotonic with increasing unsigned code for vref greater than zero.
- `P_CONTINUOUS_REEVALUATION`: The DAC target responds to input-code threshold changes without requiring a clock event, using tdel, trise, and tfall for output timing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `bipolar_dac_4b_continuous.va`.
Every supplied `.va` file is editable; do not add or omit files.
