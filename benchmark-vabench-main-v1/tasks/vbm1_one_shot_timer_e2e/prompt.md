Write a pure Verilog-A one-shot timer DUT and a minimal Spectre testbench.

Required module: `one_shot_timer`. Ports, all `electrical`, exactly as named and ordered: `trig`, `rst_n`, `pulse`.
Behavior: on each rising edge of `trig`, when `rst_n` is high, emit a fixed-width pulse of duration `tpw`; active-low reset clears the pulse. Use `@(cross(...))`, `timer(...)`, voltage-domain contributions, and `transition(...)`.
Public evaluation contract: the fixed harness runs `tran tran stop=260n maxstep=500p`; public waveform columns are `trig`, `rst_n`, and `pulse`.

Testbench requirements: include `one_shot_timer.va`, drive repeated `trig` rising edges after reset release, instantiate `(trig rst_n pulse)`, save `trig rst_n pulse`, and run exactly `tran tran stop=260n maxstep=500p`. Return one `verilog-a` block and one `spectre` block.
