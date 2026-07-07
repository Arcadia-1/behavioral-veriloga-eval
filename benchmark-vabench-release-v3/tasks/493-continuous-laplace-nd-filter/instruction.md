# Continuous Laplace Nd Filter

## Task Contract

Implement one Verilog-A source file named `continuous_laplace_nd_filter.va`.

## Public Verilog-A Interface

```verilog
module continuous_laplace_nd_filter(
    input electrical in,
    output electrical out
);
```

## Public Parameter Contract

Use the public parameter names, default values, legal ranges, filenames, and thresholds stated in the required behavior below. Do not add task-private configuration ports or extra configuration parameters.

## Required Behavior

Use laplace_nd() as a continuous-time behavioral transfer function.

- Drive `out` using `V(out) <+ laplace_nd(V(in), {1.0}, {1.0, 1e-6});`.
- Treat this as a continuous-time behavioral transfer-function task, not an event-only voltage follower.
- This task is staged for continuous-time operator syntax and simulator-boundary coverage. Full behavior certification requires a dynamic-solver accuracy contract.

## Modeling Constraints

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `continuous_laplace_nd_filter.va`.
