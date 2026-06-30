# Dither Adder

Implement `dither_adder.va` in Verilog-A.

## Interface

```verilog
module dither_adder(
    input  electrical VRES_P,
    input  electrical VRES_N,
    input  electrical DPN,
    output electrical VOUT_P,
    output electrical VOUT_N
);
```

## Required Behavior

This task asks for the `dither_adder` behavioral module, not a Spectre testbench. The hidden evaluator instantiates this module in the original `vbr1_l2_gain_extraction_convergence_measurement_flow` transient scenario and checks the saved waveform/metric behavior with EVAS.

Gold-source design notes carried into the public contract:

```text
// Differential dither adder — benchmark gold style.
// Keeps a direct contribution instead of the original transition(V(VRES_P)+...)
// form. This is no longer required for EVAS acceptance; the gold keeps the
// lower-warning, simpler output style for benchmark stability.
//
//   dither_diff = +DITHER_AMP  when DPN > vth
//   dither_diff = -DITHER_AMP  when DPN < vth
//   VOUT_P = VRES_P + dither_diff / 2
//   VOUT_N = VRES_N - dither_diff / 2
```

Original public behavior context:

# Dithered differential gain extraction flow Testbench Companion

Write a Spectre transient testbench for the `Dithered differential gain extraction flow` behavioral
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
