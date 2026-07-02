# Do While Loop Accumulator

Implement one behavioral Verilog-A source file named `do_while_loop_accumulator.va`.

## Required Feature

Use `do ... while` loop syntax to accumulate bounded behavioral state.

## Required Interface

```verilog
module do_while_loop_accumulator (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

- Initialize `out`, `metric`, and the internal event counter to zero.
- On each rising crossing of `clk` through 0.45 V:
  - If `rst` is above 0.45 V, clear `out`, `metric`, and the internal event counter.
  - Otherwise use a `do ... while` loop that executes exactly three iterations.
  - In each loop iteration add `count + 1` into a local accumulator, where `count` is the pre-event internal event counter.
  - Drive `metric` with the accumulator value.
  - Drive `out` to 0.9 V when the accumulator is greater than 3, otherwise drive 0 V.
  - Increment the internal event counter by one after computing the accumulator.
- Smooth both output voltages with `transition(..., 0, 200p, 200p)`.
- Do not use current-domain contributions.

Return exactly one source artifact named `do_while_loop_accumulator.va`.
