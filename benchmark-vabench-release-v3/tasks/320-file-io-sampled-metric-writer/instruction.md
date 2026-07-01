# File Io Sampled Metric Writer

Implement one behavioral Verilog-A DUT file named `file_io_sampled_metric_writer.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module file_io_sampled_metric_writer (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use file I/O system tasks to write one sampled metric record per accepted clock event.

Use voltage-coded logic with `vth = 0.45` V and `vhi = 0.9` V.

At `initial_step`, open a file named `samples.out` for writing. A rising `rst` event must clear the sample count, `out`, and `metric`.

On each rising crossing of `clk` through `vth` while reset is low:

- increment `count_q`
- sample `vin`
- drive `out = vin`
- drive `metric = vin / vhi`, capped to `[0, 1]`
- write exactly one line to `samples.out` using `$fwrite`:

```text
sample=<integer> value=<real> metric=<real>
```

During `@(final_step)`, close the file with `$fclose`. The first hidden clock edge occurs while reset is high and must not write a sample record. Four later post-reset samples must write the values `0.18`, `0.36`, `0.72`, and `0.54`, with metrics `0.20`, `0.40`, `0.80`, and `0.60`. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `file_io_sampled_metric_writer.va`. Do not generate a Spectre testbench for this task.
