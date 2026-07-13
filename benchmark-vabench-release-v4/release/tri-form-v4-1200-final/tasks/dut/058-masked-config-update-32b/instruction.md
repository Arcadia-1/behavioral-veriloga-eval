# Masked Config Update 32b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `masked_config_update_32b.va`: `masked_config_update_32b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_MASKED_SELECTION`: For each bit N, out_cfg[N] equals new_cfg[N] when mask[N] is high and equals old_cfg[N] when mask[N] is low.
- `P_ZERO_MASK_IDENTITY`: With every mask bit low, the complete output word equals old_cfg.
- `P_FULL_MASK_REPLACEMENT`: With every mask bit high, the complete output word equals new_cfg.
- `P_BIT_INDEPENDENCE`: Changing mask or data bit N affects only out_cfg[N]; bus indices are neither reversed nor shifted.
- `P_OUTPUT_LEVELS`: Each output bit uses 0 V for logic low and vdd for logic high with finite transition smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `masked_config_update_32b.va`.
Do not add or omit artifacts.
