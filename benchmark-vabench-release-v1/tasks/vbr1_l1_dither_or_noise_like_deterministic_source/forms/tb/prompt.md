# Task: vbr1_l1_dither_or_noise_like_deterministic_source:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Stimulus and Sources
- Base function: Dither or noise-like deterministic source
- Domain: `voltage`
- Target artifact(s): `tb_noise_gen_ref.scs`
- Supplied/reference support artifact(s): `noise_gen.va`, `noise_gen_ref.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `noise_gen.va` declares module `noise_gen` with positional ports: `vin_i`, `vout_o`.
- `noise_gen_ref.va` declares module `noise_gen` with positional ports: `vin_i`, `vout_o`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=500n maxstep=1n
```

The release harness expects these exact public scalar observables:

- `vin_i`
- `vout_o`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vin_i`

## Public Behavior Checks

- `transient_analysis_present`
- `public_observables_saved`
- `dut_or_system_instantiated`

## Output Contract

Return exactly one source artifact named `tb_noise_gen_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Dither or noise-like deterministic source Testbench Companion

Write a Spectre transient testbench for the `Dither or noise-like deterministic source` behavioral
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
