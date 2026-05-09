Write a pure Verilog-A `vco_phase_integrator` DUT and a minimal Spectre testbench.

Required module: `vco_phase_integrator`. Ports, all `electrical`, exactly as named and ordered: `vctrl, phase, clk`.
Behavior: integrate control voltage into a wrapped oscillator phase. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=180n maxstep=500p` and saves waveform columns `vctrl phase clk`.

Testbench requirements: include `vco_phase_integrator.va`, instantiate the DUT with positional port order `(vctrl phase clk)`, save `vctrl phase clk`, and run the same transient condition described in the public contract. Return one `verilog-a` block and one `spectre` block.
