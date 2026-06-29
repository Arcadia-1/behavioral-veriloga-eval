# Sine Periodic Voltage Source

Implement `multitone.va` in Verilog-A.

## Interface

Declare module `multitone` with positional port `OUT`. The port is an
electrical output.

## Public Parameter Contract

Provide these overrideable real parameters:

- `f1 = 1.0e6 Hz`, `f2 = 2.0e6 Hz`, `f3 = 3.0e6 Hz`
- `a1 = 0.2 V`, `a2 = 0.1 V`, `a3 = 0.05 V`

## Functional Contract

Drive `OUT` with a three-tone voltage source:

```text
V(OUT) = a1*sin(2*pi*f1*t) + a2*sin(2*pi*f2*t) + a3*sin(2*pi*f3*t)
```

Use `$bound_step(...)` or equivalent timestep guidance based on the highest
tone frequency so the waveform is well resolved in transient simulation.

## Modeling Constraints

Return only `multitone.va`. Do not generate a Spectre testbench or checker
logic. Do not use current contributions, `ddt()`, transistor-level devices,
AC/noise analysis, or simulator-private side channels.
