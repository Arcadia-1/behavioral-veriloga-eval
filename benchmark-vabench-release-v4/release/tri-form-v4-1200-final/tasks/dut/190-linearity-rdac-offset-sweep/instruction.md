# Linearity RDAC Offset Sweep

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `linearity_rdac_offset_sweep.va`: `linearity_rdac_offset_sweep`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_SWEEP_DIRECTION`: Rising `ck` crossings implement the RDAC sweep using `d < 0.5*vdd` as the low comparator direction.
- `P_SWEEP_INITIAL_STATE`: Initialize `vref`, `vin`, search step, and stored comparator direction to the declared sweep state.
- `P_ITERATIVE_SEARCH_UPDATES`: For each RDAC code, run exactly `iter_num` search-update clocks and halve the step before moving on direction changes.
- `P_CODE_UPDATE_AND_RECENTER`: The clock after each search window updates the 7-bit code, recenters the search, and advances the sweep without an extra search step.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `linearity_rdac_offset_sweep.va`.
Do not add or omit artifacts.
