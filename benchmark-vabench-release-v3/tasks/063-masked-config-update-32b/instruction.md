# Masked Config Update 32b

Implement one Verilog-A DUT file named `masked_config_update_32b.va`.

## Interface

Define module `masked_config_update_32b` with vector electrical ports in this exact order:

```verilog
module masked_config_update_32b(
    input electrical [31:0] old_cfg,
    input electrical [31:0] new_cfg,
    input electrical [31:0] mask,
    output electrical [31:0] out_cfg
);
```

Use `vdd=0.9`, `vth=0.45`, and `tr=20p` unless compatible parameters are needed.

## Required Behavior

Treat all input bits as 0/0.9 V logic using `vth`. For each bit `N`, drive `out_cfg[N] = new_cfg[N]` when `mask[N]` is high, otherwise drive `out_cfg[N] = old_cfg[N]`.

Drive high outputs near `vdd` and low outputs near 0 V using smooth Verilog-A contributions. Compact loop-based Verilog-A is preferred; do not manually expand 32 scalar input/output ports.

## Output

Return exactly `masked_config_update_32b.va`. Do not generate a Spectre testbench.
