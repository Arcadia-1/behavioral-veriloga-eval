# Continuous Zi Nd Filter

## Task Contract

Implement one Verilog-A source file named `continuous_zi_nd_filter.va`.

## Public Verilog-A Interface

```verilog
module continuous_zi_nd_filter(
    input electrical in,
    output electrical out
);
```

## Public Parameter Contract

Use the public parameter names, default values, legal ranges, filenames, and thresholds stated in the required behavior below. Do not add task-private configuration ports or extra configuration parameters.

## Required Behavior

Use zi_nd() as a sampled-data behavioral transfer function.

- Drive `out` using `V(out) <+ zi_nd(V(in), {0.5, 0.5}, {1.0, -0.25}, 10n);`.
- Treat this as a sampled-data continuous-time/dynamic operator task, not an event-only voltage follower.
- This task is staged for `zi_nd()` syntax and simulator-boundary coverage. Full behavior certification requires a dynamic sampled-data solver accuracy contract.

## Modeling Constraints

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `continuous_zi_nd_filter.va`.
