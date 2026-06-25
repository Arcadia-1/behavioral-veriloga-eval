# IQ Downconversion Chain

Implement `iq_downconversion_chain.va` in Verilog-A.

## Interface

```verilog
module iq_downconversion_chain(clk, rst, vin, out, metric, lo_i, lo_q, mix_i, mix_q, phase_mon);
```

## Required Behavior

This task asks for the `iq_downconversion_chain` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l2_iq_downconversion_chain` transient scenario and checks the saved waveform/metric behavior with EVAS.

Original public behavior context:

### I/Q downconversion chain (tb-generation)

Write a Spectre transient testbench for the described behavioral Verilog-A module.

Behavioral intent:

Compose quadrature LO sequencing, two mixer paths, and baseband I/Q observables in a voltage-domain receiver chain.

Module name: `iq_downconversion_chain`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

This is a voltage-domain RF/AFE behavioral macromodel task. Model observable gain, compression, LO polarity, RSSI, limiting, AGC, or I/Q baseband behavior with event-driven voltage states. Do not implement transistor RF physics, S-parameters, current-domain loads, communication modem algorithms, or full link-level decoding.

Public port contract:

```verilog
module iq_downconversion_chain(clk, rst, vin, out, metric, lo_i, lo_q, mix_i, mix_q, phase_mon);
input clk, rst, vin;
output out, metric, lo_i, lo_q, mix_i, mix_q, phase_mon;
electrical clk, rst, vin, out, metric, lo_i, lo_q, mix_i, mix_q, phase_mon;
```

Signal contract:

clk is the quadrature LO phase-advance clock and rst is voltage-coded reset. vin is the RF input envelope around 0.45 V common mode. phase_mon exposes the four-phase LO state, lo_i and lo_q expose voltage-coded I/Q LO polarity, mix_i and mix_q expose bounded mixer outputs, out is the I-path baseband observable, and metric is the Q-path baseband observable.

Saved waveform columns:

```text
clk rst vin out metric lo_i lo_q mix_i mix_q phase_mon
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
