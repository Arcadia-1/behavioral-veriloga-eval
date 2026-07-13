# Clocked ADC Quantizer Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `flash_adc_3b.va`: `flash_adc_3b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RISING_EDGE_QUANTIZATION`: At each rising CLK crossing, VIN is quantized into one of eight uniform bins spanning vrefn to vrefp.
- `P_CODE_CLAMP`: Samples at or outside the conversion endpoints produce codes clamped to the inclusive range 0 through 7.
- `P_BINARY_RAIL_ENCODING`: DOUT2 through DOUT0 encode the held code from MSB to LSB using VDD for one and VSS for zero.
- `P_CODE_MONOTONICITY`: For increasing VIN samples across the conversion range, the sampled three-bit code is nondecreasing.
- `P_SAMPLE_HOLD`: The output code remains stable between rising CLK crossings even when VIN changes.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `flash_adc_3b.va`.
Every supplied `.va` file is editable; do not add or omit files.
