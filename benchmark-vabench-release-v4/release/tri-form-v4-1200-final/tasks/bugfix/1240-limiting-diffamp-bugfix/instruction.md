# Smooth Limiting Diffamp Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `limiting_diffamp.va`: `limiting_diffamp`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ODD_DIFFERENTIAL_POLARITY`: Compute `V(sigin_p, sigin_n)`, preserve polarity, and drive an odd differential transfer.
- `P_SMALL_SIGNAL_GAIN`: Near zero differential input, drive approximately `gain * V(sigin_p, sigin_n)`.
- `P_SMOOTH_SYMMETRIC_LIMITING`: For large positive and negative differential inputs, smoothly approach `+limit` and `-limit` without a hard clamp.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `limiting_diffamp.va`.
Every supplied `.va` file is editable; do not add or omit files.
