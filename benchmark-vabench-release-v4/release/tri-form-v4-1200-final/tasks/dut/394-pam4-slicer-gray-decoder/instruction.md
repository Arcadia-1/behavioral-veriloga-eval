# PAM4 Slicer and Gray Decoder

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pam4_slicer_gray_decoder.va`: `pam4_slicer_gray_decoder`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or disable clears both bits, level metric, and valid.
- `P_RISING_EDGE_SAMPLE_HOLD`: vin is sliced only on enabled rising clk edges and outputs hold between samples.
- `P_PAM4_THRESHOLDS`: The three ordered thresholds divide vin into levels zero through three.
- `P_GRAY_MAPPING`: Levels zero through three map to Gray codes 00, 01, 11, and 10.
- `P_LEVEL_METRIC`: level_metric reports the sliced level as vss plus k/3 of the output span.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pam4_slicer_gray_decoder.va`.
Do not add or omit artifacts.
