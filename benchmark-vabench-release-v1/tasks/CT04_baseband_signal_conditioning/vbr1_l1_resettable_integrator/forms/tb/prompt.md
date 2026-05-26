# Task: vbr1_l1_resettable_integrator:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Resettable integrator
- Domain: `voltage`
- Target artifact(s): `tb_resettable_integrator_ref.scs`
- Supplied/reference support artifact(s): `resettable_integrator.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `resettable_integrator.va` declares module `resettable_integrator` with positional ports: `vin`, `rst`, `vout`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=320n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `vin`
- `rst`
- `vout`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `rst`
- `vin`

## Public Behavior Checks

- `input_drive_present`
- `reset_pulse_exercised`
- `pre_reset_output_integrates_up`
- `reset_clears_integrator`
- `post_reset_integration_restarts`

## Output Contract

Return exactly one source artifact named `tb_resettable_integrator_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Spectre testbench for a resettable timer integrator DUT.

The DUT module is `resettable_integrator` with ports `vin, rst, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `resettable_integrator.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Use a 1 ns timer update to integrate `vin` into an internal accumulator.
- High `rst` clears the accumulator to 0 V.
- Clamp the accumulator between 0 V and 0.85 V and drive `vout` with `transition()`.

Stimulus and observability requirements:
- Drive a positive input, reset pulse, and post-reset positive input interval.
- Save `vin`, `rst`, and `vout` across pre-reset integration, reset clearing, and restart windows.
