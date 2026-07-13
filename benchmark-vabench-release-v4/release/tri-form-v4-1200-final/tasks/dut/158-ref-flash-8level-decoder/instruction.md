# Ref Flash 8level Decoder

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ref_flash_8level_decoder.va`: `ref_flash_8level_decoder`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_EIGHT_TAP_COUNT`: Each rising `clks` crossing counts all eight asserted flash taps into the held decoder count.
- `P_RESIDUE_CENTERING`: `vres` subtracts the centered four-count flash estimate from the sampled input residue.
- `P_OUTPUT_NORMALIZATION`: `dout` reports the tap count normalized by eight without extra output scaling.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ref_flash_8level_decoder.va`.
Do not add or omit artifacts.
