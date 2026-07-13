# L2 CDAC 4b Residue Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `l2_cdac_4b_residue.va`: `l2_cdac_4b_residue`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_FALLING_CLOCK_SAMPLE`: `vin` is sampled into the residue on initial step and on falling `clks` crossings through `vdd/2`.
- `P_CONTROL_STEP_WEIGHTS`: Rising control crossings add positive capacitive reference steps: `dctrl3` is half scale, `dctrl2` quarter scale, and `dctrl1` eighth scale.
- `P_RETAINED_RESIDUE_OUTPUT`: `vres` retains the accumulated sampled residue between clock/control events.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `l2_cdac_4b_residue.va`.
Every supplied `.va` file is editable; do not add or omit files.
