# Rdist Normal Offset Dither

## Task Contract

Implement one behavioral Verilog-A source file named `rdist_normal_offset_dither.va`.
The DUT is a clocked voltage-domain offset-dither model that draws a normal
random offset and exposes both the perturbed output and the raw offset metric.

This is a DUT task. Do not implement a testbench, checker, or simulator-private
helper. The visible Spectre netlist is a public validation scenario, not part of
the DUT implementation.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module rdist_normal_offset_dither (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Use `vth` as the clock/reset decision threshold with default value `0.45`.
Use `tr` as the output transition rise/fall time with default value `200p`.
Initialize the internal integer seed to `393`. The random draw values themselves
are determined by the simulator's seeded `$rdist_normal` implementation and
must not be hard-coded as numeric constants.

## Required Behavior

On `initial_step`, initialize the output state, metric state, counters, and
random state to zero except for the internal seed.

On each rising crossing of `clk` through `vth`:

- if `rst > vth`, clear `out` and `metric` back to zero;
- otherwise draw one normal random offset with `$rdist_normal(seed_q, 0.0, 0.05)`;
- report that offset on `metric`;
- drive `out` to the sampled input voltage plus `0.01` times the reported metric.

## Modeling Constraints

Keep the model behavioral and voltage-domain only. Use `cross(...)` for the
clocked update and `transition(...)` for the output and metric drives. Do not
introduce current contributions or hard-code a fixed random sequence.

## Output Contract

Return exactly one source artifact named `rdist_normal_offset_dither.va`.
