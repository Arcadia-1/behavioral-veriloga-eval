# Complete Calibration Loop

Implement `complete_calibration_loop.va` in Verilog-A.

## Interface

```verilog
module complete_calibration_loop(clk, rst, vin, out, metric, trim_mon, residual_mon);
```

## Required Behavior

This task asks for the `complete_calibration_loop` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l2_complete_calibration_loop` transient scenario and checks the saved waveform/metric behavior with EVAS.

Original public behavior context:

### Complete calibration loop (tb-generation)

Write a Spectre transient testbench for the described behavioral Verilog-A module.

Behavioral intent:

Close a simple calibration loop from error stimulus through controller and actuator output.

Module name: `complete_calibration_loop`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

Public port contract:

```verilog
module complete_calibration_loop(clk, rst, vin, out, metric, trim_mon, residual_mon);
input clk, rst, vin;
output out, metric, trim_mon, residual_mon;
electrical clk, rst, vin, out, metric, trim_mon, residual_mon;
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is the external offset/error stimulus around 0.45 V. The internal controller drives correction opposite the measured residual error, trim_mon is the public bounded trim/control voltage, residual_mon is the post-correction residual monitor around 0.45 V, out is the bounded corrected plant response, and metric is high when out is close to 0.45 V.

Saved waveform columns:

```text
clk rst vin out metric trim_mon residual_mon
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
