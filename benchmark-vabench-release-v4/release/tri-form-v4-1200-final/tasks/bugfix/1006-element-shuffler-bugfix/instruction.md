# Element Shuffler Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `element_shuffler.va`: `element_shuffler`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_START`: Active-low reset establishes the state so the first rising clk edge after release selects out2.
- `P_PERMUTATION`: Rising clk edges advance the repeating out2, out0, out3, out1 permutation.
- `P_ONE_HOT`: Exactly one output is high in every stable released-reset state.
- `P_RAIL_LEVELS`: The selected output approaches vdd and all other outputs approach 0 V with finite smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `element_shuffler.va`.
Every supplied `.va` file is editable; do not add or omit files.
