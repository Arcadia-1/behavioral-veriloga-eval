# DC Aware ADC3bit

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Data Converter Models
- Domain: voltage-domain behavioral Verilog-A
- Target artifact: `dc_aware_adc3bit.va`
- Required module: `dc_aware_adc3bit`

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Model a static, analysis-friendly three-bit ADC without a sampling clock.

## Public Verilog-A Interface

```verilog
module dc_aware_adc3bit(vin, d2, d1, d0);
```

All ports are electrical. `vin` is the analog input. `d2` is the MSB and `d0`
is the LSB of the voltage-coded output word.

## Public Parameter Contract

- `vref = 1.0 V`: input full-scale reference.
- `vh = 0.9 V`: output logic-high voltage.
- `tr = 20p`: output transition smoothing time.

## Required Behavior

Clip `vin` to the 0-to-`vref` range, quantize the clipped value into eight
uniform output codes using bin-floor quantization, and drive `d2..d0` as the
binary representation of that code. The conversion is combinational/static
rather than clocked: the output word should represent the current input level
after transition smoothing, including at the beginning of a transient run.

## Modeling Constraints

Use voltage-domain Verilog-A with smooth output transitions. Do not introduce a
clock, sampling state, test-specific sample times or lookup vectors, current
contributions, `ddt()`, or `idt()`.

## Output Contract

Return exactly one complete Verilog-A source artifact named
`dc_aware_adc3bit.va`. Do not include explanatory prose outside the source
artifact contents.
