# Level Shifter Offset

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `level_shifter_offset.va`: `level_shifter_offset`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DRIVE_SIGOUT_TO_V_SIGIN_PLUS_SIGSHIFT`: Drive `sigout` to `V(sigin) + sigshift` for the current input voltage.
- `P_PRESERVE_UNITY_GAIN_WHILE_ADDING_OFFSET`: Preserve unity gain from `sigin` to `sigout` while adding the configured `sigshift` offset; input changes must appear at `sigout` with the same voltage step size.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `level_shifter_offset.va`.
Do not add or omit artifacts.
