# Control Word Encoder 7b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `control_word_encoder_7b.va`: `control_word_encoder_7b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SEVEN_BIT_DECODE`: `ctrl` is decoded LSB-first so `d0` carries bit 0 and `d6` carries bit 6.
- `P_BIT_POLARITY`: A decoded one drives its output high and a decoded zero drives its output low.
- `P_OUTPUT_RAIL_LEVELS`: Each output uses the declared `vhi` and `vlo` voltage levels for its decoded bit.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `control_word_encoder_7b.va`.
Do not add or omit artifacts.
