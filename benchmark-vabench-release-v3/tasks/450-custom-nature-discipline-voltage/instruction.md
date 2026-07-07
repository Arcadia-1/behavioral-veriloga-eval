# Custom Nature Discipline Voltage

## Task Contract

Implement one Verilog-AMS source file named `custom_nature_discipline_voltage.vams`. This task exercises a custom nature and discipline used for a voltage-domain pass-through model.

This is a Verilog-AMS semantic/support task. Preserve the custom nature and custom discipline declarations instead of replacing the model with the built-in `electrical` discipline.

## Public Verilog-A Interface

Declare a custom nature named `V3Voltage` and a custom discipline named `v3electrical`. Use this exact module interface:

```verilog
module custom_nature_discipline_voltage(a, y);
```

Port `a` is the input and port `y` is the output. Both ports must use the custom `v3electrical` discipline.

## Public Parameter Contract

This task has no public Verilog-A parameters.

## Required Behavior

`V3Voltage` must use voltage units, the access function `V`, and an absolute tolerance. `v3electrical` must use `V3Voltage` as its potential nature. The module must drive the output potential `V(y)` from the input potential `V(a)`.

## Modeling Constraints

Use a behavioral voltage contribution for the pass-through behavior. Do not use current contributions or built-in `electrical` port declarations for the target module.

## Output Contract

Return exactly one source artifact named `custom_nature_discipline_voltage.vams`.
