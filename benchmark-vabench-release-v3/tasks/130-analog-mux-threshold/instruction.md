# Analog Mux Threshold

## Task Contract

Implement a voltage-domain threshold-controlled analog multiplexer.

- Form: `dut`
- Level: `L1`
- Category: mixed-signal analog routing
- Target artifact: `analog_mux_threshold.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`analog_mux_threshold.va` must declare:

```verilog
module analog_mux_threshold(vin1, vin2, vsel, vout);
input vin1, vin2, vsel;
output vout;
electrical vin1, vin2, vsel, vout;
```

## Public Parameter Contract

- `vth = 0.45`: selection threshold in volts. Testbenches may override it.

## Required Behavior

Interpret `vsel` as a single-ended analog control voltage. When `V(vsel)` is
strictly above `vth`, drive `vout` with `V(vin1)`. Otherwise drive `vout` with
`V(vin2)`.

The selected input must update for both rising and falling crossings of the
threshold, and the initial selection must reflect the current `vsel` value.

## Modeling Constraints

Use deterministic voltage-domain behavior. Do not latch the selected input, add
gain, add filtering, create current contributions, or hard-code testbench
waveform times.

## Output Contract

Return exactly one source artifact named `analog_mux_threshold.va`.
