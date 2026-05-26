# Task: vbr1_l2_converter_front_end:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Sampling and Analog Memory
- Base function: Converter front-end
- Domain: `voltage`
- Target artifact(s): `sample_hold_droop_ref.va`, `tb_sample_hold_droop_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `sample_hold_droop_ref.va`, `tb_sample_hold_droop_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `sample_hold_droop_ref.va` declares module `sample_hold_droop_ref` with positional ports: `vdd`, `vss`, `clk`, `vin`, `vout`, `valid`, `coarse`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=170n maxstep=0.1n
```

The release harness expects these exact public scalar observables:

- `vin`
- `clk`
- `vout`
- `valid`
- `coarse`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `clk`
- `vin`

## Public Behavior Checks

- `aperture_delayed_sample_tracks_vin`
- `hold_windows_show_bounded_droop`
- `coarse_decision_matches_held_sample`
- `valid_pulses_mark_completed_samples`

## Output Contract

Return exactly these source artifacts:

- `sample_hold_droop_ref.va`
- `tb_sample_hold_droop_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `sample_hold_droop_ref` and one minimal
voltage-domain Spectre transient testbench.

## Objective

Create a pure voltage-domain converter front-end chain: aperture-delayed
sampling, hold droop, a coarse threshold decision, and a valid pulse that marks
completed samples.

## DUT Contract

- Module name: `sample_hold_droop_ref`
- Ports, all `electrical`, exactly in this order: `vdd`, `vss`, `clk`, `vin`,
  `vout`, `valid`, `coarse`
- Parameters:
  - `vth` real, default `0.45`
  - `tau` real, default `90n`
  - `dt` real, default `0.5n`
  - `taperture` real, default `200p`
  - `valid_width` real, default `2n`
  - `trf` real, default `40p`
- Behavior:
  - On each rising edge of `clk`, wait `taperture`, then sample `V(vin)`.
  - Between samples, hold the sampled value on `vout` while adding finite
    droop toward `V(vss)`.
  - Drive `coarse` high when the sampled value is above `vth`, otherwise low.
  - Pulse `valid` after each aperture-delayed sample completes.
  - Keep all outputs in the supply range and use `transition(...)`.

## Testbench Contract

- Use a 0.9 V supply and 0 V reference.
- Drive `clk` with enough rising edges inside the final validation window to create multiple hold intervals.
- Drive `vin` transitions near selected clock edges so aperture-delayed sampling
  is distinguishable from immediate edge sampling.
- Instantiate the DUT by positional ports.
- Save these exact scalar names: `vin`, `clk`, `vout`, `valid`, `coarse`.
- Include the generated DUT file `sample_hold_droop_ref.va`.
