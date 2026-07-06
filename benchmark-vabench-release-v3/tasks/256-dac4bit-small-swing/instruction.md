# DAC4bit Small Swing

## Task Contract

Implement `dac4bit_small_swing.va` as a continuous 4-bit small-swing DAC DUT.

## Public Verilog-A Interface

Use this exact module signature:

```verilog
module dac4bit_small_swing(vd3, vd2, vd1, vd0, vout);
```

All ports are electrical. `vd3` is the most significant bit, `vd0` is the least significant bit, and `vout` is the small-swing analog output.

## Public Parameter Contract

Provide these overrideable public parameters:

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vref` | `20m` | Positive output half-scale. |
| `vtrans` | `0.45` | Logic threshold for `vd3..vd0`. |

## Required Behavior

Continuously decode `vd3..vd0` as an unsigned 4-bit code. Map the code to a centered small-swing output:

```text
vout = vref * (2 * code / 15 - 1)
```

The all-zero code maps to `-vref`, the all-one code maps to `+vref`, and interior codes are uniformly spaced.

## Modeling Constraints

Use voltage-domain Verilog-A only. Do not add clocked state, current contributions, transistor devices, checker logic, out-of-band test hooks, simulator side channels, or hard-coded testbench sample times.

## Output Contract

Return exactly one source artifact named `dac4bit_small_swing.va`.
