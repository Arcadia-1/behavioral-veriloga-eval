# Safe Voltage Divider

## Task Contract

Implement a guarded voltage-domain divider with scalar gain.

- Form: `dut`
- Level: `L1`
- Category: mixed-signal analog arithmetic primitive
- Target artifact: `safe_voltage_divider.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`safe_voltage_divider.va` must declare:

```verilog
module safe_voltage_divider(signumer, sigdenom, sigout);
input signumer, sigdenom;
output sigout;
electrical signumer, sigdenom, sigout;
```

## Public Parameter Contract

- `gain = 1`: scalar multiplier applied to the quotient.
- `min_sigdenom = 1.0e-9 from (0:inf)`: minimum denominator magnitude in
  volts. Testbenches may override it.

## Required Behavior

Compute an effective denominator from `V(sigdenom)`. If its magnitude is at
least `min_sigdenom`, use it directly. If its magnitude is smaller, clamp it to
`+min_sigdenom` for a positive denominator and to `-min_sigdenom` for a zero or
negative denominator.

Drive `sigout` with `gain * V(signumer) / effective_denominator`.

## Modeling Constraints

Use deterministic voltage-domain arithmetic. Do not let the denominator become
zero, remove the sign-sensitive clamp, add filtering, or hard-code testbench
stimulus values.

## Output Contract

Return exactly one source artifact named `safe_voltage_divider.va`.
