# Repeat Loop Accumulator

## Task Contract

Implement one behavioral Verilog-A source file named `repeat_loop_accumulator.va`. This is a language-extension/L0 support task for `repeat` loop execution on sampled voltage-domain state, not a standalone core circuit macro.

Use Verilog-A `repeat` loop syntax in the non-reset sampled update path. The loop is the public language feature under review; do not replace it with an unrolled arithmetic expression.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module repeat_loop_accumulator (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Use voltage-coded logic with `vth = 0.45` V and high outputs near `vhi = 0.9` V. Drive output transitions with rise/fall time `tr = 200p`. These values may be implemented as compatible Verilog-A parameters or internal constants.

## Required Behavior

- Declare integer state for `count_q` and `acc_q`.
- Initialize output state and `count_q` at `initial_step`.
- On each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high.
- Otherwise set `acc_q = 0`, execute `repeat (4)`, and add `count_q + 1` on each repeat iteration.
- Set `out_v = vhi` only when `acc_q > 4`, else `0.0`.
- Set `metric_v = acc_q`.
- Increment `count_q` after computing the accumulator.
- Drive `out` and `metric` with `transition(..., 0, tr, tr)`.

## Modeling Constraints

Keep the model behavioral and voltage-domain only. Do not introduce current contributions.

## Output Contract

Return exactly one source artifact named `repeat_loop_accumulator.va`.
