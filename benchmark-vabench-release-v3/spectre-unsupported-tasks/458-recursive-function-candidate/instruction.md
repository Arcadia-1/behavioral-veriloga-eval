# Recursive Function Candidate

## Task Contract

Implement one behavioral Verilog-A/AMS source file named `recursive_function_candidate.va`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module recursive_function_candidate(output electrical out);
```

## Public Parameter Contract

Preserve these public parameter declarations and default values:

```verilog
parameter integer depth = 3 from [1:5];
```

## Required Behavior

Use a recursive user-defined function candidate.

Required behavior:

- declare an integer parameter `depth` with default value 3 and a legal range of 1 through 5;
- define a user function `fact` that accepts an integer input;
- return 1.0 when the input is less than or equal to 1;
- otherwise call `fact(n - 1)` recursively;
- drive `out` with `fact(depth)`.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Do not add current-domain contributions unless the public interface explicitly requires them.

This row remains archived because it uses recursive function semantics rejected by standalone Spectre in this environment. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `recursive_function_candidate.va`.
