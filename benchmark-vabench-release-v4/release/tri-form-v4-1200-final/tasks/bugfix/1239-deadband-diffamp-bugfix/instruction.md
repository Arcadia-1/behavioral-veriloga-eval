# Deadband Diffamp Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `deadband_diffamp.va`: `deadband_diffamp`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_DIFFERENTIAL_POLARITY`: Compute the differential input as `V(sigin_p, sigin_n)` with the documented polarity.
- `P_DEADBAND_LEAK_OUTPUT`: Inside the inclusive differential deadband, drive the public leakage level `sigout_leak`.
- `P_ASYMMETRIC_RESIDUE_GAINS`: Below the lower threshold use `gain_low` for the low-side signed residue plus leakage; above the upper threshold use `gain_high` for the high-side signed residue plus leakage.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `deadband_diffamp.va`.
Every supplied `.va` file is editable; do not add or omit files.
