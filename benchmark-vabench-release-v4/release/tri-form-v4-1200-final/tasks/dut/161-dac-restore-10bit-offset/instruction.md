# DAC Restore 10bit Offset

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dac_restore_10bit_offset.va`: `dac_restore_10bit_offset`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_CODE_SAMPLING`: Only rising crossings of `clk` through `vth` update the held DAC output; input-bit changes between clock crossings do not alter `vout`.
- `P_WEIGHTED_REDUNDANT_CODE`: `D10` is the largest weight, `D0` is the LSB, and `D6` and `D7` both contribute the redundant 64-LSB weight before scaling.
- `P_OFFSET_MIDRISE_OUTPUT`: The asserted weighted code is shifted by the source -32 LSB offset and placed at the mid-rise half-LSB output level using the public `lsb` scale.
- `P_OUTPUT_SMOOTH_HOLD`: `vout` transitions smoothly to each sampled code value and holds that value until the next qualifying clock edge.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dac_restore_10bit_offset.va`.
Do not add or omit artifacts.
