# Pipe 2lane Edge Align

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pipe_2lane_edge_align.va`: `pipe_2lane_edge_align`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_LANE1_STATE`: Before alignment edges, the output state initializes from `din1`.
- `P_RISING_EDGE_LANE1`: A rising `clk_align` crossing samples and publishes `din1`.
- `P_FALLING_EDGE_LANE2`: A falling `clk_align` crossing samples and publishes `din2`.
- `P_SELECTED_LEVEL_HOLD`: `dout` holds the last selected lane level with full output amplitude between alignment edges.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pipe_2lane_edge_align.va`.
Do not add or omit artifacts.
