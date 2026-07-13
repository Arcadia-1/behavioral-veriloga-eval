# Ref Flash 15level Decoder

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ref_flash_15level_decoder.va`: `ref_flash_15level_decoder`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_FIFTEEN_TAP_COUNT`: Each rising `clks` crossing counts voltage-coded assertions across the 15 tap inputs.
- `P_FULL_TAP_COVERAGE`: Upper and lower tap inputs all contribute to the count; no subset of taps is ignored.
- `P_FRACTION_NORMALIZATION_AND_GAIN`: `dout` reports the count divided by 15 without additional gain scaling.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ref_flash_15level_decoder.va`.
Do not add or omit artifacts.
