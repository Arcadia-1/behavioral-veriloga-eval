# Limiting Differential Amplifier

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband / analog primitive gain blocks
- Base function: Differential amplifier with output limiting
- Domain: `voltage`
- Target artifact(s): `limiting_differential_amplifier.va`
- Visible context: public task, module interface, parameters, and limiting contract.
- Evaluator boundary: validation logic is external; do not generate checker, testbench, or measurement helper artifacts.

## Public Verilog-A Interface

`limiting_differential_amplifier.va` must declare:

```verilog
module limiting_differential_amplifier(sigin_p, sigin_n, sigout);
input sigin_p, sigin_n;
output sigout;
electrical sigin_p, sigin_n, sigout;
parameter real gain = 1;
parameter real sigout_high = 10;
parameter real sigout_low = -10;
parameter real sigin_offset = 0;
```

## Behavioral Contract

Read the differential input `V(sigin_p, sigin_n)`, subtract `sigin_offset`, and apply the voltage gain `gain`. Center the amplified output at the midpoint between `sigout_high` and `sigout_low`, then clamp the target to those two output rails.

Compute the limited target as a real variable and drive `sigout` with a single voltage contribution. Do not use current contributions, transistor devices, smoothing filters, or testbench-specific constants.

## Output Contract

Return exactly one source artifact named `limiting_differential_amplifier.va`.
Do not include explanatory prose outside the source artifact contents.
