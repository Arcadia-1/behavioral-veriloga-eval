# Edge Interval TDC 8b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `edge_interval_tdc_8b.va`: `edge_interval_tdc_8b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_START_ARMS`: Each rising start crossing begins a new interval measurement, records that edge time, and clears valid.
- `P_NEXT_STOP_COMPLETES`: The first rising stop crossing after an armed start completes that measurement; stop crossings while unarmed do not change the result.
- `P_INTERVAL_QUANTIZATION`: A completed interval is rounded to the nearest whole nanosecond and reported as an unsigned code.
- `P_CODE_SATURATION`: Measured interval codes are saturated to the inclusive 8-bit range 0 through 255.
- `P_VALID_AND_BIT_ORDER`: valid asserts after completion; code0 is the least significant bit and code7 is the most significant bit, using 0 V and vdd logic levels.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `edge_interval_tdc_8b.va`.
Do not add or omit artifacts.
