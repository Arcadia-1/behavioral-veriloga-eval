# Limiting Differential Amplifier Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `limiting_differential_amplifier.va`: `limiting_differential_amplifier`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_OFFSET_CORRECTED_DIFFERENTIAL_GAIN`: Compute `gain * (V(sigin_p, sigin_n) - sigin_offset)`.
- `P_OUTPUT_MIDPOINT_REFERENCE`: Center the amplified value at `(sigout_high + sigout_low) / 2`.
- `P_OUTPUT_RAIL_CLAMP`: Clamp the final target to the inclusive interval `[sigout_low, sigout_high]`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `limiting_differential_amplifier.va`.
Every supplied `.va` file is editable; do not add or omit files.
