# Fixed Gain Amplifier Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `gain_amp_fixed.va`: `gain_amp_fixed`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_DIFFERENTIAL_GAIN`: The output differential equals ACTUAL_GAIN times the input differential.
- `P_POSITIVE_POLARITY`: A positive input differential produces a positive output differential and a negative input differential produces a negative output differential.
- `P_OUTPUT_COMMON_MODE`: The output pair remains centered at vdd/2 independently of input common mode.
- `P_SYMMETRIC_OUTPUT_PAIR`: Half the amplified differential is added to VOUT_P and half is subtracted from VOUT_N.
- `P_PARAMETER_OVERRIDES`: Legal ACTUAL_GAIN and vdd overrides alter differential gain and output common mode according to their declared meanings.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `gain_amp_fixed.va`.
Every supplied `.va` file is editable; do not add or omit files.
