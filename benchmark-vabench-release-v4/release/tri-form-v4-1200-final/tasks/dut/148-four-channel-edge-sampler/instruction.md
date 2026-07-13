# Four Channel Edge Sampler

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `four_channel_edge_sampler.va`: `four_channel_edge_sampler`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CONFIGURED_EDGE_SIMULTANEOUS_SAMPLE`: The configured `clk` crossing direction samples `vin0` through `vin3` simultaneously and updates all held outputs together.
- `P_CHANNEL_MAPPING`: Each sampled input channel maps to the same-numbered output channel without swaps.
- `P_OUTPUT_GAIN_AND_HOLD`: Each `vout` holds the sampled amplitude without gain scaling until the next sampling edge.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `four_channel_edge_sampler.va`.
Do not add or omit artifacts.
