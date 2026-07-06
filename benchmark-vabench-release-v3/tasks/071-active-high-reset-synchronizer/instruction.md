# Active High Reset Synchronizer

## Task Contract

Implement the requested Verilog-A artifact for `Active High Reset Synchronizer`.
- Form: `dut`
- Level: `L1`
- Category: `testbench_utility_modules`
- Target artifact(s): `reset_sync_active_high.va`

Implement `reset_sync_active_high.va`, a two-stage voltage-coded reset synchronizer with immediate active-high assertion and synchronous release.

- This is a DUT/support-component task: implement only the requested Verilog-A source artifact.
- Do not generate a Spectre testbench or validation harness.
- Preserve the public module name, port order, port directions, and parameter names.
- Treat any public validation harness as an observable use case, not as values to hard-code into the DUT.

## Public Verilog-A Interface

```verilog
module reset_sync_active_high(clk, rst, sync_rst);
```

Inputs are `clk` and `rst`. Output is `sync_rst`. All ports are electrical.

## Public Parameter Contract

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vdd` | `0.9` | Logic-high output voltage. |
| `vth` | `0.45` | Decision threshold for voltage-coded digital inputs. |
| `tr` | `20p` | Output transition rise/fall smoothing time. |

## Required Behavior

- Treat `rst` high as reset asserted and `rst` low as reset inactive.
- Assert the synchronized reset output high immediately when `rst` crosses high.
- On rising `clk` crossings while `rst` is low, release `sync_rst` low only after two inactive reset samples.
- If `rst` is high on a clock edge, keep both synchronizer stages reset and keep `sync_rst` high.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Treat voltage-coded logic low as near 0 V and logic high as near `vdd`.
- Use `transition(...)` or equivalent smooth voltage contributions for driven logic outputs.
- Do not instantiate transistor-level devices, use current-branch contributions, AC/noise analysis, validation logic, validation-only hooks, or simulator-specific side channels.
- Use event state for the two synchronizer stages and the asynchronous assertion edge.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete Verilog-A source file named `reset_sync_active_high.va`.
