# CDAC 6b Stage1 Up Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cdac_6b_stage1_up.va`: `cdac_6b_stage1_up`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_AT_INITIALIZATION_AND_ON_EACH_FALLING`: At initialization and on each falling `clks` crossing, sample `vin` into the residue. On rising control crossings, add binary-weighted residue contributions: `dctrl5` adds 1/2, `dctrl4` 1/4, continuing down to `dctrl0` at 1/64. Hold and continuously drive the current residue state between events.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cdac_6b_stage1_up.va`.
Every supplied `.va` file is editable; do not add or omit files.
