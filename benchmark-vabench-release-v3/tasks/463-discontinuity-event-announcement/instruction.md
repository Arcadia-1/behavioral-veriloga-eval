# Discontinuity Event Announcement

## Task Contract

Implement one Verilog-A source file named `discontinuity_event_announcement.va`. The task is an L0/support row for using `$discontinuity()` inside a sampled event body.

This is a DUT task for simulator-control semantics. It is not a standalone comparator; the thresholded output is the observable carrier for the discontinuity event.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module discontinuity_event_announcement (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Declare `parameter real vth = 0.45`, `parameter real vhi = 0.9`, and `parameter real tr = 200p`. `vth` is the clock/reset/input threshold, `vhi` is the high output level, and `tr` is the transition rise/fall time.

## Required Behavior

Initialize `out`, `metric`, and an internal event counter to zero. On each rising crossing of `clk` through `vth`, clear the state when `rst > vth`; otherwise call `$discontinuity(0)`, drive `out` to `vhi` when `V(vin) > vth` and to zero otherwise, drive `metric` with the pre-increment event counter value, and then increment the counter.

## Modeling Constraints

Place `$discontinuity(0)` in the event body, not in a continuous expression. Drive `out` and `metric` with `transition(..., 0, tr, tr)`. Use only voltage-domain contributions and do not use `I(...)`.

## Output Contract

Return exactly one source artifact named `discontinuity_event_announcement.va`.
