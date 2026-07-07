# Branch Declaration Voltage Probe

## Task Contract

Implement one Verilog-A source file named `branch_declaration_voltage_probe.va`. This row is a Verilog-A branch-declaration semantic/support task: it verifies that a named branch voltage can be observed through a public output.

This is a DUT task in the language-semantic support layer. The public testbenches drive voltages on `p` and `n`; the DUT must expose the branch voltage, not synthesize an unrelated waveform.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module branch_declaration_voltage_probe(
    input electrical p,
    input electrical n,
    output electrical out
);
```

## Public Parameter Contract

This module has no public module parameters. Use a fixed `transition(..., 0, 200p, 200p)` smoothing contract for the observable output.

## Required Behavior

Declare an explicit branch named `br` between `p` and `n`. Drive `out` with the named branch voltage `V(br)`, equivalent to `V(p,n)`, after the fixed transition smoothing. The output must track both positive and negative branch voltages without thresholding or clipping.

## Modeling Constraints

Use the explicit `branch (p, n) br;` declaration and read the branch with `V(br)`. Use only voltage-domain output contribution for `out`; do not use `I(...)` in this row.

## Output Contract

Return exactly one source artifact named `branch_declaration_voltage_probe.va`.
