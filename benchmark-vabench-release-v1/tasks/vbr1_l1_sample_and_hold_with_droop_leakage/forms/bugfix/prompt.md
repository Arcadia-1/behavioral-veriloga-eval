# Task: vbr1_l1_sample_and_hold_with_droop_leakage:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: Sample, Hold, and Analog Memory
- Base function: Sample-and-hold with droop/leakage
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Supplied/reference support artifact(s): `dut_buggy.va`, `tb_leaky_hold_buggy.scs`, `tb_leaky_hold_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `dut_buggy.va` declares module `leaky_hold` with positional ports: `sample`, `rst`, `vout`.
- `dut_fixed.va` declares module `leaky_hold` with positional ports: `sample`, `rst`, `vout`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=170n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `sample`
- `rst`
- `vout`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `sample_event_captures_high_hold_level`
- `safe_window_vout_decays_monotonically`
- `reset_window_clears_output_near_zero`

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `dut_fixed.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_leaky_hold_bugfix

The provided voltage-domain leaky-hold model has a leakage bug: after a sample
event it keeps the held output level instead of applying the intended gradual
decay. Fix the design so it captures a high held value on each sample edge,
decays while reset is low, and clears promptly when reset is high.

The fixed module must be named `leaky_hold` and use electrical ports `sample`,
`rst`, and `vout`. On a rising `sample` threshold crossing, the held value
should be driven near the configured sampled level. A periodic leakage update
should reduce the held value over time while `rst` is low. When `rst` is high,
the held value and output should clear near zero.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
