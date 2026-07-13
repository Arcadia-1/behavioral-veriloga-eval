# Trim Ctrl 4bit

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `trim_ctrl_4bit.va`: `trim_ctrl_4bit`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ANALOG_INPUT_ROUNDING`: Round `ain` to the nearest integer code level rather than truncating.
- `P_LOW_FOUR_BIT_MAPPING`: Emit the low four bits of the rounded code on `dout0..dout3` in the declared bit order.
- `P_CONTINUOUS_CODE_UPDATE`: Update deterministically as `ain` changes without requiring hidden state or clocks.
- `P_TRIM_OUTPUT_LEVELS`: All trim outputs are voltage-coded at valid low/high levels.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `trim_ctrl_4bit.va`.
Do not add or omit artifacts.
