# Linear PFD Gain Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `linear_pfd_gain.va`: `linear_pfd_gain`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_DIFFERENTIAL_INPUT_POLARITY`: `out` uses the input difference `in1 - in2`, preserving the specified differential polarity.
- `P_KPHI_GAIN_SCALE`: `out` is scaled by the public gain coefficient `kphi` rather than unit gain or an alternate scale.
- `P_CONTINUOUS_ANALOG_TRACKING`: `out` continuously tracks analog input changes without clocked state, clipping, or single-ended substitution.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `linear_pfd_gain.va`.
Every supplied `.va` file is editable; do not add or omit files.
