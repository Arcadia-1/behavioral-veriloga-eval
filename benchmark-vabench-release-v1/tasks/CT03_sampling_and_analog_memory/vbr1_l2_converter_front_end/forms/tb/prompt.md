# Task: vbr1_l2_converter_front_end:tb

## Release Task Contract

- Form: `tb`
- Level: `L2`
- Category: Sampling and Analog Memory
- Base function: Converter front-end
- Domain: `voltage`
- Target artifact(s): `tb_sample_hold_droop_ref.scs`
- Supplied/reference support artifact(s): `sample_hold_droop_ref.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

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

Return exactly one source artifact named `tb_sample_hold_droop_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Converter front-end chain Testbench Companion

Write a Spectre transient testbench for the `Converter front-end` behavioral
Verilog-A release task. This is the testbench-generation companion for an
already materialized end-to-end task.

The testbench should instantiate the same behavioral DUT or system module used
by the corresponding end-to-end form, drive an aperture-sensitive sampling
scenario, save the observable waveform or metric signals, and preserve the
EVAS/Spectre validation contract.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- save `vin`, `clk`, `vout`, `valid`, and `coarse`
- include or instantiate the Verilog-A behavioral module under test
- exercise aperture-delayed sampling, bounded hold droop, coarse decision, and
  valid-pulse behavior
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions
