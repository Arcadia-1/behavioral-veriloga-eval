# Display Strobe Event Logger

Implement one behavioral Verilog-A DUT file named `display_strobe_event_logger.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module display_strobe_event_logger (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use final_step and file/display system tasks for a deterministic metric.

Use voltage-coded logic with `vth = 0.45` V and high outputs near `0.9` V. The hidden evaluator samples `out` and `metric` under deterministic voltage-domain stimulus and checks the language feature named by this task.

## Output

Return exactly one source artifact named `display_strobe_event_logger.va`. Do not generate a Spectre testbench for this task.
