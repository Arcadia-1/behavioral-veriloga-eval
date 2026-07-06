# Period Meter 16b

## Task Contract

Implement the requested Verilog-A artifact for `Period Meter 16b`.
- Form: `dut`
- Level: `L1`
- Category: `testbench_utility_modules`
- Target artifact(s): `period_meter_16b.va`

Implement `period_meter_16b.va`, a voltage-domain instrumentation helper that measures rising-edge-to-rising-edge clock period and reports it as a 16-bit digital code.

- This is a DUT/support-component task: implement only the requested Verilog-A source artifact.
- Do not generate a Spectre testbench or validation harness.
- Preserve the public module name, port order, port directions, and parameter names.
- Treat any public validation harness as an observable use case, not as values to hard-code into the DUT.

## Public Verilog-A Interface

```verilog
module period_meter_16b(clk_in, valid, period0, period1, period2, period3, period4, period5, period6, period7, period8, period9, period10, period11, period12, period13, period14, period15);
```

Input is `clk_in`. Outputs are `valid` and `period0` through `period15`. All ports are electrical.

## Public Parameter Contract

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vdd` | `0.9` | Logic-high output voltage. |
| `vth` | `0.45` | Decision threshold for voltage-coded digital inputs. |
| `tr` | `20p` | Output transition rise/fall smoothing time. |

## Required Behavior

- Measure the interval between consecutive rising crossings of `clk_in`.
- After the second and later rising edges, compute `round(period / 1 ns)` and saturate to 0 through 65535.
- Drive `period0` as the least significant bit through `period15` as the most significant bit.
- Assert and hold `valid` after a period has been measured, updating the code on later periods.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Treat voltage-coded logic low as near 0 V and logic high as near `vdd`.
- Use `transition(...)` or equivalent smooth voltage contributions for driven logic outputs.
- Do not instantiate transistor-level devices, use current-branch contributions, AC/noise analysis, validation logic, validation-only hooks, or simulator-specific side channels.
- Use event state for the previous edge time, seen-edge flag, measured code, and validity flag.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete Verilog-A source file named `period_meter_16b.va`.
