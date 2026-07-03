# Mfactor System Function Gain

## Task Contract

Implement one Verilog-A source file named `mfactor_system_function_gain.va`. The task models a voltage-domain gain controlled by the Spectre instance multiplicity factor.

## Form-Specific Requirements

This is a DUT task. The supplied testbenches set instance multiplicity with Spectre `m=...`.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module mfactor_system_function_gain(
    input electrical in,
    output electrical out
);
```

## Public Parameter Contract

This task has no public Verilog-A parameters. The effective multiplicity is read from Spectre using `$mfactor`.

## Required Behavior

Read the effective instance multiplicity with Cadence-compatible `$mfactor` syntax and drive `out` with that value times `V(in)`. The supplied tests instantiate the DUT with `m=2.0`.

## Modeling Constraints

Use `transition(..., 0, 200p, 200p)` for the output. Use only voltage-domain behavior and do not hard-code the gain waveform.

## Output Contract

Return exactly one source artifact named `mfactor_system_function_gain.va`.
