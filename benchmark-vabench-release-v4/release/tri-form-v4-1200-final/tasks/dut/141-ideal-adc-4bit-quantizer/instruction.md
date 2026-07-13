# Ideal ADC 4bit Quantizer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ideal_adc_4bit_quantizer.va`: `ideal_adc_4bit_quantizer`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_DIFFERENTIAL_SAMPLE`: Each rising `vclk` crossing through `vtrans_clk` samples `V(vip)-V(vin)` and holds the resulting analog code on `digital` until the next sample.
- `P_SYMMETRIC_INPUT_RANGE`: The sampled differential input is quantized over the symmetric span from `-vref` to `+vref`; values outside that span saturate to the endpoint codes.
- `P_CODE_SCALE_AND_LSB`: `digital` represents the selected code using the declared `levels` spacing so adjacent quantization bins differ by one LSB.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ideal_adc_4bit_quantizer.va`.
Do not add or omit artifacts.
