# String Swrite Label Builder

## Task Contract

Implement one behavioral Verilog-A source file named `string_swrite_label_builder.va`.

Use `$swrite()` to build an internal string label during clocked updates. This task focuses on string-format side effects that coexist with ordinary voltage-domain outputs; do not add file I/O or console logging for this row.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module string_swrite_label_builder (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Use voltage-coded logic with `vth = 0.45` V and high outputs near `vhi = 0.9` V. Drive output transitions with rise/fall time `tr = 200p`. These values may be implemented as compatible Verilog-A parameters or internal constants. The `mode` input is a public context input; this task does not require mode-dependent voltage behavior.

## Required Behavior

- Declare a string state variable such as `label_q`.
- Initialize `out_v`, `metric_v`, and `count_q` at `initial_step`.
- On each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high.
- Otherwise set `out_v` to `vhi` when `V(vin) > vth`, else `0.0`.
- Set `metric_v` to the current `count_q` value before incrementing it.
- Call `$swrite()` on the same non-reset update path to format a label containing the sample count and metric or input context.
- Increment `count_q` after building the label.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions. Drive `out` and `metric` with `transition(..., 0, tr, tr)`. The formatted string is a simulator side effect and must not change the voltage-domain output contract.

## Output Contract

Return exactly one source artifact named `string_swrite_label_builder.va`.
