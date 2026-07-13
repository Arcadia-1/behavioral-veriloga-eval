# LNA Gain Compression Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `lna_gain_compression_macro.va`: `lna_gain_compression_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_AND_RESET_COMMON_MODE`: Initialization sets out to 0.45 V and clears metric; an active-high reset sampled on a rising clk crossing restores the same state.
- `P_SMALL_SIGNAL_GAIN`: For linear values from 0.14 V through 0.76 V, out equals 0.45 V plus gain times the sampled vin deviation and metric is 0.1 V.
- `P_POSITIVE_COMPRESSION`: Above linear 0.76 V, excess signal is compressed by factor 0.28 and metric is 0.8 V.
- `P_NEGATIVE_COMPRESSION`: Below linear 0.14 V, excess signal is compressed by factor 0.28 and metric is 0.8 V.
- `P_FINAL_OUTPUT_CLAMP`: The final held output remains within 0.04 V through 0.86 V.
- `P_CLOCKED_HOLD`: Out and metric update on rising clock crossings and hold between samples.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `lna_gain_compression_macro.va`.
Do not add or omit artifacts.
