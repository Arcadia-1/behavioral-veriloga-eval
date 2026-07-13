# Element Shuffler

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `element_shuffler.va`: `element_shuffler`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_START`: Active-low reset establishes the state so the first rising clk edge after release selects out2.
- `P_PERMUTATION`: Rising clk edges advance the repeating out2, out0, out3, out1 permutation.
- `P_ONE_HOT`: Exactly one output is high in every stable released-reset state.
- `P_RAIL_LEVELS`: The selected output approaches vdd and all other outputs approach 0 V with finite smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `element_shuffler.va`.
Do not add or omit artifacts.
