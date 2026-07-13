# Clocked ADC Quantizer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `flash_adc_3b.va`: `flash_adc_3b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RISING_EDGE_QUANTIZATION`: At each rising CLK crossing, VIN is quantized into one of eight uniform bins spanning vrefn to vrefp.
- `P_CODE_CLAMP`: Samples at or outside the conversion endpoints produce codes clamped to the inclusive range 0 through 7.
- `P_BINARY_RAIL_ENCODING`: DOUT2 through DOUT0 encode the held code from MSB to LSB using VDD for one and VSS for zero.
- `P_CODE_MONOTONICITY`: For increasing VIN samples across the conversion range, the sampled three-bit code is nondecreasing.
- `P_SAMPLE_HOLD`: The output code remains stable between rising CLK crossings even when VIN changes.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `flash_adc_3b.va`.
Do not add or omit artifacts.
