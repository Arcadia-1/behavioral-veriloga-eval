# Comparator Offset Search

Implement `comparator_offset_search_ref.va` in Verilog-A.

## Interface

```verilog
module comparator_offset_search_ref(vdd, vss, inp, inn, outp, trip_v, offset_est, valid);
```

## Required Behavior

This task asks for the `comparator_offset_search_ref` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l2_comparator_measurement_flow` transient scenario and checks the saved waveform/metric behavior with EVAS.

Original public behavior context:

# Single-ramp comparator offset measurement flow Testbench Companion

Write a Spectre transient testbench for the `Single-ramp comparator offset measurement flow` behavioral
Verilog-A release task. This is the testbench-generation companion for an
already materialized end-to-end task.

The testbench should instantiate the same behavioral DUT or system module used
by the corresponding end-to-end form, drive the public transient scenario, save
the observable waveform or metric signals, and preserve the EVAS/Spectre
validation contract.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- instantiate `comparator_offset_search_ref` with ports `vdd vss inp inn outp trip_v offset_est valid`
- drive `inn` at 0.500 V and perform a single ramp of `inp` from 0.490 V to 0.520 V over the transient
- save exactly the public scalar observables needed by the checker: `inp`, `inn`, `outp`, `trip_v`, `offset_est`, and `valid`
- include the Verilog-A behavioral module under test
- exercise the crossing so `outp`, `valid`, `trip_v`, and `offset_est` all settle after the expected 5 mV offset trip point
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
