# Bus Splitter 256 To 16x16

## Task Contract

Implement the requested Verilog-A artifact for `Bus Splitter 256 To 16x16`.
- Form: `dut`
- Level: `L1`
- Category: `testbench_utility_modules`
- Target artifact(s): `bus_split_256_to_16x16.va`

Implement `bus_split_256_to_16x16.va`, a voltage-coded bus reshaping helper that splits one 256-bit configuration bus into sixteen 16-bit blocks.

- This is a DUT/support-component task: implement only the requested Verilog-A source artifact.
- Do not generate a Spectre testbench or validation harness.
- Preserve the public module name, port order, port directions, and parameter names.
- Treat any public validation harness as an observable use case, not as values to hard-code into the DUT.

## Public Verilog-A Interface

```verilog
module bus_split_256_to_16x16(in_bus, out0, out1, out2, out3, out4, out5, out6, out7, out8, out9, out10, out11, out12, out13, out14, out15);
    input [255:0] in_bus;
    output [15:0] out0, out1, out2, out3, out4, out5, out6, out7, out8, out9, out10, out11, out12, out13, out14, out15;
```

All ports are electrical.

## Public Parameter Contract

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vdd` | `0.9` | Logic-high output voltage. |
| `vth` | `0.45` | Decision threshold for voltage-coded digital inputs. |
| `tr` | `20p` | Output transition rise/fall smoothing time. |

## Required Behavior

- Treat `in_bus[255:0]` as voltage-coded logic using `vth`.
- Map input bit `N` to output block `N/16` and bit `N%16` without inversion or reordering.
- Examples: `in_bus[0]` drives `out0[0]`, `in_bus[15]` drives `out0[15]`, and `in_bus[255]` drives `out15[15]`.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Treat voltage-coded logic low as near 0 V and logic high as near `vdd`.
- Use `transition(...)` or equivalent smooth voltage contributions for driven logic outputs.
- Do not instantiate transistor-level devices, use current-branch contributions, AC/noise analysis, validation logic, validation-only hooks, or simulator-specific side channels.
- Compact loop-based Verilog-A is preferred; do not manually expand 256 scalar assignments unless required by the simulator subset.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete Verilog-A source file named `bus_split_256_to_16x16.va`.
