# Edge Crossing Interval Timer

Implement `cross_interval_163p333_ref.va` in Verilog-A.

## Interface

```verilog
module cross_interval_163p333_ref (
    inout  electrical VDD,
    inout  electrical VSS,
    input  electrical a,
    input  electrical b,
    output electrical delay_out,
    output electrical seen_out
);
```

## Required Behavior

This task asks for the `cross_interval_163p333_ref` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l1_edge_interval_timer` transient scenario and checks the saved waveform/metric behavior with EVAS.

Original public behavior context:

# Edge interval timer Testbench Companion

Write a Spectre transient testbench for the `Edge interval timer` behavioral
Verilog-A release task. This is the testbench-generation companion for an
already materialized end-to-end task.

The testbench should instantiate the same behavioral DUT or system module used
by the corresponding end-to-end form, drive the public transient scenario, save
the observable waveform or metric signals, and preserve the EVAS/Spectre
validation contract.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- save the public observables needed by the public behavior checks
- include or instantiate the Verilog-A behavioral module under test
- satisfy the named behavior checks using only public waveforms and side outputs
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
