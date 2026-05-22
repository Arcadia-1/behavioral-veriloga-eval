# Task: vbr1_l1_sine_periodic_voltage_source:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Stimulus and Sources
- Base function: Sine/periodic voltage source
- Domain: `voltage`
- Target artifact(s): `tb_multitone_ref.scs`
- Supplied/reference support artifact(s): `multitone.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `multitone.va` declares module `multitone` with positional ports: `OUT`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=500n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `OUT`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `transient_analysis_present`
- `public_observables_saved`
- `dut_or_system_instantiated`

## Output Contract

Return exactly one source artifact named `tb_multitone_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Sine/periodic voltage source TB Companion

Write a Spectre transient testbench for this behavioral release task.

This task form is materialized from the already source-controlled `dut`
release gold for `Sine/periodic voltage source`. It exists to make the public
benchmark split complete without inventing a new circuit kernel or a fake
bugfix.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- save the public observables needed by the checker
- include or instantiate the behavioral module under test
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions
