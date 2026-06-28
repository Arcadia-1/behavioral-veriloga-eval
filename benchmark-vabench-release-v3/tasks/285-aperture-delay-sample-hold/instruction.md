# Aperture Delay Track And Hold

One-shot DUT-generation task for a voltage-domain aperture-delay
track-and-hold.

## Agent-Visible Input

- `tb_sample_hold_aperture_ref.scs`

## Required Output

- `sample_hold_aperture_ref.va`

## Public Interface

Declare `sample_hold_aperture_ref(VDD, VSS, clk, vin, vout)` with electrical
voltage-domain ports. `clk` uses public `0 V` to `0.9 V` logic levels.

## Functional Contract

- On each rising `clk` transition, schedule a sample after a `400 ps` aperture
  delay.
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
points, use current contributions, `ddt()`, or `idt()`.
