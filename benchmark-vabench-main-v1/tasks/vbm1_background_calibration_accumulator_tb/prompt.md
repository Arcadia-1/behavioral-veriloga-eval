Given a voltage-domain DUT module `background_calibration_accumulator`, generate only a Spectre testbench. Do not generate Verilog-A modules. Include file: `background_calibration_accumulator.va`. Positional port order: `(clk rst err accum)`.

Required module: `background_calibration_accumulator`. Ports, all `electrical`, exactly as named and ordered: `clk, rst, err, accum`.
Behavior: slowly accumulate signed background error with saturation. Use Spectre-compatible Verilog-A, voltage-domain contributions, bounded internal state when needed, and `transition(...)` on driven outputs.
Public evaluation contract: the fixed harness runs exactly `tran tran stop=220n maxstep=500p` and saves waveform columns `clk rst err accum`.

Return exactly one fenced `spectre` code block.
