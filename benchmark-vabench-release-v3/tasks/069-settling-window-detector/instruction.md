# Settling Window Detector

## Task Contract

Implement the requested Verilog-A artifact for `Settling Window Detector`.
- Form: `dut`
- Level: `L1`
- Category: `testbench_utility_modules`
- Target artifact(s): `settling_window_detector.va`

Implement `settling_window_detector.va`, a voltage-domain instrumentation helper that detects when an analog signal has stayed inside a target tolerance window for a required hold time.

- This is a DUT/support-component task: implement only the requested Verilog-A source artifact.
- Do not generate a Spectre testbench or validation harness.
- Preserve the public module name, port order, port directions, and parameter names.
- Treat any public validation harness as an observable use case, not as values to hard-code into the DUT.

## Public Verilog-A Interface

```verilog
module settling_window_detector(vin, target, tol, settled, t_code0, t_code1, t_code2, t_code3, t_code4, t_code5, t_code6, t_code7);
```

Inputs are `vin`, `target`, and `tol`. Outputs are `settled` and `t_code0` through `t_code7`. All ports are electrical.

## Public Parameter Contract

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vdd` | `0.9` | Logic-high output voltage. |
| `vth` | `0.45` | Decision threshold for voltage-coded digital inputs. |
| `tr` | `20p` | Output transition rise/fall smoothing time. |

## Required Behavior

- Treat the input as in-window when `abs(V(vin) - V(target)) <= V(tol)`.
- When the signal first enters the window, record the entry time and drive `settled` low.
- If the signal leaves the window, clear the entry state, drive `settled` low, and clear the time code.
- Assert `settled` only after the signal has remained continuously in-window for at least 20 ns.
- Drive `t_code[7:0]` to `round(entry_time / 1 ns)`, saturated to the 8-bit range, with `t_code0` as the least significant bit.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Treat voltage-coded logic low as near 0 V and logic high as near `vdd`.
- Use `transition(...)` or equivalent smooth voltage contributions for driven logic outputs.
- Do not instantiate transistor-level devices, use current-branch contributions, AC/noise analysis, validation logic, validation-only hooks, or simulator-specific side channels.
- Keep continuous window qualification and the stored entry time consistent; do not report settled during the initial hold interval.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete Verilog-A source file named `settling_window_detector.va`.
