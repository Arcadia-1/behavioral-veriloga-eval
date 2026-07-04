# Enable Gated Clock Pulse

## Task Contract

Implement `enable_gated_clock_pulse.va`, a simple voltage-coded enabled clock-level pulse helper for AMS control and testbench timing.

## Form-Specific Requirements

- This is a DUT/support-component task: implement only the requested Verilog-A source artifact.
- Do not generate a Spectre testbench or checker.
- Preserve the public module name, port order, port directions, and parameter names.
- Treat any public validation harness as an observable use case, not as values to hard-code into the DUT.

## Public Verilog-A Interface

```verilog
module enable_gated_clock_pulse(clk, en, pulse);
```

Inputs are `clk` and `en`. Output is `pulse`. All ports are electrical.

## Public Parameter Contract

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vdd` | `0.9` | Logic-high output voltage. |
| `vth` | `0.45` | Decision threshold for voltage-coded digital inputs. |
| `tr` | `20p` | Output transition rise/fall smoothing time. |

## Required Behavior

- Treat `clk` and `en` as voltage-coded logic using `vth`.
- Drive `pulse` high exactly when both `clk` and `en` are high.
- Drive `pulse` low otherwise.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Treat voltage-coded logic low as near 0 V and logic high as near `vdd`.
- Use `transition(...)` or equivalent smooth voltage contributions for driven logic outputs.
- Do not instantiate transistor-level devices, use current-branch contributions, AC/noise analysis, checker logic, private test hooks, or simulator-private side channels.

## Output Contract

Return exactly one complete Verilog-A source file named `enable_gated_clock_pulse.va`.
