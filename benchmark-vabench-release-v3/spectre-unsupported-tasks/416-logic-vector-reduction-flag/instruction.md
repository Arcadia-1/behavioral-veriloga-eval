# Logic Vector Reduction Flag

Implement one behavioral Verilog-A source file named `logic_vector_reduction_flag.vams`.

## Interface

Use this exact module interface:

```verilog
module logic_vector_reduction_flag(input [3:0] code, output valid);
```

Keep the model behavioral/digital and do not introduce current contributions.

## Required Behavior

Use logic vector reduction in a continuous assignment.

Required behavior:

- declare `logic [3:0] code`;
- declare scalar `logic valid`;
- continuously assign `valid = |code`;
- `valid` must be low only when all four bits of `code` are low;
- `valid` must be high when any one or more bits of `code` are high.

Return exactly one source artifact named `logic_vector_reduction_flag.vams`.
