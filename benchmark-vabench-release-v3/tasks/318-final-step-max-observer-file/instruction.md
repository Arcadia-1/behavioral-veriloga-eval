# Final Step Max Observer File

Implement one behavioral Verilog-A DUT file named `final_step_max_observer_file.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module final_step_max_observer_file (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `@(final_step)` and file system tasks to publish a deterministic final maximum metric.

Use voltage-coded logic with `vth = 0.45` V and `vhi = 0.9` V.

On every rising crossing of `clk` through `vth`:

- if `rst` is high, clear the sample count, maximum value, `out`, and `metric`
- otherwise increment `count_q` and update `max_q` with the current `vin` sample
- drive `out = max_q`
- drive `metric = max_q / vhi`, capped to the range `[0, 1]`

A rising `rst` event must also clear the maximum observer immediately. During `@(final_step)`, write exactly one file named `candidate.out` with the format:

```text
count=<integer> max=<real> metric=<real>
```

For the hidden testbench, the first clock edge occurs while reset is high and must not contribute. Four later post-reset samples must produce `candidate.out` with `count=4 max=0.810 metric=0.900`. Use `$fopen`, `$fwrite`, and `$fclose`. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `final_step_max_observer_file.va`. Do not generate a Spectre testbench for this task.
