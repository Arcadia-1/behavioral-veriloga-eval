# Offset Gain Amplifier

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband / analog primitive gain blocks
- Base function: Single-ended offset-correcting gain stage
- Domain: `voltage`
- Target artifact(s): `offset_gain_amplifier.va`
- Visible context: public task, module interface, fixed gain/offset contract.
- Evaluator boundary: validation logic is external; do not generate checker, testbench, or measurement helper artifacts.

## Public Verilog-A Interface

`offset_gain_amplifier.va` must declare:

```verilog
module offset_gain_amplifier(sigin, sigout);
input sigin;
output sigout;
electrical sigin, sigout;
```

## Behavioral Contract

Model a single-ended voltage gain stage that subtracts a 0.2 V input offset before applying a fixed voltage gain of 3.0. Drive `sigout` with the amplified offset-corrected signal.

Use a direct voltage-domain contribution. Do not add rail clipping, filtering, current contributions, transistor devices, or testbench-specific constants.

## Output Contract

Return exactly one source artifact named `offset_gain_amplifier.va`.
Do not include explanatory prose outside the source artifact contents.
