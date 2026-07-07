# String Formatted Metric Line

## Task Contract

Implement one behavioral Verilog-A source file named `string_formatted_metric_line.va`.

Use `$swrite()` to build a formatted metric line and append that line to `metric_lines.log` with `$fopen`, `$fwrite`, and `$fclose`. This row is distinct from an internal-only string label because the formatted string is emitted through a file side effect.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module string_formatted_metric_line (
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
- Call `$swrite()` to format a line containing the sample count and metric or input context.
- Append the formatted line to `metric_lines.log` on the same non-reset update path using `$fopen`, `$fwrite`, and `$fclose`.
- Increment `count_q` after formatting and writing the line.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions. Drive `out` and `metric` with `transition(..., 0, tr, tr)`. The file write is a simulator side effect and must not change the voltage-domain output contract.

## Output Contract

Return exactly one source artifact named `string_formatted_metric_line.va`.
