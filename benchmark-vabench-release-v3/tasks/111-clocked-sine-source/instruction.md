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

Public parameters:

- `vdd = 0.9 V`: positive output common-mode supply parameter.
- `vth = 0.45 V`: voltage threshold for `CLK` and `RST_N`.
- `ampl = 0.15 V`: sine amplitude before any testbench override.
- `freq = 300 kHz`: sine frequency before any testbench override.
- `sigma = 0.01 V`: deterministic random perturbation scale.
- `SEED = 0`: seed passed to `$rdist_normal(SEED, 0, 1)`.

Sample the sine and random perturbation only on rising `CLK` crossings after
reset release. `VOUT_N` should remain at `vdd/2`; the perturbation is applied
to the positive side so the composed measurement flow sees a repeatable
single-ended stimulus component.

Use `vth` with a default near 0.45 V to interpret the voltage-coded `CLK` and
`RST_N` control inputs, and keep the model pure behavioral Verilog-A. Do not use
transistor-level devices, AC/noise analysis, private test hooks, or
simulator-private side channels.

Only `vin_src.va` is the support component under review; companion modules may
be supplied by the harness for composed-flow evaluation.
