# String Mode Tagged Log

Implement one behavioral Verilog-A source file named `string_mode_tagged_log.va`.

## Interface

Use this exact module interface:

```verilog
module string_mode_tagged_log (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

Keep the model behavioral and do not introduce current contributions.

## Required Behavior

Use $sformat() to create mode-tagged log text for $strobe().

Required behavior:

- declare a string state variable such as `label_q`;
- initialize `out_v`, `metric_v`, and `count_q` at `initial_step`;
- on each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high;
- otherwise set `out_v` to `vhi` when `V(vin) > vth`, else 0.0;
- set `metric_v` to the current `count_q` value before incrementing it;
- assign `label_q = $sformat("mode=%0d vin=%0.3f", count_q, V(vin))` or an equivalent format that includes both mode/count and input value;
- call `$strobe("%s", label_q)` or an equivalent `$strobe` call using the formatted label;
- increment `count_q` after logging;
- drive `out` and `metric` with `transition(...)`.

Return exactly one source artifact named `string_mode_tagged_log.va`.
