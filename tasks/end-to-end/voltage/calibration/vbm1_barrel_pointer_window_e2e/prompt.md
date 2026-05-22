# Task: vbm1_barrel_pointer_window_e2e

Write both the Verilog-A DUT and Spectre testbench for a 4-state barrel pointer
window generator.

The DUT module must be named `barrel_pointer_window` and use ports `clk`,
`rst_n`, `win0`, `win1`, `win2`, and `win3`. All ports are electrical. `rst_n`
is active low. Reset returns the pointer to state 0. Each rising `clk` edge
while reset is released advances the state modulo 4. Exactly two adjacent
window outputs are high in each state: `win0/win1`, then `win1/win2`, then
`win2/win3`, then `win3/win0`.

The testbench must stimulate reset and at least six post-reset clocked states,
save `clk`, `rst_n`, and all `win*` outputs, and run a transient analysis with
sufficient time resolution for event checking.

Return exactly two files: `barrel_pointer_window.va` and `tb_barrel_pointer_window_ref.scs`.
