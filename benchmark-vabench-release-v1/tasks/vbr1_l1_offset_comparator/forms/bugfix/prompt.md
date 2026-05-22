# Task: vbr1_l1_offset_comparator:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: Comparators and Decision Circuits
- Base function: Offset comparator
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Supplied/reference support artifact(s): `dut_buggy.va`, `tb_comparator_offset_buggy.scs`, `tb_comparator_offset_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `dut_buggy.va` declares module `cmp_offset_ref` with positional ports: `VDD`, `VSS`, `CLK`, `VINP`, `VINN`, `OUT_P`.
- `dut_fixed.va` declares module `cmp_offset_ref` with positional ports: `VDD`, `VSS`, `CLK`, `VINP`, `VINN`, `OUT_P`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=28n maxstep=20p
```

The release harness expects these exact public scalar observables:

- `CLK`
- `VINP`
- `VINN`
- `OUT_P`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `clocked_low_vinp_phase_latches_low_output`
- `clocked_high_vinp_phase_latches_high_output`
- `output_decisions_match_positive_offset_polarity`
- `expected_safe_window_sequence_LHHHLLL`

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `dut_fixed.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_offset_comparator_bugfix

The provided voltage-domain offset comparator applies the decision polarity
incorrectly around its input offset threshold. Fix the comparator so the output
goes high only when `VINP - VINN` exceeds the positive offset value.

The fixed module must be named `cmp_offset_ref` and use electrical ports `VDD`,
`VSS`, `CLK`, `VINP`, `VINN`, and `OUT_P`. On each rising clock crossing, the
model should latch the comparator decision and drive `OUT_P` between `VSS` and
`VDD` using a smoothed voltage transition.

Use voltage contributions and event-driven state updates. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.
