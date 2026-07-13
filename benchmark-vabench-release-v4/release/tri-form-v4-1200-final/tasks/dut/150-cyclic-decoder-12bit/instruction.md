# Cyclic Decoder 12bit

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cyclic_decoder_12bit.va`: `cyclic_decoder_12bit`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RISING_EDGE_12BIT_DECODE`: Each rising `clks` crossing samples the twelve voltage-coded bits into an unsigned code.
- `P_BIT_WEIGHT_ORDER`: `d0` is the LSB and `d11` is the MSB in the decoded code.
- `P_CENTERED_OUTPUT_SCALE`: The decoded value is normalized to the full 12-bit range, shifted by the half-scale midpoint, and held on `dout`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cyclic_decoder_12bit.va`.
Do not add or omit artifacts.
