# Task: vbr1_l2_converter_front_end:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Sample, Hold, and Analog Memory
- Base function: Converter front-end
- Domain: `voltage`
- Target artifact(s): `sample_hold_droop_ref.va`, `tb_sample_hold_droop_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `sample_hold_droop_ref.va`, `tb_sample_hold_droop_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `sample_hold_droop_ref.va` declares module `sample_hold_droop_ref` with positional ports: `vdd`, `vss`, `clk`, `vin`, `vout`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=170n maxstep=0.1n
```

The release harness expects these exact public scalar observables:

- `vin`
- `clk`
- `vout`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `clk`
- `vin`

## Public Behavior Checks

- `sample_tracks_input_after_clk_edge`
- `hold_windows_show_bounded_droop`
- `droop_not_excessive_between_samples`

## Output Contract

Return exactly these source artifacts:

- `sample_hold_droop_ref.va`
- `tb_sample_hold_droop_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `sample_hold_droop_ref` and one minimal EVAS-compatible Spectre testbench.

# Task: sample_hold_droop_smoke

## Objective

Create a pure voltage-domain sample-and-hold model with observable hold droop. The testbench must
produce several sampling and hold windows so EVAS can measure droop behavior.

## DUT Contract

- Module name: `sample_hold_droop_ref`
- Ports, all `electrical`, exactly in this order: `vdd`, `vss`, `clk`, `vin`, `vout`
- Parameters:
  - `vth` real, default `0.45`
  - `tau` real, default `120n`
  - `dt` real, default `0.5n`
  - `trf` real, default `40p`
- Behavior:
  - Sample `V(vin)` on each rising edge of `clk`.
  - Between rising edges, hold the sampled value while adding finite droop toward `V(vss)`.
  - Output should remain in the supply range.
  - Use `@(cross(V(clk) - vth, +1))` and `transition(...)`.

## Testbench Contract

- Use a 0.9 V supply and 0 V reference.
- Drive `clk` with enough rising edges inside the final validation window to create multiple hold intervals.
- Drive `vin` through several distinct levels so the held output changes between samples.
- Instantiate the DUT by positional ports.
- Save these exact scalar names: `vin`, `clk`, `vout`.
- Include the generated DUT file `sample_hold_droop_ref.va`.
