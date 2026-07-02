# VA LX ADC Ideal 4b

Implement the Verilog-A DUT `va_lx_adc_ideal_4b` in `va_lx_adc_ideal_4b.va`.

## Public Interface

The module port order is:

```text
vin, clks, d1, d2, d3, d4
```

All ports are electrical. `vin` is the analog input, `clks` is the track/convert clock, `d4` is the MSB, and `d1` is the LSB.

## Public Parameters

- `vdd = 1.0`: input full-scale reference and clock-high voltage in volts.
- The clock threshold is `vdd/2`.
- Output bits use scalar voltage levels 0.0 and 1.0.

## Functional Contract

While `clks` is above `vdd/2`, track the current value of `vin`. On the falling crossing of `clks` through `vdd/2`, convert the last tracked value with a four-step binary-search ADC:

1. Compare against `vdd/2` to decide `d4`.
2. Move the comparison threshold by `vdd/4` toward the selected half range.
3. Compare to decide `d3`, then move by `vdd/8`.
4. Compare to decide `d2`, then move by `vdd/16`.
5. Compare to decide `d1`.

Reset the output bits to zero at initialization and on each rising crossing of `clks` through `vdd/2`.

## Modeling Constraints

Use voltage-domain Verilog-A behavior only. Do not use current contributions, file I/O, random behavior, or simulator-private side channels.

## Output Contract

Return exactly one source artifact named `va_lx_adc_ideal_4b.va`. Do not include explanatory prose outside the source artifact contents.
