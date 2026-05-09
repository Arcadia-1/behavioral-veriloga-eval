The following lock detector incorrectly mirrors reset instead of checking phase/frequency alignment. Fix it without changing the public interface.

```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module lock_detector(ref_clk, fb_clk, rst_n, lock);
    input ref_clk, fb_clk, rst_n; output lock; electrical ref_clk, fb_clk, rst_n, lock;
    analog begin V(lock) <+ transition(V(rst_n), 0, 500p, 500p); end
endmodule

```

Required module: `lock_detector`. Ports, all `electrical`, exactly as named and ordered: `ref_clk`, `fb_clk`, `rst_n`, `lock`.
Behavior: after reset release, assert `lock` only after at least `need` consecutive reference edges have a recent feedback edge within timing tolerance `tol`; reset clears the streak and lock. Use voltage-domain event logic and `transition(...)`.
Public evaluation contract: the fixed harness runs `tran tran stop=320n maxstep=500p`; public waveform columns are `ref_clk`, `fb_clk`, `rst_n`, and `lock`.

Return exactly one complete Verilog-A code block for module `lock_detector`.
