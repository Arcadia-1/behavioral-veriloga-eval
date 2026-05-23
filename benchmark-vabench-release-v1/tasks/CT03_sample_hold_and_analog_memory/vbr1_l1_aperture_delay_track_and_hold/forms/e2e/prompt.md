# Task: vbr1_l1_aperture_delay_track_and_hold:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Sample, Hold, and Analog Memory
- Base function: Aperture-delay track-and-hold
- Domain: `voltage`
- Target artifact(s): `sample_hold_aperture_ref.va`, `tb_sample_hold_aperture_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `sample_hold_aperture_ref.va`, `tb_sample_hold_aperture_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `sample_hold_aperture_ref.va` declares module `sample_hold_aperture_ref` with positional ports: `VDD`, `VSS`, `clk`, `vin`, `vout`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=140n maxstep=100p
```

The release harness expects these exact public scalar observables:

- `vin`
- `clk`
- `vout`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`
- `clk`
- `vin`

## Public Behavior Checks

- `sampled_values_match_aperture_delayed_input`
- `held_output_remains_between_samples`

## Output Contract

Return exactly these source artifacts:

- `sample_hold_aperture_ref.va`
- `tb_sample_hold_aperture_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbr1_l1_aperture_delay_track_and_hold:e2e

Write both the Verilog-A DUT and Spectre testbench for a sample-and-hold with aperture delay.

The DUT module is `sample_hold_aperture_ref` with ports `VDD, VSS, clk, vin, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- On a rising `clk` edge, schedule sampling after a 200 ps aperture delay.
- At the aperture timer event, capture `vin` and hold it on `vout` until the next sample.
- Drive `vout` with smoothed voltage-domain transitions.

Required testbench behavior:
- Drive a changing input around clock edges so aperture-delayed sampling is distinguishable from immediate sampling.
- Save `clk`, `vin`, and `vout`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `sample_hold_aperture_ref.va` and `tb_sample_hold_aperture_ref.scs`.
