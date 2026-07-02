# Discontinuity Event Announcement

Implement one Verilog-A source file named `discontinuity_event_announcement.va`.

## Required Feature

Use $discontinuity() in an event body to announce a behavioral discontinuity.

## Required Interface

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

## Required Behavior

- Initialize `out`, `metric`, and an internal event counter to zero.
- On each rising crossing of `clk` through 0.45 V:
  - If `rst` is above 0.45 V, clear `out`, `metric`, and the event counter.
  - Otherwise call `$discontinuity(0)` inside the event body.
  - Then drive `out` to 0.9 V when `vin` is above 0.45 V, otherwise 0 V.
  - Drive `metric` with the pre-increment event counter value and increment the counter.
- Drive `out` and `metric` with `transition(..., 0, 200p, 200p)`.
- Use only voltage-domain contributions; do not use `I(...)`.

Return exactly one source artifact named `discontinuity_event_announcement.va`.
