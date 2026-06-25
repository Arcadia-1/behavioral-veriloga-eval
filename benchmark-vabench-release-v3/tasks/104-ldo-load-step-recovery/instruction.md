# LDO Load Step Recovery

Implement `ldo_load_step_recovery_flow.va` in Verilog-A.

## Interface

```verilog
module ldo_load_step_recovery_flow(clk, rst, vin, out, metric, load_mon, ctrl_mon);
```

## Required Behavior

This task asks for the `ldo_load_step_recovery_flow` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l2_ldo_load_step_recovery_flow` transient scenario and checks the saved waveform/metric behavior with EVAS.

Original public behavior context:

### LDO load-step recovery flow (tb-generation)

Write a Spectre transient testbench for the described behavioral Verilog-A module.

Behavioral intent:

Compose a regulator macro model with repeated load-step disturbances and recovery-status observation.

Module name: `ldo_load_step_recovery_flow`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

This is a voltage-domain macro-model task for bias/reference/power management behavior. Model observable startup, threshold, trim, hysteresis, droop, or recovery behavior with event-driven voltage state updates. Do not use branch currents, transistor devices, process-device equations, or true current-mode regulation loops.

Public port contract:

```verilog
module ldo_load_step_recovery_flow(clk, rst, vin, out, metric, load_mon, ctrl_mon);
input clk, rst, vin;
output out, metric, load_mon, ctrl_mon;
electrical clk, rst, vin, out, metric, load_mon, ctrl_mon;
```

Signal contract:

clk and rst are voltage-coded logic signals. vin is the public load-step stimulus. load_mon tracks the bounded load request seen by the regulator macro, ctrl_mon is an abstract voltage-domain pass/recovery control monitor, out is the regulator output after transient droop and recovery, and metric marks recovered regulation after each load transition. This remains a behavioral load-step recovery macro, not a transistor/pass-device LDO implementation.

Saved waveform columns:

```text
clk rst vin out metric load_mon ctrl_mon
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
