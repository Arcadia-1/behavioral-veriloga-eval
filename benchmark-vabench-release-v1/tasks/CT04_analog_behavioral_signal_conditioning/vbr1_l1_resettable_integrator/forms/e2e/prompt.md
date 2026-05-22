# Task: vbr1_l1_resettable_integrator:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Analog Behavioral Signal Conditioning
- Base function: Resettable integrator
- Domain: `voltage`
- Target artifact(s): `resettable_integrator.va`, `tb_resettable_integrator_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `resettable_integrator.va`, `tb_resettable_integrator_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

- `pre_reset_output_integrates_up`
- `reset_clears_integrator`
- `post_reset_integration_restarts`

## Output Contract

Return exactly these source artifacts:

- `resettable_integrator.va`
- `tb_resettable_integrator_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_resettable_integrator_e2e

Write both the Verilog-A DUT and Spectre testbench for a resettable timer integrator.

The DUT module is `resettable_integrator` with ports `vin, rst, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Use a 1 ns timer update to integrate `vin` into an internal accumulator.
- High `rst` clears the accumulator to 0 V.
- Clamp the accumulator between 0 V and 0.85 V and drive `vout` with `transition()`.

Required testbench behavior:
- Drive a positive input, reset pulse, and post-reset positive input interval.
- Save `vin`, `rst`, and `vout` across pre-reset integration, reset clearing, and restart windows.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `resettable_integrator.va` and `tb_resettable_integrator_ref.scs`.
