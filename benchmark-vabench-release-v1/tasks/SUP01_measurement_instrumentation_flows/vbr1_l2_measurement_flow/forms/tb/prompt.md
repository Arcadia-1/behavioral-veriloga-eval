# Task: vbr1_l2_measurement_flow:tb

## Release Task Contract

- Form: `tb`
- Level: `L2`
- Category: Measurement Instrumentation Flows
- Base function: Measurement flow
- Domain: `voltage`
- Target artifact(s): `tb_final_step_file_metric_ref.scs`
- Supplied/reference support artifact(s): `final_step_file_metric_ref.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `final_step_file_metric_ref.va` declares module `final_step_file_metric_ref` with positional ports: `VDD`, `VSS`, `ref`, `metric_out`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=80n maxstep=20p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `ref`
- `metric_out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`
- `ref`

## Public Behavior Checks

- `ref_edges_counted_on_expected_grid`
- `metric_out_normalizes_final_edge_count`
- `final_step_writes_candidate_metric_file`

## Output Contract

Return exactly one source artifact named `tb_final_step_file_metric_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Measurement flow Testbench Companion

Write a Spectre transient testbench for the `Measurement flow` behavioral
Verilog-A release task. This is the testbench-generation companion for an
already materialized end-to-end task.

The testbench should instantiate the same behavioral DUT or system module used
by the corresponding end-to-end form, drive the public transient scenario, save
the observable waveform or metric signals, and preserve the EVAS/Spectre
validation contract.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- save the public observables needed by the public behavior checks
- include or instantiate the Verilog-A behavioral module under test
- satisfy the named behavior checks using only public waveforms and side outputs
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions
