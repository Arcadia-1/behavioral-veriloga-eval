# Strongarm Style Latch Comparator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cmp_strongarm.va`: `cmp_strongarm`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_AND_FALLING_RESET`: All decision and latch monitor outputs initialize low and return low after each falling clock crossing.
- `P_POSITIVE_DECISION`: A rising clock crossing with VINP minus VINN minus voffset positive latches DCMPP and LP high while DCMPN and LM remain low.
- `P_NEGATIVE_DECISION`: A rising clock crossing with VINP minus VINN minus voffset negative latches DCMPN and LM high while DCMPP and LP remain low.
- `P_ZERO_DIFFERENTIAL`: An exactly zero effective differential sampled at a rising clock crossing leaves both complementary decision states low.
- `P_LATCH_HOLD`: The sampled decision is held between clock events and does not track input changes while the clock remains high.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cmp_strongarm.va`.
Do not add or omit artifacts.
