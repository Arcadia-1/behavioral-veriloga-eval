Given a voltage-domain DUT module `one_shot_timer`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `one_shot_timer.va`. Positional port order: `(trig rst_n pulse)`.

Required module: `one_shot_timer`. Ports, all `electrical`, exactly as named and ordered: `trig`, `rst_n`, `pulse`.
Behavior: on each rising edge of `trig`, when `rst_n` is high, emit a fixed-width pulse of duration `tpw`; active-low reset clears the pulse. Use `@(cross(...))`, `timer(...)`, voltage-domain contributions, and `transition(...)`.
Public evaluation contract: the fixed harness runs `tran tran stop=260n maxstep=500p`; public waveform columns are `trig`, `rst_n`, and `pulse`.

Return exactly one fenced `spectre` code block.
