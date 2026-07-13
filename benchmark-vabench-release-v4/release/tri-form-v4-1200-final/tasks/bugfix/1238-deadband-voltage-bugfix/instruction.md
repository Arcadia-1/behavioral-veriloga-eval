# Deadband Voltage Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `deadband_voltage.va`: `deadband_voltage`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_DEADBAND_ZERO_REGION`: Inside the inclusive deadband window from `sigin_dead_low` to `sigin_dead_high`, drive `sigout` to `0 V`.
- `P_SIGNED_RESIDUE_OUTSIDE_WINDOW`: Below the lower edge, drive the signed excess below `sigin_dead_low`; above the upper edge, drive the signed excess above `sigin_dead_high` while preserving sign.
- `P_DEADBAND_EDGE_CONTINUITY`: Use the public lower and upper threshold values so the output is continuous at both deadband edges.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `deadband_voltage.va`.
Every supplied `.va` file is editable; do not add or omit files.
