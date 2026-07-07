# Event Or Cross Timer

## Task Contract

Implement one behavioral Verilog-A source file named `event_or_cross_timer.va`. This is a language-extension/L0 support task for a flat analog event expression that combines `cross()` and `timer()` with `or`, not a standalone core circuit macro.

Use one analog event statement whose sensitivity expression is `cross(V(clk) - vth, +1) or timer(1n, 1n)`. Both event sources must execute the same sampled update body.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module event_or_cross_timer(
    input electrical vin,
    input electrical clk,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Use threshold `vth = 0.45` V for the clock crossing and transition rise/fall time `tr = 200p`. Use a periodic timer with first event at `1n` and period `1n`.

## Required Behavior

- Initialize `out_v` and `event_count` at `initial_step`.
- On either event source, sample `V(vin)` into `out_v`.
- Increment `event_count` once per event body execution.
- Drive `out` from `out_v` and `metric` from `event_count` with `transition(..., 0, tr, tr)`.

## Modeling Constraints

Keep the model behavioral and voltage-domain only. Do not introduce current contributions or split the required event expression into separate event statements.

## Output Contract

Return exactly one source artifact named `event_or_cross_timer.va`.
