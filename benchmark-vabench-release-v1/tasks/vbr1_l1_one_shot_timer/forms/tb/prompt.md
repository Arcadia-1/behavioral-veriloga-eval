# Task: vbr1_l1_one_shot_timer:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Digital and Event-Driven Logic
- Base function: One-shot timer
- Domain: `voltage`
- Target artifact(s): `tb_one_shot_timer_ref.scs`
- Supplied/reference support artifact(s): `one_shot_timer.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `one_shot_timer.va` declares module `one_shot_timer` with positional ports: `trig`, `rst_n`, `pulse`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=260n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `trig`
- `rst_n`
- `pulse`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `rst_n`
- `trig`

## Public Behavior Checks

- `pulse_goes_high_after_trigger`
- `pulse_width_about_8ns`
- `reset_keeps_pulse_low`

## Output Contract

Return exactly one source artifact named `tb_one_shot_timer_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_one_shot_timer_tb

Write a Spectre testbench for a one-shot pulse timer DUT.

The DUT module is `one_shot_timer` with ports `trig, rst_n, pulse`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `one_shot_timer.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Use active-low reset to clear any active or pending pulse.
- On a rising `trig` edge while reset is released, assert `pulse` high and schedule a clear event 8 ns later.
- The public stimulus uses non-overlapping trigger pulses; implement fixed-width pulse behavior for those triggers and drive `pulse` through `transition()`.

Stimulus and observability requirements:
- Drive multiple trigger events with reset released and include windows before, during, and after each pulse.
- Save `trig`, `rst_n`, and `pulse`.

Return exactly one Spectre testbench file named `tb_one_shot_timer_ref.scs`.
