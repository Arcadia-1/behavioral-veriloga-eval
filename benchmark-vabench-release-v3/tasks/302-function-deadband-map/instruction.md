# Function Deadband Map

Implement one behavioral Verilog-A DUT file named `function_deadband_map.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module function_deadband_map (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use a user-defined function to implement deadband mapping.

Use voltage-coded logic with `vth = 0.45` V and high outputs near `0.9` V. The hidden evaluator samples `out` and `metric` under deterministic voltage-domain stimulus and checks the language feature named by this task.

## Output

Return exactly one source artifact named `function_deadband_map.va`. Do not generate a Spectre testbench for this task.
