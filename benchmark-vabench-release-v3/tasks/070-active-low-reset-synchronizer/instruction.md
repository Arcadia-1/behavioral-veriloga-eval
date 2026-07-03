# Active Low Reset Synchronizer

## Task Contract

Implement `reset_sync_active_low.va`, a two-stage voltage-coded reset synchronizer with immediate active-low assertion and synchronous release.

## Form-Specific Requirements

- This is a DUT/support-component task: implement only the requested Verilog-A source artifact.
- Do not generate a Spectre testbench or checker.
- Preserve the public module name, port order, port directions, and parameter names.
- Treat any public validation harness as an observable use case, not as values to hard-code into the DUT.

## Public Verilog-A Interface

```verilog
module reset_sync_active_low(clk, rst_n, sync_rst_n);
```

Inputs are `clk` and `rst_n`. Output is `sync_rst_n`. All ports are electrical.

## Public Parameter Contract

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vdd` | `0.9` | Logic-high output voltage. |
| `vth` | `0.45` | Decision threshold for voltage-coded digital inputs. |
| `tr` | `20p` | Output transition rise/fall smoothing time. |

## Required Behavior

- Treat `rst_n` low as reset asserted and `rst_n` high as reset inactive.
- Assert the synchronized reset output low immediately when `rst_n` crosses low.
- On rising `clk` crossings while `rst_n` is high, release `sync_rst_n` high only after two inactive reset samples.
- If `rst_n` is low on a clock edge, keep both synchronizer stages reset and keep `sync_rst_n` low.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Treat voltage-coded logic low as near 0 V and logic high as near `vdd`.
- Use `transition(...)` or equivalent smooth voltage contributions for driven logic outputs.
- Do not instantiate transistor-level devices, use current-branch contributions, AC/noise analysis, checker logic, private test hooks, or simulator-private side channels.
- Use event state for the two synchronizer stages and the asynchronous assertion edge.

## Output Contract

Return exactly one complete Verilog-A source file named `reset_sync_active_low.va`.
