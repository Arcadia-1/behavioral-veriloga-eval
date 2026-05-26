# Task: vbr1_l1_clocked_sample_and_hold:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Sampling and Analog Memory
- Base function: Clocked sample-and-hold
- Domain: `voltage`
- Target artifact(s): `tb_sample_hold_ref.scs`
- Supplied/reference support artifact(s): `sample_hold.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `sample_hold.va` declares module `sample_hold` with positional ports: `VDD`, `VSS`, `IN`, `CLK`, `OUT`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=1u maxstep=2n
```

The release harness expects these exact public scalar observables:

- `in`
- `clk`
- `out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `in`
- `clk`

## Public Behavior Checks

- `sh_output_tracks_input_at_edges`
- `sh_output_held_between_edges`

## Output Contract

Return exactly one source artifact named `tb_sample_hold_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Clocked sample-and-hold Testbench Companion

Write a Spectre transient testbench for the `Clocked sample-and-hold` behavioral
Verilog-A release task. This is the testbench-generation companion for an
already materialized end-to-end task.

The testbench should instantiate the same behavioral DUT or system module used
by the corresponding end-to-end form, drive the public transient scenario, save
the observable waveform or metric signals, and preserve the EVAS/Spectre
validation contract.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- save the public observables needed by the checker
- include or instantiate the Verilog-A behavioral module under test
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions
