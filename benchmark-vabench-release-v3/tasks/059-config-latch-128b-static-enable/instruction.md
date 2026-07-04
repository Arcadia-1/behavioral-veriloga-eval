# Config Latch 128b Static Enable

## Task Contract

Implement `config_latch_128b.va`, a wide static enable-gated configuration bus helper for AMS testbenches and behavioral support flows.

## Form-Specific Requirements

- This is a DUT/support-component task: implement only the requested Verilog-A source artifact.
- Do not generate a Spectre testbench or checker.
- Preserve the public module name, port order, port directions, and parameter names.
- Treat any public validation harness as an observable use case, not as values to hard-code into the DUT.

## Public Verilog-A Interface

```verilog
module config_latch_128b(en, d, q);
    input en;
    input [127:0] d;
    output [127:0] q;
```

All ports are electrical.

## Public Parameter Contract

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vdd` | `0.9` | Logic-high output voltage. |
| `vth` | `0.45` | Decision threshold for voltage-coded digital inputs. |
| `tr` | `20p` | Output transition rise/fall smoothing time. |

## Required Behavior

- Treat `en` and `d[127:0]` as voltage-coded logic using `vth`.
- When `en` is high, drive each `q[N]` to the corresponding `d[N]` logic value.
- When `en` is low, drive every `q[N]` low.
- Do not add storage or clocking behavior; the public interface defines a static enable gate.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Treat voltage-coded logic low as near 0 V and logic high as near `vdd`.
- Use `transition(...)` or equivalent smooth voltage contributions for driven logic outputs.
- Do not instantiate transistor-level devices, use current-branch contributions, AC/noise analysis, checker logic, private test hooks, or simulator-private side channels.
- Compact loop-based Verilog-A is preferred for the 128-bit bus.

## Output Contract

Return exactly one complete Verilog-A source file named `config_latch_128b.va`.
