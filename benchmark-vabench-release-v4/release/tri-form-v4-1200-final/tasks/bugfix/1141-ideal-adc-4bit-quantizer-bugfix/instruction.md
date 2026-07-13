# Ideal ADC 4bit Quantizer Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ideal_adc_4bit_quantizer.va`: `ideal_adc_4bit_quantizer`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLOCKED_DIFFERENTIAL_SAMPLE`: Each rising `vclk` crossing through `vtrans_clk` samples `V(vip)-V(vin)` and holds the resulting analog code on `digital` until the next sample.
- `P_SYMMETRIC_INPUT_RANGE`: The sampled differential input is quantized over the symmetric span from `-vref` to `+vref`; values outside that span saturate to the endpoint codes.
- `P_CODE_SCALE_AND_LSB`: `digital` represents the selected code using the declared `levels` spacing so adjacent quantization bins differ by one LSB.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ideal_adc_4bit_quantizer.va`.
Every supplied `.va` file is editable; do not add or omit files.
