Create only the DUT Verilog-A model for `vco_phase_integrator`. Do not generate a testbench.

Required module: `vco_phase_integrator`. Ports, all `electrical`, exactly as named and ordered: `vctrl, phase, clk`.
Behavior: integrate control voltage into a wrapped oscillator phase. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `vctrl phase clk`.

Return exactly one complete Verilog-A code block for `vco_phase_integrator.va`.
