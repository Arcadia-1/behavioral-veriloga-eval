# String Mode Tagged Log

## Task Contract

Implement one behavioral Verilog-A source file named `string_mode_tagged_log.va`.

## Form-Specific Requirements

Use `$sformat` to create mode-tagged log text for `$strobe`. For Spectre compatibility, call `$sformat` in task form with a destination string, for example `$sformat(label_q, "mode=%0d vin=%0.3f", count_q, V(vin));`. Do not assign the return value of `$sformat`.

## Public Verilog-A Interface

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

## Public Parameter Contract

Use voltage-coded logic with `vth = 0.45` V and high outputs near `vhi = 0.9` V. Drive output transitions with rise/fall time `tr = 200p`. These values may be implemented as compatible Verilog-A parameters or internal constants.

## Required Behavior

- Declare a string state variable such as `label_q`.
- Initialize `out_v`, `metric_v`, and `count_q` at `initial_step`.
- On each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high.
- Otherwise set `out_v` to `vhi` when `V(vin) > vth`, else `0.0`.
- Set `metric_v` to the current `count_q` value before incrementing it.
- Format `label_q` with text that includes the count or mode tag and the input value.
- Call `$strobe("%s", label_q)` or an equivalent `$strobe` call using the formatted label.
- Increment `count_q` after logging.

## Modeling Constraints

Keep the model behavioral and do not introduce current contributions. Drive `out` and `metric` with `transition(..., 0, tr, tr)`. The formatted string and strobe are simulator side effects and must not change the voltage-domain output contract.

## Output Contract

Return exactly one source artifact named `string_mode_tagged_log.va`.
