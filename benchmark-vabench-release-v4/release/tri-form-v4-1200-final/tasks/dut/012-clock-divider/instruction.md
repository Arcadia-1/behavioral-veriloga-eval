# Clock Divider

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `clk_divider_ref.va`: `clk_divider_ref`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET`: Active-low reset clears divider phase and drives clk_out and lock low.
- `P_RATIO_DECODE`: The LSB-first 8-bit code selects the divide ratio, with code zero mapped to ratio one.
- `P_DIVIDED_PERIOD`: For ratios above one, successive clk_out rising edges span the decoded number of clk_in rising edges.
- `P_ODD_RATIO_DUTY`: Odd ratios retain both phases with floor/ceil segment lengths differing by at most one input cycle.
- `P_LOCK_REACQUIRE`: lock asserts after one complete output period and clears/reacquires when the ratio changes.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `clk_divider_ref.va`.
Do not add or omit artifacts.
