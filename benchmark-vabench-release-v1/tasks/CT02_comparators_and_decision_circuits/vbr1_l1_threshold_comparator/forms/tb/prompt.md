# Task: vbr1_l1_threshold_comparator:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Comparators and Decision Circuits
- Base function: Threshold comparator
- Domain: `voltage`
- Target artifact(s): `tb_comparator_ref.scs`
- Supplied/reference support artifact(s): `comparator.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `comparator.va` declares module `comparator` with positional ports: `VDD`, `VSS`, `VINP`, `VINN`, `OUT_P`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=30n maxstep=0.1n
```

The release harness expects these exact public scalar observables:

- `vinp`
- `vinn`
- `out_p`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `vinp`
- `vinn`

## Public Behavior Checks

- `transient_analysis_present`
- `public_observables_saved`
- `dut_or_system_instantiated`
- `stimulus_exercises_negative_positive_negative_differential`
- `out_p_has_rising_and_falling_decisions`

## Output Contract

Return exactly one source artifact named `tb_comparator_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Threshold comparator Testbench Companion

Write a Spectre transient testbench for the `Threshold comparator` behavioral
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
- drive `vinp - vinn` through a negative, positive, and negative sequence so
  both comparator output edges are visible in one run
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions
