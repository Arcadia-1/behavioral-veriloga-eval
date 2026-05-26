# Task: vbr1_l1_precision_rectifier:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Precision rectifier
- Domain: `voltage`
- Target artifact(s): `precision_rectifier.va`
- Supplied/reference support artifact(s): `tb_precision_rectifier_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

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

## Public Behavior Checks

- `negative_input_rectifies_to_zero`
- `positive_input_follows_input`
- `near_zero_has_no_large_offset`

## Output Contract

Return exactly one source artifact named `precision_rectifier.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_precision_rectifier_dut

Write a pure voltage-domain Verilog-A module for a ideal precision rectifier.

The DUT module is `precision_rectifier` with ports `vin, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Drive `vout` to `vin` when `vin` is positive and to 0 V when `vin` is negative.
- Use only voltage-domain contributions and smooth the output with `transition()`.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `precision_rectifier.va`.
