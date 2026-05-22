# Task: vbr1_l1_one_shot_timer:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: Digital and Event-Driven Logic
- Base function: One-shot timer
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Supplied/reference support artifact(s): `dut_buggy.va`, `tb_one_shot_timer_buggy.scs`, `tb_one_shot_timer_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `dut_buggy.va` declares module `one_shot_timer` with positional ports: `trig`, `rst_n`, `pulse`.
- `dut_fixed.va` declares module `one_shot_timer` with positional ports: `trig`, `rst_n`, `pulse`.

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

- `trigger_edges_generate_safe_window_pulses`
- `pulse_clears_after_configured_width`
- `reset_falling_edge_clears_active_pulse_before_timeout`

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `dut_fixed.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_one_shot_timer_bugfix

The provided voltage-domain one-shot timer has a reset-priority bug: a reset
asserted while the output pulse is active does not immediately clear the pulse.
Fix the design so reset has priority over the pending one-shot timeout.

The fixed module must be named `one_shot_timer` and use electrical ports
`trig`, `rst_n`, and `pulse`. While `rst_n` is low, `pulse` must remain low and
any pending timeout must be disarmed. When `rst_n` is high, each rising `trig`
crossing should start one pulse of the configured width. If reset falls during
that pulse, the pulse should clear promptly rather than waiting for the timer.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
