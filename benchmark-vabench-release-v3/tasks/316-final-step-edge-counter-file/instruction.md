# Final Step Edge Counter File

## Task Contract

Implement one behavioral Verilog-A DUT file named `final_step_edge_counter_file.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Public Verilog-A Interface

```verilog
module final_step_edge_counter_file (
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

Use `@(final_step)` and file system tasks to publish a deterministic final edge-count metric.

Use voltage-coded logic with `vth = 0.45` V and `vhi = 0.9` V.

On every rising crossing of `clk` through `vth`:

- if `rst` is high, clear the edge count, `out`, and `metric`
- otherwise increment `count_q` by one
- drive `out = vhi * count_q / 4.0`, capped at `vhi`
- drive `metric = count_q / 4.0`, capped at `1.0`

A rising `rst` event must also clear the outputs immediately. During `@(final_step)`, write exactly one file named `candidate.out` with the format:

```text
count=<integer> metric=<real>
```

Clock events that occur while reset is high must not contribute to the count.
Each accepted post-reset clock edge increments the count and updates the
normalized metric. Use `$fopen`, `$fwrite`, and `$fclose`; do not hard-code
testbench-specific waveform times or sample values. Do not use `I(...)`,
`ddt(...)`, or `idt(...)`.

## Modeling Constraints

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `final_step_edge_counter_file.va`. Do not generate a Spectre testbench for this task.
