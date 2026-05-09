Create only the DUT Verilog-A model for `barrel_pointer_window`. Do not generate a testbench.

Required module: `barrel_pointer_window`. Ports, all `electrical`, exactly as named and ordered: `clk, rst_n, win0, win1, win2, win3`.
Behavior: rotate a two-element adjacent selection window. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=130n maxstep=500p` and saves waveform columns `clk rst_n win0 win1 win2 win3`.

Return exactly one complete Verilog-A code block for `barrel_pointer_window.va`.
