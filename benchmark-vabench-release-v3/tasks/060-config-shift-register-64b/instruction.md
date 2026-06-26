# Config Shift Register 64b

Implement one Verilog-A DUT file named `config_shift_reg_64b.va`.

## Interface

Define module `config_shift_reg_64b` with vector electrical output in this exact order:

```verilog
module config_shift_reg_64b(
    input electrical clk,
    input electrical rst_n,
    input electrical serial_in,
    output electrical [63:0] q
);
```

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed.

## Required Behavior

Treat `clk`, `rst_n`, and `serial_in` as 0/0.9 V logic using `vth`. On each rising crossing of `clk`, if `rst_n` is high, shift `serial_in` into `q[0]`, previous `q[0]` into `q[1]`, and so on through `q[63]`. If `rst_n` is low on a rising clock edge, clear all register bits.

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions. Compact loop-based Verilog-A is preferred; do not manually expand 64 scalar output ports.

## Output

Return exactly `config_shift_reg_64b.va`. Do not generate a Spectre testbench.
