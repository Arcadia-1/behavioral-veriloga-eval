# Clocked Sine Source

Implement `vin_src.va` in Verilog-A.

## Interface

```verilog
module vin_src(
    input  electrical CLK,
    input  electrical RST_N,
    output electrical VOUT_P,
    output electrical VOUT_N
);
```

## Required Behavior

This is an L2 support-component task for measurement-flow stimulus generation,
not a core circuit-function task. Implement `vin_src.va`, a clocked differential
sine stimulus source that can support composed measurement flows such as
gain-extraction benches.

On each rising crossing of `CLK`, if `RST_N` is high, update `VOUT_P` to a
sampled sine value around `vdd/2`. Keep `VOUT_N` at `vdd/2` as the reference
side. While reset is low, hold both outputs near `vdd/2`.

```text
VOUT_P = vdd/2 + ampl*sin(2*pi*freq*t) + optional deterministic perturbation
VOUT_N = vdd/2
```

Use the public parameters `vdd`, `vth`, `ampl`, `freq`, `sigma`, and `SEED`
where applicable. The important behavioral boundary is that the source is
clocked/sample-held rather than continuously recomputing random values at every
analog evaluation point.

Use `vth` with a default near 0.45 V to interpret the voltage-coded `CLK` and
`RST_N` control inputs, and keep the model pure behavioral Verilog-A. Do not use
transistor-level devices, AC/noise analysis, private test hooks, or
simulator-private side channels.

Only `vin_src.va` is the support component under review; companion modules may
be supplied by the harness for composed-flow evaluation.
