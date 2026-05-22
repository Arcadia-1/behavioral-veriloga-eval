# Task: vbr1_l1_offset_comparator:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Comparators and Decision Circuits
- Base function: Offset comparator
- Domain: `voltage`
- Target artifact(s): `cmp_offset_ref.va`, `tb_comparator_offset_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `cmp_offset_ref.va`, `tb_comparator_offset_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `cmp_offset_ref.va` declares module `cmp_offset_ref` with positional ports: `VDD`, `VSS`, `CLK`, `VINP`, `VINN`, `OUT_P`.

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

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`
- `CLK`
- `VINP`
- `VINN`

## Public Behavior Checks

- `clocked_output_sequence_LHHHLLL`
- `offset_threshold_affects_borderline_decisions`

## Output Contract

Return exactly these source artifacts:

- `cmp_offset_ref.va`
- `tb_comparator_offset_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_offset_comparator_e2e

Write both the Verilog-A DUT and Spectre testbench for a clocked comparator with input offset.

The DUT module is `cmp_offset_ref` with ports `VDD, VSS, CLK, VINP, VINN, OUT_P`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- On each rising `CLK` edge, compare `VINP - VINN` against an internal positive offset threshold.
- Drive `OUT_P` to the supply level for a high decision and to `VSS` for a low decision.
- Use smoothed voltage-domain output transitions.

Required testbench behavior:
- Sweep `VINP` around `VINN` while clocking the comparator.
- Save the clock, differential inputs, and output so low/high/low decisions are visible.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `cmp_offset_ref.va` and `tb_comparator_offset_ref.scs`.
