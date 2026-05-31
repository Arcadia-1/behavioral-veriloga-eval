# Task: vbr1_l1_precision_rectifier:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Precision rectifier
- Domain: `voltage`
- Target artifact(s): `precision_rectifier.va`, `tb_precision_rectifier_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `precision_rectifier.va`, `tb_precision_rectifier_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `precision_rectifier.va` declares module `precision_rectifier` with positional ports: `vin`, `vout`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=120n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `vin`
- `vout`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vin`

## Public Behavior Checks

- `negative_input_rectifies_to_zero`
- `positive_input_follows_input`
- `near_zero_has_no_large_offset`

## Output Contract

Return exactly these source artifacts:

- `precision_rectifier.va`
- `tb_precision_rectifier_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_precision_rectifier_e2e

Write both the Verilog-A DUT and Spectre testbench for a ideal precision rectifier.

The DUT module is `precision_rectifier` with ports `vin, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Drive `vout` to `vin` when `vin` is positive and to 0 V when `vin` is negative.
- Use only voltage-domain contributions and smooth the output with `transition()`.

Required testbench behavior:
- Apply negative, near-zero, and positive input intervals.
- Save `vin` and `vout` for rectification checks.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `precision_rectifier.va` and `tb_precision_rectifier_ref.scs`.
