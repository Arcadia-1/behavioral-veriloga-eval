# Connectrules Electrical Map

Implement one behavioral Verilog-A/AMS source file named `connectrules_electrical_map.vams`.

## Interface

Use the exact Verilog-AMS connectrules/connectmodule structure shown in the starter file. This is a mixed-signal connection-language candidate, not part of the ordinary behavioral-event certification layer.

## Required Feature

Declare connectrules mapping between disciplines.

## Required Behavior

Required behavior:

- declare a `connectrules` block;
- map an electrical-to-electrical connection through a named connectmodule;
- define the referenced `connectmodule`;
- include a minimal module artifact so the file has a concrete top-level symbol;
- keep current contributions out of the task.

Return exactly one source artifact named `connectrules_electrical_map.vams`.
