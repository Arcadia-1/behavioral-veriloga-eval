# Config Shift Register 64b

Implement one Verilog-A DUT file named `config_shift_reg_64b.va`.

## Interface

Define module `config_shift_reg_64b` with scalar electrical ports in this exact order:

```text
clk, rst_n, sin, q63, q62, q61, q60, q59, q58, q57, q56, q55, q54, q53, q52, q51, q50, q49, q48, q47, q46, q45, q44, q43, q42, q41, q40, q39, q38, q37, q36, q35, q34, q33, q32, q31, q30, q29, q28, q27, q26, q25, q24, q23, q22, q21, q20, q19, q18, q17, q16, q15, q14, q13, q12, q11, q10, q9, q8, q7, q6, q5, q4, q3, q2, q1, q0
```

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed. Treat logic inputs as 0/0.9 V using `vth`.

## Required Behavior

On each rising crossing of `clk`, if `rst_n` is high, shift `sin` into `q0`, previous `q0` into `q1`, and so on through `q63`. If `rst_n` is low on a rising clock edge, clear all register bits.

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions.

## Output

Return exactly `config_shift_reg_64b.va`. Do not generate a Spectre testbench.
