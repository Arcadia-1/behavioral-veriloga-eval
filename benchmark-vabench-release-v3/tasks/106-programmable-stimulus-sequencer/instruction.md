# Programmable Stimulus Sequencer

Implement `programmable_stimulus_sequencer.va` in Verilog-A.

## Interface

```verilog
module programmable_stimulus_sequencer(clk, rst, mode, gate, out, metric);
```

## Required Behavior

This task asks for the `programmable_stimulus_sequencer` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l2_programmable_stimulus_sequencer` transient scenario and checks the saved waveform/metric behavior with EVAS.

Original public behavior context:

### Programmable stimulus sequencer (tb-generation)

Write a Spectre transient testbench for the described behavioral Verilog-A module.

Behavioral intent:

Generate a programmable ramp, swept/chirp sine, and gated burst/PRBS stimulus schedule.

Module name: `programmable_stimulus_sequencer`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

Public port contract:

```verilog
module programmable_stimulus_sequencer(clk, rst, mode, gate, out, metric);
input clk, rst, mode, gate;
output out, metric;
electrical clk, rst, mode, gate, out, metric;
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. mode selects ramp, sine, or burst/PRBS behavior. gate enables the burst segment. out is the generated stimulus waveform. metric is a voltage-coded segment-status observable.

Saved waveform columns:

```text
clk rst mode gate out metric
```

Public transient contract:

```spectre
tran tran stop=90n maxstep=0.25n
```

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
