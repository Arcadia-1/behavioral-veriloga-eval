# Offset RDAC Search Flow

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `offset_rdac_search_flow.va`: `offset_rdac_search_flow`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_TWO_PHASE_CLOCKED_FLOW`: Rising `ck` crossings execute the deterministic RDAC-refinement phase before the offset-search phase, using `d < 0.5 V` as the low comparator direction.
- `P_REFERENCE_AND_CODE_INITIALIZATION`: Initialize `vref`, `vin`, and the 7-bit RDAC trial code to the declared reference-grid and MSB-first state.
- `P_RDAC_REFINEMENT_SEQUENCE`: The six RDAC refinement clocks resolve the current bit and assert the next lower trial bit in the declared order.
- `P_OFFSET_SEARCH_BISECTION`: The eight offset-search clocks compare consecutive directions, halve the search step on direction changes, and update `vin/vref` with the declared polarity.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `offset_rdac_search_flow.va`.
Do not add or omit artifacts.
