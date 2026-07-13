# Iterative ISAR DAC Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `iterative_isar_dac.va`: `iterative_isar_dac`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_INITIAL_SEARCH_STATE`: At initialization and reset, `vdac` returns to zero and the search step returns to `range`.
- `P_COMPARATOR_POLARITY_UPDATE`: On each rising `clk` crossing while active, `dcmp > vth` steps `vdac` in the specified comparator-driven direction and low decisions step the opposite way.
- `P_RADIX_STEP_REDUCTION`: The search step is divided by the public radix after each active comparison until it reaches the LSB limit.
- `P_HELD_DAC_OUTPUT`: `vdac` holds the current iterative search value between reset and qualifying clock events.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `iterative_isar_dac.va`.
Every supplied `.va` file is editable; do not add or omit files.
