Write a pure Verilog-A lock detector and a minimal Spectre testbench.

Required module: `lock_detector`. Ports, all `electrical`, exactly as named and ordered: `ref_clk`, `fb_clk`, `rst_n`, `lock`.
Behavior: after reset release, assert `lock` only after at least `need` consecutive reference edges have a recent feedback edge within timing tolerance `tol`; reset clears the streak and lock. Use voltage-domain event logic and `transition(...)`.
Public evaluation contract: the fixed harness runs `tran tran stop=320n maxstep=500p`; public waveform columns are `ref_clk`, `fb_clk`, `rst_n`, and `lock`.

Testbench requirements: include `lock_detector.va`, drive `ref_clk` and `fb_clk` misaligned early and aligned later, instantiate `(ref_clk fb_clk rst_n lock)`, save `ref_clk fb_clk rst_n lock`, and run exactly `tran tran stop=320n maxstep=500p`. Return one `verilog-a` block and one `spectre` block.
