# Slew Asymmetric Rise Fall

## Task Contract

Implement one behavioral Verilog-A DUT file named `slew_asymmetric_rise_fall.va`. The DUT switches between high and low voltage targets while enforcing intentionally asymmetric rising and falling slew-rate limits.

This is a DUT-only Verilog-A modeling task. The supplied testbenches are verification scenarios; do not hard-code their stop times, sample times, or waveform breakpoints into the DUT.

## Public Verilog-A Interface

```verilog
module slew_asymmetric_rise_fall (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

- `vth = 0.45` V is the reset, clock, and mode threshold.
- `rise_rate = 8.0e8` V/s is the positive output slew-rate limit.
- `fall_rate = 2.0e8` V/s is the positive magnitude of the falling slew-rate limit. Cadence Verilog-A `slew(expr, SRpos, SRneg)` expects `SRneg` to be negative, so use `-fall_rate` as the third argument.

## Required Behavior

On reset, clear target `out` and `metric` to zero. On each rising crossing of `clk` through `vth` while reset is low:

- if `mode` is low, set target `out = 0.80`
- if `mode` is high, set target `out = 0.10`
- set target `metric = target_out / 0.80`

Both `out` and `metric` must rise faster than they fall. The falling ramp must remain slew-limited after a high-to-low target change.

## Modeling Constraints

Use pure voltage-domain behavioral Verilog-A. Do not instantiate devices, do not drive `I(...)` branch contributions, and do not use `ddt(...)` or `idt(...)`. Drive the public outputs with `slew(target, rise_rate, -fall_rate)`, not with an immediate assignment or `transition()`.

## Output Contract

Return exactly one source artifact named `slew_asymmetric_rise_fall.va`. Do not generate a Spectre testbench for this task.
