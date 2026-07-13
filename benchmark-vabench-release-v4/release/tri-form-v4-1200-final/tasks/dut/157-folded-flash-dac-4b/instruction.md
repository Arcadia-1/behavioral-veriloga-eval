# Folded Flash DAC 4b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `folded_flash_dac_4b.va`: `folded_flash_dac_4b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_VOLTAGE_CODED_SUBCODE_DECODE`: `vd1` through `vd3` form the lower subcode and `vd4` selects the folded branch using `vtrans`.
- `P_FOLD_MIRROR_TRANSFER`: The upper folded branch mirrors the subcode around the fold center instead of using a direct unsigned code.
- `P_OUTPUT_SCALE_DENOMINATOR`: The folded code is scaled by the declared 4-bit denominator and reference before driving `vout`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `folded_flash_dac_4b.va`.
Do not add or omit artifacts.
