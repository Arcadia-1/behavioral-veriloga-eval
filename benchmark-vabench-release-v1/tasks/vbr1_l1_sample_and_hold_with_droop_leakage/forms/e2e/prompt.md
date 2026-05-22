# Task: vbr1_l1_sample_and_hold_with_droop_leakage:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Sample, Hold, and Analog Memory
- Base function: Sample-and-hold with droop/leakage
- Domain: `voltage`
- Target artifact(s): `leaky_hold.va`, `tb_leaky_hold_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `leaky_hold.va`, `tb_leaky_hold_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `leaky_hold.va` declares module `leaky_hold` with positional ports: `sample`, `rst`, `vout`.

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

Public stimulus/source nodes visible in the reference harness include:

- `sample`
- `rst`

## Public Behavior Checks

- `capture_reaches_high_level`
- `held_output_droops_over_time`
- `reset_clears_output`
- `second_capture_recovers`

## Output Contract

Return exactly these source artifacts:

- `leaky_hold.va`
- `tb_leaky_hold_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_leaky_hold_e2e

Write both the Verilog-A DUT and Spectre testbench for a leaky sample-and-hold.

The DUT module is `leaky_hold` with ports `sample, rst, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- A rising `sample` edge captures a fixed 0.75 V held level.
- A 1 ns timer applies exponential droop by multiplying the held value by 0.985 while reset is low.
- High `rst` clears the held value; drive `vout` through `transition()`.

Required testbench behavior:
- Generate capture events, an observable droop interval, reset clearing, and a second capture.
- Save `sample`, `rst`, and `vout`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `leaky_hold.va` and `tb_leaky_hold_ref.scs`.
