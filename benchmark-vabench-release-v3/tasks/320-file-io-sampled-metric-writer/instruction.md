# File Io Sampled Metric Writer

## Task Contract

Implement one behavioral Verilog-A DUT file named `file_io_sampled_metric_writer.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Public Verilog-A Interface

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

## Public Parameter Contract

Use the public parameter names, default values, legal ranges, filenames, and thresholds stated in the required behavior below. Do not add task-private configuration ports or extra configuration parameters.

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

During `@(final_step)`, close the file with `$fclose`. Clock events that occur
while reset is high must not write a sample record. Each accepted post-reset
clock edge must write the current `vin` sample and its normalized metric using
the public line format above. Do not hard-code testbench-specific waveform times
or sample values. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Modeling Constraints

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `file_io_sampled_metric_writer.va`. Do not generate a Spectre testbench for this task.
