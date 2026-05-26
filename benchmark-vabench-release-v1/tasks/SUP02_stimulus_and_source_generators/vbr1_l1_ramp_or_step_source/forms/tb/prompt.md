# Task: vbr1_l1_ramp_or_step_source:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Stimulus and Source Generators
- Base function: Periodic phase-ramp guard source
- Domain: `voltage`
- Target artifact(s): `tb_bound_step_period_guard_ref.scs`
- Supplied/reference support artifact(s): `bound_step_period_guard_ref.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `bound_step_period_guard_ref.va` declares module `bound_step_period_guard_ref` with positional ports: `VDD`, `VSS`, `guard_out`, `phase_out`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=34n maxstep=20n errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `guard_out`
- `phase_out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`

## Public Behavior Checks

- `periodic_phase_ramp_wraps`
- `guard_pulse_repeats_each_period`
- `guard_pulse_width_fraction`

## Output Contract

Return exactly one source artifact named `tb_bound_step_period_guard_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Periodic phase-ramp guard source TB Companion

Write a Spectre transient testbench for this behavioral release task.

This task form is materialized from the already source-controlled `e2e`
release gold for `Periodic phase-ramp guard source`. It exists to make the public
benchmark split complete without inventing a new circuit kernel or a fake
bugfix.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- save the public observables needed by the public behavior checks
- include or instantiate the behavioral module under test
- satisfy the named behavior checks using only public waveforms and side outputs
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions
