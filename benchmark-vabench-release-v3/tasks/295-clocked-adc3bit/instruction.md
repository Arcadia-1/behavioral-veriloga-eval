# Clocked ADC 3bit Bit Bus

Implement the Verilog-A DUT `clocked_adc3bit` in `clocked_adc3bit.va`.

## Public Interface

The module port order is:

```text
vd2, vd1, vd0, vin, vclk
```

All ports are electrical. `vin` is the analog input, `vclk` is the sampling clock, `vd2` is the MSB output bit, and `vd0` is the LSB output bit.

## Public Parameters

- `vth_clk = 0.45`: rising-edge clock threshold in volts.
- `vh = 0.9`: output high rail in volts.
- The output low rail is 0.0 V.

## Functional Contract

On each rising crossing of `vclk` through `vth_clk`, sample `vin` and quantize the 0 V to 1 V input range into eight uniform lower-inclusive bins. Values below 0 V clip to code 0, values at or above 1 V clip to code 7, and interior bin boundaries occur at multiples of one eighth of a volt.

Drive `vd2`, `vd1`, and `vd0` as the binary representation of the sampled code, using `vh` for bit 1 and 0.0 V for bit 0.

This task evaluates a clocked ADC with explicit bit-bus voltage outputs. It is distinct from scalar-code ADC tasks whose output is a single analog code value.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A behavior only. Do not use current contributions, file I/O, random behavior, or simulator-private side channels.

## Output Contract

Return exactly one source artifact named `clocked_adc3bit.va`. Do not include explanatory prose outside the source artifact contents.
