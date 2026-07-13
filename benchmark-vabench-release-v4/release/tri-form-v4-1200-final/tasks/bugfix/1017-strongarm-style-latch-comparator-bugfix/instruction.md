# Strongarm Style Latch Comparator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cmp_strongarm.va`: `cmp_strongarm`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_AND_FALLING_RESET`: All decision and latch monitor outputs initialize low and return low after each falling clock crossing.
- `P_POSITIVE_DECISION`: A rising clock crossing with VINP minus VINN minus voffset positive latches DCMPP and LP high while DCMPN and LM remain low.
- `P_NEGATIVE_DECISION`: A rising clock crossing with VINP minus VINN minus voffset negative latches DCMPN and LM high while DCMPP and LP remain low.
- `P_ZERO_DIFFERENTIAL`: An exactly zero effective differential sampled at a rising clock crossing leaves both complementary decision states low.
- `P_LATCH_HOLD`: The sampled decision is held between clock events and does not track input changes while the clock remains high.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cmp_strongarm.va`.
Every supplied `.va` file is editable; do not add or omit files.
