# Weighted Decoder 7b5

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `weighted_decoder_7b5.va`: `weighted_decoder_7b5`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SHARED_272_DENOMINATOR`: All decoded outputs use the shared normalization denominator of 272.0, including the fixed reference basis.
- `P_SEVEN_BIT_OUTPUT`: `aout7b` reports the 7-bit decoded analog output with the specified redundant SAR weights.
- `P_SEVEN_HALF_BIT_OUTPUT`: `aout7b5` preserves the half-bit redundant contribution and correct polarity.
- `P_EIGHT_BIT_OUTPUT`: `aout8b` reports the full 8-bit weighted output with the correct amplitude.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `weighted_decoder_7b5.va`.
Do not add or omit artifacts.
