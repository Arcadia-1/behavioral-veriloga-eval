# Ramp Step Source

Implement `bound_step_period_guard_ref.va` in Verilog-A.

## Interface

Declare module `bound_step_period_guard_ref` with positional ports
`VDD, VSS, guard_out, phase_out`. `VDD` and `VSS` are electrical supply rails;
`guard_out` and `phase_out` are electrical outputs.

## Public Parameter Contract

- `period = 8 ns`: ramp period before any testbench override.
- `pulse_w = 1.5 ns`: guard-pulse high duration before any testbench override.
- `points_per_period = 16.0`: timestep guidance for resolving the ramp.
- `tedge = 40 ps`: guard output transition time.

## Functional Contract

Generate a periodic normalized phase ramp and a guard pulse. Within each
period, `phase_out` ramps from `VSS` toward `VDD` and wraps at the start of the
next period. `guard_out` is high only during the first `pulse_w` seconds of
each period and low otherwise. The output levels should track the supplied rail
voltages, not hard-coded absolute rails.

Using `$bound_step(period / points_per_period)` is allowed to keep the narrow
guard pulse observable, but the scored behavior is the ramp wrap and guard
timing.

## Modeling Constraints

Return only `bound_step_period_guard_ref.va`. Do not generate a Spectre
testbench or checker logic. Do not use current contributions, `ddt()`, `idt()`,
transistor-level devices, AC/noise analysis, or simulator-private side
channels.
