# Task: vbr1_l2_serializer_frame_alignment_flow:tb

## Release Task Contract

- Form: `tb`
- Level: `L2`
- Category: Digital and Event-Driven Logic
- Base function: Serializer frame-alignment flow
- Domain: `voltage`
- Target artifact(s): `tb_serializer_frame_alignment_ref.scs`
- Supplied/reference support artifact(s): `serializer_frame_alignment_ref.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `serializer_frame_alignment_ref.va` declares module `serializer_frame_alignment_ref` with positional ports: `vdd`, `vss`, `clk`, `load`, `din7`, `din6`, `din5`, `din4`, `din3`, `din2`, `din1`, `din0`, `sout`, `frame`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=130n maxstep=0.1n
```

The release harness expects these exact public scalar observables:

- `clk`
- `load`
- `frame`
- `sout`
- `din7`
- `din6`
- `din5`
- `din4`
- `din3`
- `din2`
- `din1`
- `din0`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `clk`
- `load`
- `din7`
- `din6`
- `din5`
- `din4`
- `din3`
- `din2`
- `din1`
- `din0`

## Public Behavior Checks

- `transient_analysis_present`
- `public_observables_saved`
- `dut_or_system_instantiated`

## Output Contract

Return exactly one source artifact named `tb_serializer_frame_alignment_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Serializer frame-alignment flow Testbench Companion

Write a Spectre transient testbench for the `Serializer frame-alignment flow` behavioral
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
