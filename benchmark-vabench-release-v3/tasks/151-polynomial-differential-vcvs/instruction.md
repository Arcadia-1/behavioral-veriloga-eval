# Polynomial Differential VCVS

## Task Contract

Implement a nonlinear differential voltage-controlled voltage source with
common-mode centered differential outputs.

- Form: `dut`
- Level: `L1`
- Category: mixed-signal nonlinear analog primitive
- Target artifact: `polynomial_differential_vcvs.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`polynomial_differential_vcvs.va` must declare:

```verilog
module polynomial_differential_vcvs(inp, inn, outp, outn);
input inp, inn;
output outp, outn;
electrical inp, inn, outp, outn;
```

## Public Parameter Contract

- `vcmo = 1.1`: output common-mode voltage.
- `a1 = 1`, `a2 = 0`, `a3 = 0`, `a5 = 0`, `a7 = 0`: polynomial
  coefficients for powers of the differential input voltage.
- `vsat = 10000000`: magnitude limit for the half-differential output target.

## Required Behavior

Let `vid = V(inp, inn)`. Compute the half-differential target as:

`(a1*vid + a2*vid^2 + a3*vid^3 + a5*vid^5 + a7*vid^7) / 2`

Limit that target to the interval `[-vsat, +vsat]`. Drive `outp` to
`vcmo + limited_target` and `outn` to `vcmo - limited_target`.

## Modeling Constraints

Use direct voltage contributions and real-valued arithmetic. Preserve the
output common-mode. Do not add dynamic state, current contributions, rail models,
or testbench-specific constants.

## Output Contract

Return exactly one source artifact named `polynomial_differential_vcvs.va`.
