# Task: vbr1_l1_edge_detector:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: Digital and Event-Driven Logic
- Base function: Edge detector
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Supplied/reference support artifact(s): `dut_buggy.va`, `tb_edge_detector_buggy.scs`, `tb_edge_detector_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `dut_buggy.va` declares module `edge_detector` with positional ports: `sig`, `rst_n`, `pulse`.
- `dut_fixed.va` declares module `edge_detector` with positional ports: `sig`, `rst_n`, `pulse`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=180n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `sig`
- `rst_n`
- `pulse`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `pulse_high_at_safe_windows_after_rising_sig_edges`
- `pulse_low_before_next_falling_edge_windows`
- `reset_keeps_pulse_low_before_release`

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `dut_fixed.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_edge_detector_bugfix

The provided voltage-domain edge detector has an edge-polarity bug: it produces
the output pulse on the falling edge of `sig` instead of the rising edge. Fix
the design so it emits one bounded-width pulse after each rising `sig` crossing
while reset is released.

The fixed module must be named `edge_detector` and use electrical ports `sig`,
`rst_n`, and `pulse`. When `rst_n` is low, the pulse output must be low and the
internal one-shot state must be cleared. When reset is released, each rising
edge of `sig` should arm a pulse with the configured width and then clear it.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
