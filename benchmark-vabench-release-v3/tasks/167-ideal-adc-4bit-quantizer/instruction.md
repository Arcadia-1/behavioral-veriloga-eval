# Ideal ADC 4bit Quantizer

Implement the Verilog-A DUT `ideal_adc_4bit_quantizer` in `ideal_adc_4bit_quantizer.va`.

## Public Interface

The module port order is:

```text
vclk, vip, vin, digital
```

All ports are electrical. `vip` and `vin` form the differential analog input, `vclk` is the sampling clock, and `digital` is a scalar analog output that carries the quantized code value.

## Public Parameters

- `vref = 1.0`: differential full-scale half range in volts.
- `levels = 16`: number of quantizer output levels.
- `vtrans_clk = 0.5`: rising-edge clock threshold in volts.
- `tdel = 0`, `trise = 20p`, `tfall = 20p`: transition timing for `digital`.

## Functional Contract

On each rising crossing of `vclk` through `vtrans_clk`, sample the differential input voltage `V(vip) - V(vin)`.

Quantize the sample into an unsigned 4-bit code over the differential range `-vref` to `+vref`. Use `levels` uniformly spaced output regions across that range. The code equals the number of interior decision thresholds that the sample strictly exceeds, then clips to `0..levels-1`.

Drive the scalar analog output `digital` to the resulting code value.

## Modeling Constraints

Use voltage-domain Verilog-A behavior only. Do not use current contributions, file I/O, random behavior, or simulator-private side channels.

## Output Contract

Return exactly one source artifact named `ideal_adc_4bit_quantizer.va`. Do not include explanatory prose outside the source artifact contents.
