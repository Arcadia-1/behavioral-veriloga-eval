# Sample Hold Droop Front End

Implement `sample_hold_droop_ref.va` in Verilog-A.

## Interface

```verilog
module sample_hold_droop_ref(vdd, vss, clk, vin, vout, valid, coarse);
```

## Required Behavior

This task asks for the `sample_hold_droop_ref` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l2_converter_front_end` transient scenario and checks the saved waveform/metric behavior with EVAS.

Original public behavior context:

# Converter front-end chain Testbench Companion

Write a Spectre transient testbench for the `Converter front-end` behavioral
Verilog-A release task. This is the testbench-generation companion for an
already materialized end-to-end task.

The testbench should instantiate the same behavioral DUT or system module used
by the corresponding end-to-end form, drive an aperture-sensitive sampling
scenario, save the observable waveform or metric signals, and preserve the
EVAS/Spectre validation contract.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- save `vin`, `clk`, `vout`, `valid`, and `coarse`
- include or instantiate the Verilog-A behavioral module under test
- exercise aperture-delayed sampling, bounded hold droop, coarse decision, and
  valid-pulse behavior
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions

Use voltage-coded logic with a 0.45 V threshold where applicable, drive high logic outputs near 0.9 V and low outputs near 0 V, and keep the model pure behavioral Verilog-A. Do not use transistor-level devices, AC/noise analysis, hidden checker logic, or simulator-private side channels.

Only the target artifact is graded as the candidate implementation; companion Verilog-A files listed by the testbench are supplied by the harness for this task.
