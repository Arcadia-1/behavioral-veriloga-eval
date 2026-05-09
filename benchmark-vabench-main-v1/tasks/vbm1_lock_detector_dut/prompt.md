Create only the DUT Verilog-A model for `lock_detector`. Do not generate a testbench.

Required module: `lock_detector`. Ports, all `electrical`, exactly as named and ordered: `ref_clk`, `fb_clk`, `rst_n`, `lock`.
Behavior: after reset release, assert `lock` only after at least `need` consecutive reference edges have a recent feedback edge within timing tolerance `tol`; reset clears the streak and lock. Use voltage-domain event logic and `transition(...)`.
Public evaluation contract: the fixed harness runs `tran tran stop=320n maxstep=500p`; public waveform columns are `ref_clk`, `fb_clk`, `rst_n`, and `lock`.

Return exactly one complete Verilog-A code block for `lock_detector.va`.
