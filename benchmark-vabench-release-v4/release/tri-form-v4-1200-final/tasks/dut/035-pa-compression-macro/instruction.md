# PA Compression Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pa_compression_macro.va`: `pa_compression_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_COMMON_MODE`: Initialization or active reset returns out to 0.45 V common mode and clears metric to 0 V.
- `P_CLOCKED_UPDATE`: Out and metric update from the sampled signed drive vin - 0.45 V on rising clk crossings and hold between updates.
- `P_LINEAR_REGION`: When 0.45 V + gain*(vin - 0.45 V) lies from 0.12 V through 0.78 V, out equals that target and metric is 0.1 V.
- `P_SYMMETRIC_COMPRESSION`: Targets above 0.78 V or below 0.12 V are compressed with slope 0.18 about the corresponding boundary, and metric is 0.85 V.
- `P_OUTPUT_CLAMP`: The compressed output remains within 0.02 V through 0.88 V with finite transition smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pa_compression_macro.va`.
Do not add or omit artifacts.
