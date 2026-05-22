# Task: vbr1_l1_one_shot_timer:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Digital and Event-Driven Logic
- Base function: One-shot timer
- Domain: `voltage`
- Target artifact(s): `one_shot_timer.va`, `tb_one_shot_timer_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `one_shot_timer.va`, `tb_one_shot_timer_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

Return exactly these source artifacts:

- `one_shot_timer.va`
- `tb_one_shot_timer_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_one_shot_timer_e2e

Write both the Verilog-A DUT and Spectre testbench for a one-shot pulse timer.

The DUT module is `one_shot_timer` with ports `trig, rst_n, pulse`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Use active-low reset to clear any active or pending pulse.
- On a rising `trig` edge while reset is released, assert `pulse` high and schedule a clear event 8 ns later.
- The public stimulus uses non-overlapping trigger pulses; implement fixed-width pulse behavior for those triggers and drive `pulse` through `transition()`.

Required testbench behavior:
- Drive multiple trigger events with reset released and include windows before, during, and after each pulse.
- Save `trig`, `rst_n`, and `pulse`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `one_shot_timer.va` and `tb_one_shot_timer_ref.scs`.
