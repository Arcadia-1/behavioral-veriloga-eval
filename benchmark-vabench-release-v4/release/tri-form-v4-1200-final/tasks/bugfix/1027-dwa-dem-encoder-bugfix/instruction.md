# DWA DEM Encoder Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dwa_ptr_gen.va`: `dwa_ptr_gen`
- `v2b_4b.va`: `v2b_4b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_V2B_ROUND_AND_CLAMP`: On each rising helper clock crossing, vin rounds to the nearest integer and clamps to a four-bit code from 0 through 15.
- `P_ACTIVE_LOW_RESET_POINTER`: A sampled active-low reset initializes ptr to the one-hot ptr_init position.
- `P_ROTATING_POINTER_UPDATE`: Each post-reset rising edge advances the circular pointer by the sampled unsigned code modulo 16.
- `P_POINTER_ONE_HOT`: Ptr remains exactly one-hot at the updated circular pointer position.
- `P_DWA_SELECTED_MASK`: Cell_en implements the public rotating span and LSB boundary-cell rule for the sampled code, including the code-zero boundary-cell case.
- `P_SYSTEM_CODE_BINDING`: The four helper outputs feed the DWA code bus in MSB-to-LSB order without bit reversal.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dwa_ptr_gen.va`, `v2b_4b.va`.
Every supplied `.va` file is editable; do not add or omit files.
