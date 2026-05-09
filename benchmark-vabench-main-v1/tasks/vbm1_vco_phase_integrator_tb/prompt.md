Given a voltage-domain DUT module `vco_phase_integrator`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `vco_phase_integrator.va`. Positional port order: `(vctrl phase clk)`.

Required module: `vco_phase_integrator`. Ports, all `electrical`, exactly as named and ordered: `vctrl, phase, clk`.
Behavior: integrate control voltage into a wrapped oscillator phase. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `vctrl phase clk`.

Return exactly one fenced `spectre` code block.
