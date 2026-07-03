# Vargain Diffamp Clip

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband / analog primitive variable-gain blocks
- Base function: Parameterized voltage-controlled differential gain block with clipping
- Domain: `voltage`
- Target artifact(s): `vargain_diffamp_clip.va`
- Visible context: public task, module interface, parameters, control/input roles, and clipping contract.
- Evaluator boundary: validation logic is external; do not generate checker, testbench, or measurement helper artifacts.

## Public Verilog-A Interface

`vargain_diffamp_clip.va` must declare:

```verilog
module vargain_diffamp_clip(sigin_p, sigin_n, sigctrl_p, sigctrl_n, sigout);
input sigin_p, sigin_n, sigctrl_p, sigctrl_n;
output sigout;
electrical sigin_p, sigin_n, sigctrl_p, sigctrl_n, sigout;
parameter real gain_const = 3.0;
parameter real sigout_high = 1.0;
parameter real sigout_low = -1.0;
parameter real sigin_offset = 0.05;
```

## Behavioral Contract

Model a parameterized voltage-controlled differential gain block. The differential control voltage `V(sigctrl_p, sigctrl_n)` scales the differential input after subtracting `sigin_offset`. Multiply by `gain_const`, then clamp the output target to `sigout_low` and `sigout_high`.

Compute the clipped target as a real variable and drive `sigout` with a single voltage contribution. Do not use current contributions, transistor devices, filtering, or testbench-specific constants.

## Output Contract

Return exactly one source artifact named `vargain_diffamp_clip.va`.
Do not include explanatory prose outside the source artifact contents.
