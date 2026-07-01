# Aperture Delay Sample Hold

One-shot DUT-generation task for a voltage-domain aperture-delay
track-and-hold.

## Agent-Visible Input

- `tb_sample_hold_aperture_ref.scs`

## Required Output

- `sample_hold_aperture_ref.va`

## Public Interface

Declare `sample_hold_aperture_ref(VDD, VSS, clk, vin, vout)` with electrical
voltage-domain ports. `clk` uses public `0 V` to `0.9 V` logic levels.

## Public Parameter Contract

Preserve these public parameters when using the supplied starter interface:

- `vth = 0.45 V`: rising-clock threshold.
- `taperture = 200 ps from [0:inf)`: delay from the rising `clk` crossing to
  the sampled aperture instant.
- `tedge = 50 ps from (0:inf)`: output transition smoothing time.

## Functional Contract

- On each rising `clk` transition through `vth`, schedule a sample after
  `taperture`.
- At the delayed aperture instant, capture the current value of `vin`; do not
  capture the value present exactly at the clock edge.
- After a short settling interval, `vout` should be close to the delayed
  sampled value and should hold until the next delayed sample.
- The harness exercises a broad voltage range, so the held output sequence
  should follow multiple delayed input levels.
- Drive output changes as smooth voltage-domain transitions.

## Modeling Constraints

Return only the DUT. Drive `vout` with voltage contributions. Do not modify or
emit the support testbench, add checker logic, hard-code private waveform sample
points, add simulator-private side channels, use current contributions, `ddt()`,
or `idt()`.
