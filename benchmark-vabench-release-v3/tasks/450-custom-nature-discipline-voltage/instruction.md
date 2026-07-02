# Custom Nature Discipline Voltage

Implement one behavioral Verilog-A/AMS source file named `custom_nature_discipline_voltage.vams`.

## Interface

Use the exact Verilog-AMS interface shown in the starter file. This is a language-declaration candidate, not part of the built-in `electrical` behavioral-event certification layer.

## Required Feature

Declare a custom nature and discipline for behavioral voltage modeling.

## Required Behavior

Required behavior:

- declare a custom `nature` with units, access function, and absolute tolerance;
- declare a custom `discipline` using that nature as its potential;
- declare module ports using the custom discipline;
- drive the output potential from the input potential using a behavioral voltage contribution;
- do not use current contributions.

Return exactly one source artifact named `custom_nature_discipline_voltage.vams`.
