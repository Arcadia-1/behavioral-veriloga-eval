# Clocked ADC Quantizer

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Data Converter Models
- Domain: voltage-domain behavioral Verilog-A
- Target artifact: `flash_adc_3b.va`
- Required module: `flash_adc_3b`

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Do not generate a Spectre testbench, checker, waveform post-processor, or extra support file.

## Public Verilog-A Interface

`flash_adc_3b.va` declares module `flash_adc_3b` with positional ports:

```verilog
module flash_adc_3b(VDD, VSS, VIN, CLK, DOUT2, DOUT1, DOUT0);
```

All ports are electrical. `VDD` and `VSS` are output logic rails, `VIN` is the
analog input, `CLK` is the sampling clock, and `DOUT2`, `DOUT1`, and `DOUT0`
are voltage-coded output bits from MSB to LSB.

## Public Parameter Contract

- `vrefp = 0.9 V`: upper endpoint of the ADC input range.
- `vrefn = 0.0 V`: lower endpoint of the ADC input range.
- `vth = 0.45 V`: rising-clock threshold.
- `tedge = 100p`: transition smoothing time for the output bits.

## Required Behavior

On each rising crossing of `CLK` through `vth`, quantize `VIN` into one of
eight uniform bins spanning `vrefn` to `vrefp`. Clamp the resulting code to the
inclusive range 0 through 7 and hold that sampled code until the next rising
clock edge.

Drive `DOUT2`, `DOUT1`, and `DOUT0` as the binary representation of the held
code, using `VDD` for logic 1 and `VSS` for logic 0. The public observable
waveforms are `vin`, `clk`, `dout2`, `dout1`, and `dout0`.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A with event-driven sampling and smoothed
output transitions. Do not use current contributions, transistor-level devices,
`ddt()`, `idt()`, or testbench-specific timing constants inside the DUT.

## Output Contract

Return exactly one complete Verilog-A source artifact named `flash_adc_3b.va`.
Do not include explanatory prose outside the source artifact contents.
