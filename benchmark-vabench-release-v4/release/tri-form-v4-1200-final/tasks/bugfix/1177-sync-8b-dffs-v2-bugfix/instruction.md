# Sync 8b DFFs V2 Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sync_8b_dffs_v2.va`: `sync_8b_dffs_v2`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_PHASED_CAPTURE_ORDER`: Each phase clock captures its corresponding `dl` input and shifts previously captured upper-phase data down the chain in the specified order.
- `P_INTERMEDIATE_OUTPUT_CAPTURE`: Intermediate outputs, including `do4`, reflect their synchronized pipeline state rather than a stuck or skipped stage.
- `P_FINAL_OUTPUT_CAPTURE`: The most delayed output `do8` reflects the final synchronized stage with correct polarity.
- `P_FULL_LEVEL_OUTPUTS`: All `do` outputs drive full voltage-coded levels for their captured state.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sync_8b_dffs_v2.va`.
Every supplied `.va` file is editable; do not add or omit files.
