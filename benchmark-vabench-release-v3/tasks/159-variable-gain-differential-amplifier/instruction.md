# Variable Gain Differential Amplifier

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband / analog primitive variable-gain blocks
- Base function: Differential variable-gain amplifier with output limiting
- Domain: `voltage`
- Target artifact(s): `variable_gain_differential_amplifier.va`
- Visible context: public task, module interface, control/input roles, and limiting contract.
- Evaluator boundary: validation logic is external; do not generate checker, testbench, or measurement helper artifacts.

## Public Verilog-A Interface

`variable_gain_differential_amplifier.va` must declare:

```verilog
module variable_gain_differential_amplifier(sigin_p, sigin_n, sigctrl_p, sigctrl_n, sigout);
input sigin_p, sigin_n, sigctrl_p, sigctrl_n;
output sigout;
electrical sigin_p, sigin_n, sigctrl_p, sigctrl_n, sigout;
```

## Behavioral Contract

Model a differential variable-gain voltage amplifier. The differential control voltage `V(sigctrl_p, sigctrl_n)` scales the differential input voltage `V(sigin_p, sigin_n)`. Use a gain constant of 2.0, center the output around 0.2 V, and clamp the final output target to the range -0.4 V through 0.8 V.

Compute the limited target as a real variable and drive `sigout` with a single voltage contribution. Do not use current contributions, transistor devices, filtering, or testbench-specific constants.

## Output Contract

Return exactly one source artifact named `variable_gain_differential_amplifier.va`.
Do not include explanatory prose outside the source artifact contents.
