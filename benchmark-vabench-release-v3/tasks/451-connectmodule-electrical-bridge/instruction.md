# Connectmodule Electrical Bridge

Implement one behavioral Verilog-A/AMS source file named `connectmodule_electrical_bridge.vams`.

## Interface

Use the exact Verilog-AMS connectmodule interface shown in the starter file. This is a mixed-signal connection-language candidate, not part of the ordinary behavioral-event certification layer.

## Required Feature

Declare a connectmodule bridge for mixed-signal connection behavior.

## Required Behavior

Required behavior:

- declare a `connectmodule`;
- use electrical input/output ports;
- include a behavioral voltage bridge from input to output;
- keep current contributions out of the task.

Return exactly one source artifact named `connectmodule_electrical_bridge.vams`.
