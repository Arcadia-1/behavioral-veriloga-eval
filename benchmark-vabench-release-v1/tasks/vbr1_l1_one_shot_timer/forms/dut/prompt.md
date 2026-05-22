# Task: vbr1_l1_one_shot_timer:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Digital and Event-Driven Logic
- Base function: One-shot timer
- Domain: `voltage`
- Target artifact(s): `one_shot_timer.va`
- Supplied/reference support artifact(s): `tb_one_shot_timer_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

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

## Public Behavior Checks

- `pulse_goes_high_after_trigger`
- `pulse_width_about_8ns`
- `reset_keeps_pulse_low`

## Output Contract

Return exactly one source artifact named `one_shot_timer.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_one_shot_timer_dut

Write a pure voltage-domain Verilog-A module for a one-shot pulse timer.

The DUT module is `one_shot_timer` with ports `trig, rst_n, pulse`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Use active-low reset to clear any active or pending pulse.
- On a rising `trig` edge while reset is released, assert `pulse` high and schedule a clear event 8 ns later.
- The public stimulus uses non-overlapping trigger pulses; implement fixed-width pulse behavior for those triggers and drive `pulse` through `transition()`.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `one_shot_timer.va`.
