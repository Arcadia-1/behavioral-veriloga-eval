Write a pure Verilog-A sample-and-hold DUT with aperture delay and a minimal Spectre testbench.

Required DUT module: `sample_hold_aperture_ref`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `clk`, `vin`, `vout`.

DUT behavior:
- On each rising edge of `clk`, arm a sample event at `$abstime + taperture`.
- At that aperture event, capture `vin` and hold it on `vout` until the next capture.
- Use voltage-domain contributions and `transition(...)`.

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Provide `VDD=0.9 V` and `VSS=0 V`.
- Drive `clk` with repeated rising edges.
- Drive `vin` with changing plateaus so aperture timing can be observed.
- Save plain scalar names: `vin`, `clk`, `vout`.
- Run exactly `tran tran stop=140n maxstep=100p`.
- Include `sample_hold_aperture_ref.va` using `ahdl_include`.

Return two fenced code blocks: one `verilog-a` block and one `spectre` block.
