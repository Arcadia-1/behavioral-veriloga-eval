# Specify Specparam Delay

Implement one behavioral Verilog-A/AMS source file named `specify_specparam_delay.vams`.

## Interface

Use the exact Verilog/AMS timing interface shown in the starter file. This is an AMS/digital timing-language candidate, not part of the ordinary behavioral-event certification layer.

## Required Feature

Use specify/specparam delay syntax.

## Required Behavior

Required behavior:

- declare a module with logic input/output;
- drive the output from the input;
- include a `specify` block;
- declare a `specparam` delay;
- declare a path delay from input to output.

Return exactly one source artifact named `specify_specparam_delay.vams`.
