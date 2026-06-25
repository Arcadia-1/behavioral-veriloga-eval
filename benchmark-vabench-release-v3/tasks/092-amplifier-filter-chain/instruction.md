# Amplifier Filter Chain

Implement `amplifier_filter_chain.va` in Verilog-A.

## Interface

```verilog
module amplifier_filter_chain(clk, rst, vin, out, metric, preamp_mon, filt1_mon, filt2_mon, settle_metric);
```

## Required Behavior

This task asks for the `amplifier_filter_chain` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l2_amplifier_filter_chain` transient scenario and checks the saved waveform/metric behavior with EVAS.

Original public behavior context:

### Amplifier/filter chain (tb-generation)

Write a Spectre transient testbench for the described behavioral Verilog-A module.

Behavioral intent:

Combine a gain block and low-pass filter; expose the bounded pre-filter amplified target on metric so out can be checked for lagged settling.

Module name: `amplifier_filter_chain`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

Public port contract:

```verilog
module amplifier_filter_chain(clk, rst, vin, out, metric, preamp_mon, filt1_mon, filt2_mon, settle_metric);
input clk, rst, vin;
output out, metric, preamp_mon, filt1_mon, filt2_mon, settle_metric;
electrical clk, rst, vin, out, metric, preamp_mon, filt1_mon, filt2_mon, settle_metric;
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is an analog voltage stimulus. metric and preamp_mon expose the bounded pre-filter amplified target. filt1_mon and filt2_mon expose the two internal low-pass states. out is the bounded filtered voltage derived from the second pole. settle_metric is a voltage-coded settled-status observable.

Saved waveform columns:

```text
clk rst vin out metric preamp_mon filt1_mon filt2_mon settle_metric
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
