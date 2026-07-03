# String Config Label Select

## Task Contract

Implement one behavioral Verilog-A source file named `string_config_label_select.va`.

## Form-Specific Requirements

Use `$sformat` to select and record configuration labels. For Spectre compatibility, call `$sformat` in task form with a destination string, for example `$sformat(label_q, "cfg=A count=%0d vin=%0.3f", count_q, V(vin));`. Do not assign the return value of `$sformat`.

## Public Verilog-A Interface

```verilog
module string_config_label_select (
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

- Declare a string state variable such as `label_q`.
- Initialize `out_v`, `metric_v`, and `count_q` at `initial_step`.
- On each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high.
- When `mode` is low, select configuration A: set `out_v` to `vhi` when `V(vin) > vth`, else `0.0`; set `metric_v = count_q`; and format a `cfg=A` label.
- When `mode` is high, select configuration B: set `out_v` to `0.0` when `V(vin) > vth`, else `vhi`; set `metric_v = count_q + 10`; and format a `cfg=B` label.
- Increment `count_q` after formatting the selected label.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions. Drive `out` and `metric` with `transition(..., 0, tr, tr)`. The formatted string is observable only through simulator side effects and must not change the voltage-domain output contract.

## Output Contract

Return exactly one source artifact named `string_config_label_select.va`.
