# Linearity RDAC Offset Sweep Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `linearity_rdac_offset_sweep.va`: `linearity_rdac_offset_sweep`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLOCKED_SWEEP_DIRECTION`: Rising `ck` crossings implement the RDAC sweep using `d < 0.5*vdd` as the low comparator direction.
- `P_SWEEP_INITIAL_STATE`: Initialize `vref`, `vin`, search step, and stored comparator direction to the declared sweep state.
- `P_ITERATIVE_SEARCH_UPDATES`: For each RDAC code, run exactly `iter_num` search-update clocks and halve the step before moving on direction changes.
- `P_CODE_UPDATE_AND_RECENTER`: The clock after each search window updates the 7-bit code, recenters the search, and advances the sweep without an extra search step.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `linearity_rdac_offset_sweep.va`.
Every supplied `.va` file is editable; do not add or omit files.
