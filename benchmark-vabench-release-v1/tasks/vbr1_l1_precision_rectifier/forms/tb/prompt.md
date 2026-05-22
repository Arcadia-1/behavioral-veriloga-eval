# Task: vbr1_l1_precision_rectifier:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Analog Behavioral Signal Conditioning
- Base function: Precision rectifier
- Domain: `voltage`
- Target artifact(s): `tb_precision_rectifier_ref.scs`
- Supplied/reference support artifact(s): `precision_rectifier.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

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

Return exactly one source artifact named `tb_precision_rectifier_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_precision_rectifier_tb

Write a Spectre testbench for a ideal precision rectifier DUT.

The DUT module is `precision_rectifier` with ports `vin, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `precision_rectifier.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Drive `vout` to `vin` when `vin` is positive and to 0 V when `vin` is negative.
- Use only voltage-domain contributions and smooth the output with `transition()`.

Stimulus and observability requirements:
- Apply negative, near-zero, and positive input intervals.
- Save `vin` and `vout` for rectification checks.

Return exactly one Spectre testbench file named `tb_precision_rectifier_ref.scs`.
