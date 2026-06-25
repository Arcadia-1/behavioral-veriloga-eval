# Gain Estimator

Implement `gain_estimator.va` in Verilog-A.

## Interface

```verilog
module gain_estimator(VDD, VSS, vinp, vinn, voutp, voutn, gain_out, valid);
```

## Required Behavior

This task asks for the `gain_estimator` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l1_gain_estimator` transient scenario and checks the saved waveform/metric behavior with EVAS.

Original public behavior context:

Write a Spectre transient testbench for the supplied `gain_estimator` behavioral measurement helper.

Public requirements:

- Instantiate `gain_estimator` with ports `(VDD VSS vinp vinn voutp voutn gain_out valid)`.
- Drive `VDD=0.9 V` and `VSS=0 V`.
- Provide a differential input with about 60 mV peak-to-peak span.
- Provide a differential output with about 360 mV peak-to-peak span, corresponding to gain near 6.
- Run long enough for `valid` to assert and for `gain_out` to settle.
- Save exactly `vinp`, `vinn`, `voutp`, `voutn`, `gain_out`, and `valid`.
- Use voltage-domain behavioral sources only; avoid transistor-level devices, AC/noise analysis, and current-domain solver assumptions.

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
