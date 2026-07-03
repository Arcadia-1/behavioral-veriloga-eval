# Differential Amplifier Core

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband / analog primitive gain blocks
- Base function: Differential-input single-ended gain core
- Domain: `voltage`
- Target artifact(s): `differential_amplifier_core.va`
- Visible context: public task, module interface, fixed gain/offset contract.
- Evaluator boundary: validation logic is external; do not generate checker, testbench, or measurement helper artifacts.

## Public Verilog-A Interface

`differential_amplifier_core.va` must declare:

```verilog
module differential_amplifier_core(sigin_p, sigin_n, sigout);
input sigin_p, sigin_n;
output sigout;
electrical sigin_p, sigin_n, sigout;
```

## Behavioral Contract

Model a single-ended output gain core driven by the differential input voltage. Subtract a 0.05 V input-referred offset from `V(sigin_p, sigin_n)`, then apply a fixed voltage gain of 2.0 and drive `sigout`.

Use a direct voltage-domain contribution. Do not add rail clipping, filtering, current contributions, transistor devices, or testbench-specific constants.

## Output Contract

Return exactly one source artifact named `differential_amplifier_core.va`.
Do not include explanatory prose outside the source artifact contents.
