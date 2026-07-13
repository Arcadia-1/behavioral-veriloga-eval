# Coarse QTZ 3bit Residue

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `coarse_qtz_3bit_residue.va`: `coarse_qtz_3bit_residue`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLIP_VIN_TO_THE_RANGE_FROM`: Clip `vin` to the range from `-vref` to `+vref`.
- `P_QUANTIZE_THE_CLIPPED_VALUE_INTO_EIGHT`: Quantize the clipped value into eight 3-bit codes using round-to-nearest behavior.
- `P_SATURATE_THE_CODE_AT_THE_ENDPOINTS`: Saturate the code at the endpoints.
- `P_USE_UNIFORMLY_SPACED_QUANTIZATION_LEVELS_START`: Use uniformly spaced quantization levels starting at `-vref`, with one LSB equal to one eighth of the full input span.
- `P_DRIVE_D0_D1_AND_D2_AS`: Drive `d0`, `d1`, and `d2` as LSB-to-MSB voltage-coded bits.
- `P_DRIVE_VRES_AS_THE_CLIPPED_INPUT`: Drive `vres` as the clipped input minus the selected quantized analog level.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `coarse_qtz_3bit_residue.va`.
Do not add or omit artifacts.
