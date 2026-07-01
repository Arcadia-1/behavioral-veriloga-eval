# Final Step Average Metric File

Implement one behavioral Verilog-A DUT file named `final_step_average_metric_file.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module final_step_average_metric_file (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `@(final_step)` and file system tasks to publish a deterministic final average metric.

Use voltage-coded logic with `vth = 0.45` V and `vhi = 0.9` V.

On every rising crossing of `clk` through `vth`:

- if `rst` is high, clear the sample count, sum, average, `out`, and `metric`
- otherwise accumulate the current `vin` sample into `sum_q`
- compute `avg_q = sum_q / count_q`
- drive `out = avg_q`
- drive `metric = avg_q / vhi`, capped to the range `[0, 1]`

A rising `rst` event must also clear the running average immediately. During `@(final_step)`, write exactly one file named `candidate.out` with the format:

```text
count=<integer> avg=<real> metric=<real>
```

For the hidden testbench, the first clock edge occurs while reset is high and must not contribute to the average. Four later post-reset samples must produce `candidate.out` with `count=4 avg=0.450 metric=0.500`. Use `$fopen`, `$fwrite`, and `$fclose`. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `final_step_average_metric_file.va`. Do not generate a Spectre testbench for this task.
