# Low Active Enable Decoder 4b

## Task Contract

Implement `low_active_enable_decoder_4b.va`, a voltage-coded active-low one-hot decoder helper for support/control wiring.

## Form-Specific Requirements

- This is a DUT/support-component task: implement only the requested Verilog-A source artifact.
- Do not generate a Spectre testbench or checker.
- Preserve the public module name, port order, port directions, and parameter names.
- Treat any public validation harness as an observable use case, not as values to hard-code into the DUT.

## Public Verilog-A Interface

```verilog
module low_active_enable_decoder_4b(en_n, a0, a1, a2, a3, y0_n, y1_n, y2_n, y3_n, y4_n, y5_n, y6_n, y7_n, y8_n, y9_n, y10_n, y11_n, y12_n, y13_n, y14_n, y15_n);
```

Inputs are `en_n` and address bits `a0` through `a3`. Outputs are active-low `y0_n` through `y15_n`. All ports are electrical.

## Public Parameter Contract

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vdd` | `0.9` | Logic-high output voltage. |
| `vth` | `0.45` | Decision threshold for voltage-coded digital inputs. |
| `tr` | `20p` | Output transition rise/fall smoothing time. |

## Required Behavior

- Treat `en_n` and `a[3:0]` as voltage-coded logic using `vth`.
- Decode `a3:a0` as an unsigned 4-bit address, with `a0` as the least significant bit.
- When `en_n` is low, drive exactly one selected output `yN_n` low and all other outputs high.
- When `en_n` is high, drive all outputs high.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Treat voltage-coded logic low as near 0 V and logic high as near `vdd`.
- Use `transition(...)` or equivalent smooth voltage contributions for driven logic outputs.
- Do not instantiate transistor-level devices, use current-branch contributions, AC/noise analysis, checker logic, private test hooks, or simulator-private side channels.

## Output Contract

Return exactly one complete Verilog-A source file named `low_active_enable_decoder_4b.va`.
