# DAC7 Code Generator

## Task Contract

Implement a clocked seven-output voltage-coded counter source for DAC stimulus.

- Form: `dut`
- Level: support/L1 policy candidate
- Category: stimulus support component
- Target artifact: `dac7_code_generator.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`dac7_code_generator.va` must declare:

```verilog
module dac7_code_generator(clks, din0, din1, din2, din3, din4, din5, din6);
input clks;
output din0, din1, din2, din3, din4, din5, din6;
electrical clks, din0, din1, din2, din3, din4, din5, din6;
```

## Public Parameter Contract

- `vlo = 0`: low output voltage.
- `vhi = 0.9`: high output voltage.
- `vth = 0.45`: rising clock-edge threshold in volts.
- `tt = 20p`: output transition rise/fall time.

## Required Behavior

Initialize an 8-bit counter and all seven outputs low. On each rising threshold
crossing of `clks`, increment the counter and wrap it from 255 back to 0.

Drive inverted counter bits onto the outputs after each update:

- `din0`: inverted counter bit 7
- `din1`: inverted counter bit 6
- `din2`: inverted counter bit 5
- `din3`: inverted counter bit 4
- `din4`: inverted counter bit 3
- `din5`: inverted counter bit 2
- `din6`: inverted counter bit 1

Use `vhi` for logic one and `vlo` for logic zero.

## Modeling Constraints

Use voltage-coded outputs and transition-shaped edges. Do not use a packed bus,
change the bit order, omit inversion, update on falling edges, or hard-code
testbench clock times.

## Output Contract

Return exactly one source artifact named `dac7_code_generator.va`.
