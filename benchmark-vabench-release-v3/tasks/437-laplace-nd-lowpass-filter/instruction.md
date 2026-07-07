# Laplace Nd Lowpass Filter

## Task Contract

Implement one behavioral Verilog-A/AMS source file named `laplace_nd_lowpass_filter.va`. This is an L1 voltage-domain analog-operator source task for a continuous-time numerator/denominator low-pass filter.

Use `laplace_nd(V(vin), {1.0}, {1.0, 100n})` as the public operator form for a 100 ns first-order low-pass response. The operator result must be computed in continuous analog context and then sampled by the clocked behavior; do not place the operator call inside the clock event body, reset conditional, loop, or other conditional/event-only context.

## Public Verilog-A Interface

Use the exact module interface from the starter file:

```verilog
module laplace_nd_lowpass_filter (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

The `mode` port is part of the public interface for harness compatibility; it does not need to change the required behavior.

## Public Parameter Contract

Expose the starter parameters `vth`, `vhi`, and `tr` with their starter defaults and units. `vth` is the voltage threshold used for `clk` and `rst`; `vhi` is retained for starter and harness compatibility and does not scale the required operator output; `tr` is the transition edge time for the voltage outputs.

## Required Behavior

The continuous operator value is the first-order low-pass response; each rising `clk` sample copies that filtered value to both `out` and `metric`. If `rst` is above `vth` at a clock sample, clear the sampled output state and metric state to zero. Drive `out` and `metric` as voltage outputs using the sampled real states and `transition(..., 0.0, tr, tr)` smoothing.

## Modeling Constraints

Keep the model voltage-domain only. Do not use current contributions, conservative KCL/MNA branch behavior, simulator-private side channels, file I/O, or checker-only hooks. The analog operator call must remain in continuous analog context so the source is legal standalone Spectre Verilog-A.

## Output Contract

Return exactly one source artifact named `laplace_nd_lowpass_filter.va`.
