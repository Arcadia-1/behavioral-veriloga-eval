# Recursive Function Candidate

Implement one behavioral Verilog-A/AMS source file named `recursive_function_candidate.va`.

## Interface

Use this exact module interface:

```verilog
module recursive_function_candidate(
    output electrical out
);
```

Keep the model behavioral and do not introduce current contributions.

## Required Behavior

Use a recursive user-defined function candidate.

Required behavior:

- define a user function `fact` that accepts an integer input;
- return 1.0 when the input is less than or equal to 1;
- otherwise call `fact(n - 1)` recursively;
- drive `out` with `fact(3)`, which should evaluate to 6.0.

Return exactly one source artifact named `recursive_function_candidate.va`.
