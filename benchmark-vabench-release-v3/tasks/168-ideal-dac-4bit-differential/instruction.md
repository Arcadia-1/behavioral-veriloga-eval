# Ideal DAC 4bit Differential

Implement the Verilog-A DUT `ideal_dac_4bit_differential` in `ideal_dac_4bit_differential.va`.

## Public Interface

The module port order is:

```text
clk, digital, vcm, vop, von
```

All ports are electrical. `digital` is an analog scalar code input, `vcm` is the output common-mode input, and `vop`/`von` are the differential outputs.

## Public Parameters

- `vref = 1.0`: differential full-scale half range in volts.
- `levels = 16`: number of DAC output levels.
- `vtrans_clk = 0.5`: falling-edge clock threshold in volts.
- `tdel = 0`, `trise = 20p`, `tfall = 20p`: transition timing for the outputs.

## Functional Contract

On each falling crossing of `clk` through `vtrans_clk`, read the integer-valued analog code on `digital` and clamp it to `0..levels-1`.

Use a mid-rise differential transfer over the range from just above `-vref` to just below `+vref`. The differential LSB is the full differential span divided by `levels`: code 0 produces `-vref` plus half an LSB, and each one-code increase raises the differential output by one LSB.

The output common mode must track `vcm`: the average of `vop` and `von` follows `vcm`, while the difference `vop - von` carries the DAC output.

Apply the output transition timing to the event-updated differential component. Keep the analog common-mode input outside the `transition(...)` filter so common-mode tracking remains continuous.

## Modeling Constraints

Use voltage-domain Verilog-A behavior only. Do not use current contributions, file I/O, random behavior, or simulator-private side channels.

## Output Contract

Return exactly one source artifact named `ideal_dac_4bit_differential.va`. Do not include explanatory prose outside the source artifact contents.
