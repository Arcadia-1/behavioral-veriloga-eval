# Programmable Divider By N

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `programmable_divider_by_n.va`: `programmable_divider_by_n`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DIVIDE_RATIO_EDGE_COUNTING`: On rising crossings of `clk` through `vth`, round `divctrl` to the requested divide ratio, clip ratios below one to one, maintain the modulo counter, and assert `out` only when the counter state is zero.
- `P_CLOCK_THRESHOLD_OBSERVABILITY`: Use the public `vth` threshold for edge detection so the declared clock stimulus produces the expected counted edges.
- `P_OUTPUT_HIGH_LEVEL`: Drive high output states near the public `vh` level and low states near `0 V`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `programmable_divider_by_n.va`.
Do not add or omit artifacts.
