# Aperture Delay Track And Hold

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Sampling and Analog Memory
- Base function: Aperture-delay track-and-hold
- Domain: `voltage`
- Target artifact(s): `sample_hold_aperture_ref.va`
- Supplied/reference support artifact(s): `tb_sample_hold_aperture_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `sample_hold_aperture_ref.va` declares module `sample_hold_aperture_ref` with positional ports: `VDD`, `VSS`, `clk`, `vin`, `vout`.
- All ports are electrical. `clk` uses voltage-coded logic levels.

## Public Parameter Contract

The starter declares these public parameters. Preserve them as overrideable
parameters unless an equivalent public interface is supplied:

- `vth = 0.45 V`: rising-clock threshold for detecting a sample request.
- `taperture = 200 ps from [0:inf)`: aperture delay from the rising clock
  crossing to the instant where `vin` is captured.
- `tedge = 50 ps from (0:inf)`: smoothing time for output transitions.

## Public Testbench And Observable Contract

The visible smoke testbench uses this transient setting:

```spectre
tran tran stop=140n maxstep=100p
```

The release harness expects these exact public scalar observables:

- `vin`
- `clk`
- `vout`

Do not emit checker logic, private test hooks, simulator-private side channels,
or a replacement Spectre testbench.

## Public Behavior Checks

- `sampled_values_match_aperture_delayed_input`
- `held_output_remains_between_samples`

## Output Contract

Return exactly one source artifact named `sample_hold_aperture_ref.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a pure voltage-domain Verilog-A module for a sample-and-hold with
aperture delay.

The DUT module is `sample_hold_aperture_ref` with ports `VDD, VSS, clk, vin,
vout`. Digital-control ports use voltage-coded logic levels.

Required behavior:
- On a rising `clk` crossing of `vth`, schedule sampling after `taperture`.
- At the delayed aperture instant, capture the current value of `vin`, not the
  value present exactly at the clock edge.
- Hold the captured value on `vout` until the next delayed sample.
- Drive `vout` with smoothed voltage-domain transitions.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.
