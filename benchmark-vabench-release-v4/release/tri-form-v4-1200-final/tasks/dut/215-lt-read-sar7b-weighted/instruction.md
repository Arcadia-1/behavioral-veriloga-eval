# LT Read SAR7B Weighted

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `lt_read_sar7b_weighted.va`: `lt_read_sar7b_weighted`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CONTINUOUSLY_DRIVE`: Continuously drive:
- `P_TEXT_VOUT_VREF_VREF_D7_D6`: ```text vout = -vref + vref * (d7 + d6/2 + d5/4 + d4/8 + d3/16 + d2/32 + d1/64 + d0/128) ```
- `P_WHERE_EACH_D_TERM_IS_1`: where each `d` term is `1` when the corresponding input voltage is above `vth` and `0` otherwise.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `lt_read_sar7b_weighted.va`.
Do not add or omit artifacts.
