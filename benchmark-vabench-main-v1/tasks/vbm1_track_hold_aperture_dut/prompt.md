Create only the DUT Verilog-A model for the `track_hold_aperture` circuit function.
Do not generate a testbench; the evaluator will use a fixed public harness.

Required module: `sample_hold_aperture_ref`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `clk`, `vin`, `vout`.

Behavior:
- On each rising edge of `clk`, arm a sample event at `$abstime + taperture`.
- At that aperture event, capture `vin` and hold it on `vout` until the next capture.
- Use voltage-domain contributions and `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=140n maxstep=100p`.
- Public waveform columns are `vin`, `clk`, and `vout`.

Return exactly one complete Verilog-A code block for `sample_hold_aperture_ref.va`.
