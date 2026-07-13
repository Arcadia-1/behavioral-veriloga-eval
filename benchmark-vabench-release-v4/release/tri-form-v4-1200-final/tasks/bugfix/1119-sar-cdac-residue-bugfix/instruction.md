# SAR CDAC Residue Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sar_cdac_residue.va`: `sar_cdac_residue`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INPUT_SAMPLE`: At initial_step and each rising CLK crossing through vdd/2, the residue state samples VIN.
- `P_S6_HALF_ADD`: Each falling S6 crossing through vdd/2 adds one half of the public reference span to the current residue.
- `P_BINARY_SUBTRACTIONS`: Rising crossings of S5, S4, S3, S2, and S1 through vdd/2 subtract one fourth, one eighth, one sixteenth, one thirty-second, and one sixty-fourth of the public reference span respectively.
- `P_EDGE_POLARITY`: S6 updates only on falling vdd/2 threshold crossings, while S5 through S1 update only on rising vdd/2 threshold crossings.
- `P_ACCUMULATED_STATE`: Between declared sampling and switch events, VRES represents and holds the accumulated residue state.
- `P_OUTPUT_TRANSITION`: VRES changes from the residue state using the declared tr transition time.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sar_cdac_residue.va`.
Every supplied `.va` file is editable; do not add or omit files.
