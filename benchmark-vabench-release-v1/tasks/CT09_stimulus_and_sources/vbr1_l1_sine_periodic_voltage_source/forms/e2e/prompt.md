# Task: vbr1_l1_sine_periodic_voltage_source:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Stimulus and Sources
- Base function: Sine/periodic voltage source
- Domain: `voltage`
- Target artifact(s): `multitone.va`, `tb_multitone_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `multitone.va`, `tb_multitone_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

- `multitone_waveform_matches_public_samples`

## Output Contract

Return exactly these source artifacts:

- `multitone.va`
- `tb_multitone_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Sine/periodic voltage source E2E Companion

Write both the Verilog-A behavioral module and a Spectre transient testbench.

This task form is materialized from the already source-controlled `dut`
release gold for `Sine/periodic voltage source`. It exists to make the public
benchmark split complete without inventing a new circuit kernel or a fake
bugfix.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include the behavioral Verilog-A module
- include a transient `tran` analysis
- save the public observables needed by the public behavior checks
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions
