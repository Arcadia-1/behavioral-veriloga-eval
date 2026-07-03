# Differential Gain Driver

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband / analog primitive differential drivers
- Base function: Differential input to balanced differential output driver
- Domain: `voltage`
- Target artifact(s): `differential_gain_driver.va`
- Visible context: public task, module interface, gain parameter, and behavioral contract.
- Evaluator boundary: validation logic is external; do not generate checker, testbench, or measurement helper artifacts.

## Public Verilog-A Interface

`differential_gain_driver.va` must declare:

```verilog
module differential_gain_driver(sigin_p, sigin_n, sigout_p, sigout_n, sigref);
input sigin_p, sigin_n, sigref;
output sigout_p, sigout_n;
electrical sigin_p, sigin_n, sigout_p, sigout_n, sigref;
parameter real gain = 1;
```

## Behavioral Contract

Read the differential input `V(sigin_p, sigin_n)` and generate a balanced differential output pair around the reference node `sigref`. The output differential voltage must equal the input differential voltage multiplied by `gain`; each output side contributes half of that differential swing with opposite polarity around `sigref`.

Use voltage-domain contributions only. Do not introduce single-ended common-mode shifts beyond the supplied `sigref`, current contributions, transistor devices, filtering, or testbench-specific constants.

## Output Contract

Return exactly one source artifact named `differential_gain_driver.va`.
Do not include explanatory prose outside the source artifact contents.
