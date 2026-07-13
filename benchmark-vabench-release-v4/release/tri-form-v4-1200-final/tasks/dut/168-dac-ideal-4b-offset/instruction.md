# DAC Ideal 4b Offset

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dac_ideal_4b_offset.va`: `dac_ideal_4b_offset`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_THRESHOLDED_4BIT_CODE`: `din3` is the MSB and `din0` is the LSB of a 4-bit unsigned code using threshold `vth`.
- `P_OFFSET_PLUS_SCALED_TRIM`: The output equals the public `offset` plus the code-scaled trim increment using the public `scaling` factor.
- `P_EVENT_UPDATED_OUTPUT`: `dout` updates on input threshold crossings or initial step and otherwise holds the smooth voltage output.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dac_ideal_4b_offset.va`.
Do not add or omit artifacts.
