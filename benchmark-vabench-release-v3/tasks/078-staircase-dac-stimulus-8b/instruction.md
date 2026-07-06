# Staircase DAC Stimulus 8b

## Task Contract

Implement the requested Verilog-A artifact for `Staircase DAC Stimulus 8b`.
- Form: `dut`
- Level: `L1`
- Category: `testbench_utility_modules`
- Target artifact(s): `staircase_dac_stimulus_8b.va`

Implement `staircase_dac_stimulus_8b.va`, a deterministic clocked stimulus source that emits both an 8-bit voltage-coded count and a corresponding analog staircase voltage.

- This is a DUT/support-component task: implement only the requested Verilog-A source artifact.
- Do not generate a Spectre testbench or validation harness.
- Preserve the public module name, port order, port directions, and parameter names.
- Treat any public validation harness as an observable use case, not as values to hard-code into the DUT.

## Public Verilog-A Interface

```verilog
module staircase_dac_stimulus_8b(clk, rst, vout, code0, code1, code2, code3, code4, code5, code6, code7);
```

Inputs are `clk` and `rst`. Outputs are analog `vout` and digital-coded `code0` through `code7`. All ports are electrical.

## Public Parameter Contract

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vdd` | `0.9` | Logic-high output voltage. |
| `vth` | `0.45` | Decision threshold for voltage-coded digital inputs. |
| `tr` | `20p` | Output transition rise/fall smoothing time. |

## Required Behavior

- On each rising `clk` crossing, reset the internal 8-bit code to zero if `rst` is high.
- Otherwise increment the code modulo 256.
- Drive `code0` as the least significant bit through `code7` as the most significant bit.
- Drive `vout = vdd * code / 255.0` so the staircase spans from 0 V to `vdd`.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Treat voltage-coded logic low as near 0 V and logic high as near `vdd`.
- Use `transition(...)` or equivalent smooth voltage contributions for driven logic outputs.
- Do not instantiate transistor-level devices, use current-branch contributions, AC/noise analysis, validation logic, validation-only hooks, or simulator-specific side channels.
- Use clocked event state for the internal code; do not infer the code from absolute simulation time.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete Verilog-A source file named `staircase_dac_stimulus_8b.va`.
