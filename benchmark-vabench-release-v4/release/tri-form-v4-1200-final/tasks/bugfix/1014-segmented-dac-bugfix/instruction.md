# Segmented DAC Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `segmented_dac.va`: `segmented_dac`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_SEGMENT_WEIGHTS`: b0 and b1 contribute one and two LSB steps while each active thermometer control contributes four LSB steps.
- `P_CODE_MONOTONICITY`: Increasing the summed segmented code does not decrease aout.
- `P_ENDPOINTS`: The zero code maps to vss and the all-active 15-step code maps to vref.
- `P_RAIL_RELATIVE_MAPPING`: Intermediate codes linearly span the vss-to-vref range.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `segmented_dac.va`.
Every supplied `.va` file is editable; do not add or omit files.
