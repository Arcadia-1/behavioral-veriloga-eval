# Task: vbr1_l1_hysteresis_comparator:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Comparator and Decision Circuits
- Base function: Hysteresis comparator
- Domain: `voltage`
- Target artifact(s): `tb_cmp_hysteresis_ref.scs`
- Supplied/reference support artifact(s): `cmp_hysteresis.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `cmp_hysteresis.va` declares module `cmp_hysteresis` with positional ports: `VINN`, `VINP`, `OUTN`, `OUTP`, `VSS`, `VDD`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=80n maxstep=100p
```

The release harness expects these exact public scalar observables:

- `vinp`
- `vinn`
- `out_p`
- `out_n`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `gnd`
- `vinp`
- `vinn`

## Public Behavior Checks

- `output_shows_hysteresis_window`
- `upward_and_downward_trip_points_are_separated`

## Output Contract

Return exactly one source artifact named `tb_cmp_hysteresis_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Hysteresis comparator Testbench Companion

Write a Spectre transient testbench for the `Hysteresis comparator` behavioral
Verilog-A release task. This is the testbench-generation companion for an
already materialized end-to-end task.

The testbench should instantiate the same behavioral DUT or system module used
by the corresponding end-to-end form, drive the public transient scenario, save
the observable waveform or metric signals, and preserve the EVAS/Spectre
validation contract.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include `cmp_hysteresis.va` via `ahdl_include`
- instantiate `cmp_hysteresis` with scalar nodes `vinn`, `vinp`, `out_n`,
  `out_p`, `gnd`, and `vdd`
- include `tran tran stop=80n maxstep=100p`
- save `vinp`, `vinn`, `out_p`, and `out_n`
- drive the differential input upward through `+vhys/2` and downward through
  `-vhys/2`, with an intermediate hold region between the two thresholds
- make the upward and downward trip points visibly separated in the saved
  waveform
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions
