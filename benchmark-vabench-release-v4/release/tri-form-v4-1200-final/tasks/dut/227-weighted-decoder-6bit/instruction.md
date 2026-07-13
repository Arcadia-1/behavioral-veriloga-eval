# Weighted Decoder 6bit

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `weighted_decoder_6bit.va`: `weighted_decoder_6bit`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_TREAT_EACH_INPUT_AS_LOGIC_1`: Treat each input as logic 1 when its voltage is greater than `vth`, otherwise logic 0.
- `P_INTERPRET_VD1_VD6_AS_AN_UNSIGNED`: Interpret `vd1..vd6` as an unsigned binary word with `vd1` as MSB and `vd6` as LSB.
- `P_SCALE_THE_DECODED_CODE_BY_VREF`: Scale the decoded code by `vref`.
- `P_MAP_ALL_ZERO_INPUT_TO_0`: Map all-zero input to 0 V.
- `P_MAP_ALL_ONES_INPUT_TO_VREF`: Map all-ones input to `vref`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `weighted_decoder_6bit.va`.
Do not add or omit artifacts.
