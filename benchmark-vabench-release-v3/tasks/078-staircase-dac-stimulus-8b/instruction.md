# Staircase DAC Stimulus 8b

Implement `staircase_dac_stimulus_8b.va` in Verilog-A.

## Interface

```verilog
module staircase_dac_stimulus_8b(clk, rst, vout, code0, code1, code2, code3, code4, code5, code6, code7);
```

Inputs: `clk, rst`.
Outputs: `vout, code0, code1, code2, code3, code4, code5, code6, code7`.

## Required Behavior

On each rising `clk`, reset the code to zero while `rst` is high; otherwise increment an 8-bit code modulo 256. Drive `code[7:0]` and analog `vout = 0.9 * code / 255`.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
