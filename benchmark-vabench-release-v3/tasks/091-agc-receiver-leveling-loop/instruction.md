# AGC Receiver Leveling Loop

Implement `agc_receiver_leveling_loop.va` in Verilog-A.

## Interface

```verilog
module agc_receiver_leveling_loop(clk, rst, vin, out, metric, gain_mon, rssi_mon);
```

## Required Behavior

This task asks for the `agc_receiver_leveling_loop` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l2_agc_receiver_leveling_loop` transient scenario and checks the saved waveform/metric behavior with EVAS.

Original public behavior context:

### AGC receiver leveling loop (tb-generation)

Write a Spectre transient testbench for the described behavioral Verilog-A module.

Behavioral intent:

Compose a receiver gain path, envelope/RSSI observation, and gain-control update so output amplitude settles toward a target level.

Module name: `agc_receiver_leveling_loop`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

This is a voltage-domain RF/AFE behavioral macromodel task. Model observable gain, compression, LO polarity, RSSI, limiting, AGC, or I/Q baseband behavior with event-driven voltage states. Do not implement transistor RF physics, S-parameters, current-domain loads, communication modem algorithms, or full link-level decoding.

Public port contract:

```verilog
module agc_receiver_leveling_loop(clk, rst, vin, out, metric, gain_mon, rssi_mon);
input clk, rst, vin;
output out, metric, gain_mon, rssi_mon;
electrical clk, rst, vin, out, metric, gain_mon, rssi_mon;
```

Signal contract:

clk and rst are voltage-coded logic signals. vin is the receiver input envelope around 0.45 V common mode. rssi_mon is the public envelope/RSSI monitor, gain_mon is the bounded public gain-control monitor, the internal gain-control loop reduces gain under overload and restores a target output amplitude, out is the leveled receiver output, and metric is high near target amplitude.

Saved waveform columns:

```text
clk rst vin out metric gain_mon rssi_mon
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
