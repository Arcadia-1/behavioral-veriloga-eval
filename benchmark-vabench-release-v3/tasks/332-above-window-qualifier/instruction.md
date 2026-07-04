# Above Window Qualifier

## Task Contract

Implement one behavioral Verilog-A DUT file named `above_window_qualifier.va`.

## Form-Specific Requirements

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Use `above()` and `last_crossing()` to qualify whether two rising threshold crossings arrive inside a bounded timing window.

For Spectre compatibility, call `last_crossing` with the supported crossing-expression and direction arguments, for example `last_crossing(V(vin) - vth, +1)`. Do not use extra tolerance arguments on `last_crossing`.

## Public Verilog-A Interface

```verilog
module above_window_qualifier (
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

- `@(above(V(vin) - vth))` sets a latch.
- Continuously evaluate the latest rising threshold-crossing time with `last_crossing(V(vin) - vth, +1)`.
- On each rising `vin` threshold crossing, compare the current crossing time with the previous rising crossing time.
- When two consecutive rising crossings are separated by at least `120 ns` and at most `260 ns`, drive `metric = vhi`; otherwise drive `metric = 0.0`.
- `@(cross(V(rst) - vth, +1))` clears the latch, metric, and stored crossing time.
- Drive `out = vhi` when the latch is set, otherwise `0.0`.

## Modeling Constraints

Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions. Use `transition(..., 0, tr, tr)` for both outputs.

## Output Contract

Return exactly one source artifact named `above_window_qualifier.va`. Do not generate a Spectre testbench for this task.
