# Zi Np Discrete Filter

## Task Contract

Implement one behavioral Verilog-A/AMS source file named `zi_np_discrete_filter.va`. This is an L1 voltage-domain analog-operator source task for a sampled-data numerator/pole filter.

Use `zi_np(V(vin), {0.25}, {0.75, 0.0}, 100n)` as the public operator form for a 100 ns numerator/pole sampled-data low-pass response; the real pole must include its imaginary-part entry. The operator result must be computed in continuous analog context and then sampled by the clocked behavior; do not place the operator call inside the clock event body, reset conditional, loop, or other conditional/event-only context.

## Public Verilog-A Interface

Use the exact module interface from the starter file:

```verilog
module zi_np_discrete_filter (
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

The operator value is the first-order sampled-data low-pass response; each rising `clk` sample copies that filtered value to both `out` and `metric`. If `rst` is above `vth` at a clock sample, clear the sampled output state and metric state to zero. Drive `out` and `metric` as voltage outputs using the sampled real states and `transition(..., 0.0, tr, tr)` smoothing.

## Modeling Constraints

Keep the model voltage-domain only. Do not use current contributions, conservative KCL/MNA branch behavior, simulator-private side channels, file I/O, or checker-only hooks. The analog operator call must remain in continuous analog context so the source is legal standalone Spectre Verilog-A.

## Output Contract

Return exactly one source artifact named `zi_np_discrete_filter.va`.
