# Comparator Offset Driver Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `comparator_offset_binary_driver.va`: `comparator_offset_binary_driver`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_FALLING_CLOCK_DECISION_SAMPLE`: On each falling `clk` threshold crossing, sample `dcmpp` to choose the next binary-search direction.
- `P_DECISION_POLARITY_UPDATE`: A high decision moves the differential input negative and a low decision moves it positive.
- `P_HALVING_SEARCH_STEP`: The differential search step halves after each sampled decision.
- `P_COMMON_MODE_HALF_SCALE_DRIVE`: `vinp` and `vinn` are driven symmetrically around the common-mode level with half differential amplitude on each side.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `comparator_offset_binary_driver.va`.
Every supplied `.va` file is editable; do not add or omit files.
