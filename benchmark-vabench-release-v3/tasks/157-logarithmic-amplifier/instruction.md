# Logarithmic Amplifier

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband / analog primitive nonlinear amplifiers
- Base function: Offset-corrected logarithmic voltage amplifier
- Domain: `voltage`
- Target artifact(s): `logarithmic_amplifier.va`
- Visible context: public task, module interface, and nonlinear transfer contract.
- Evaluator boundary: validation logic is external; do not generate checker, testbench, or measurement helper artifacts.

## Public Verilog-A Interface

`logarithmic_amplifier.va` must declare:

```verilog
module logarithmic_amplifier(sigin, sigout);
input sigin;
output sigout;
electrical sigin, sigout;
```

## Behavioral Contract

Subtract a 0.2 V input offset, take the absolute value of the adjusted signal, floor the magnitude at 0.1 V to keep the logarithm well-defined, and drive `sigout` with the natural logarithm of that guarded magnitude.

Use Verilog-A real arithmetic and math operators. Do not use current contributions, transistor devices, smoothing filters, or testbench-specific constants.

## Output Contract

Return exactly one source artifact named `logarithmic_amplifier.va`.
Do not include explanatory prose outside the source artifact contents.
