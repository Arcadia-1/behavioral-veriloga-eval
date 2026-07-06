# LT Read SAR6B Weighted

## Task Contract

Implement `lt_read_sar6b_weighted.va` as a continuous weighted SAR readout DUT. This row models a source-style 6-input readout where one input is a dummy/present-but-ignored bit.

## Public Verilog-A Interface

Use this exact module signature:

```verilog
module lt_read_sar6b_weighted(d0, d1, d2, d3, d4, d5, vout, gnd);
```

All ports are electrical. `d5..d1` are active weighted decision inputs, `d0` is present but ignored by this source-style readout, `vout` is the analog output, and `gnd` is the supplied reference node.

## Public Parameter Contract

Provide these overrideable public parameters:

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vth` | `0.45` | Logic threshold for decision inputs. |
| `vref` | `0.9` | Bipolar offset and weighting reference. |

## Required Behavior

Continuously drive:

```text
vout = -vref + vref * (d5 + d4/2 + d3/4 + d2/8 + d1/16)
```

where each `d` term is `1` when the corresponding input voltage is above `vth` and `0` otherwise. `d0` must not affect the output.

## Modeling Constraints

Use voltage-domain Verilog-A only. Do not add clocked state, current contributions, transistor devices, checker logic, out-of-band test hooks, simulator side channels, or hard-coded testbench sample times.

## Output Contract

Return exactly one source artifact named `lt_read_sar6b_weighted.va`.
