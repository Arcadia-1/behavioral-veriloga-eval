# CDAC Bidirect Residue Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cdac_bidirect_residue.va`: `cdac_bidirect_residue`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_SAMPLE_RESIDUE_ON_CLKS_FALL`: At initialization and on each falling `clks` crossing, sample `vin` into the residue state.
- `P_MSB_RESIDUE_STEP_SIGN`: A falling `dctrl7` event adds the half-scale MSB residue step with the declared sign.
- `P_LOWER_BIT_RESIDUE_WEIGHTS`: Falling `dctrl6..dctrl1` events apply the declared binary-weighted residue steps.
- `P_RESIDUE_OUTPUT_GAIN`: `vres` drives the sampled residue with the declared gain and voltage scale.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cdac_bidirect_residue.va`.
Every supplied `.va` file is editable; do not add or omit files.
