# Task: vbr1_l1_settling_time_detector:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Measurement and Testbench Instrumentation
- Base function: Settling response measurement helper
- Domain: `voltage`
- Target artifact(s): `tb_settling_time_measurement_tb_ref.scs`
- Supplied/reference support artifact(s): `settling_time_measurement_tb.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `settling_time_measurement_tb.va` declares module `settling_time_measurement_tb` with positional ports: `step`, `vout`, `done`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=160n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `step`
- `vout`
- `done`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `step`

## Public Behavior Checks

- `vout_rises_monotonically_toward_step`
- `done_low_before_boundary`
- `done_high_in_late_settled_window`

## Output Contract

Return exactly one source artifact named `tb_settling_time_measurement_tb_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_settling_time_measurement_tb_tb

Write a Spectre testbench for a settling response measurement helper DUT.

The DUT module is `settling_time_measurement_tb` with ports `step, vout, done`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `settling_time_measurement_tb.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Use a 1 ns timer update with `y += 0.04 * (V(step) - y)` to model a settling response.
- Drive `vout` from `y`; assert `done` only after 120 ns and once `y` is above 0.75 V.
- This is a measurement-helper behavior task, not a true bugfix task.

Stimulus and observability requirements:
- Apply a step input and run past the 120 ns settling boundary.
- Save `step`, `vout`, and `done` with enough samples before and after the boundary.

Review caveat: This is a normal measurement-helper behavior task. It is not a bugfix task; exact 120 ns boundary semantics belong in conformance.

Return exactly one Spectre testbench file named `tb_settling_time_measurement_tb_ref.scs`.
