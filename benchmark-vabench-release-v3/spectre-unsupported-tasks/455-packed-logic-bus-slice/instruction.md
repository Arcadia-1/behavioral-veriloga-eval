# Packed Logic Bus Slice

Implement one behavioral Verilog-A/AMS source file named `packed_logic_bus_slice.vams`.

## Interface

Use the exact Verilog-AMS digital interface shown in the starter file. This is an AMS/digital mixed-signal candidate, not part of the electrical behavioral-event certification layer.

## Required Feature

Use a packed-style logic bus with slices and concatenation.

## Required Behavior

Required behavior:

- declare an 8-bit logic input bus;
- declare a 4-bit logic output bus;
- use bit select or part select on the input bus;
- use concatenation to build the output bus;
- continuously assign `{a[7:6], a[1:0]}` to `y`.

Return exactly one source artifact named `packed_logic_bus_slice.vams`.
