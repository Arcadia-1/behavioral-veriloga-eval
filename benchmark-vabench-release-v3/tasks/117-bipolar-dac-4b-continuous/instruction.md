# Source Bipolar DAC 4b Continuous

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Data Converter
- Base function: source-derived `bipolar_dac_4b_continuous`
- Domain: `voltage`
- Target artifact(s): `bipolar_dac_4b_continuous.va`
- Source provenance: `shigao/DAC4bit_1.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

## Public Verilog-A Interface

`bipolar_dac_4b_continuous.va` declares module `bipolar_dac_4b_continuous` with positional ports:

```text
vd3, vd2, vd1, vd0, vout
```

## Public Testbench And Observable Contract

The public and hidden smoke testbench uses the transient statement shown in `test_hidden/tests/tb_source_ref.scs`.
The evaluator samples stable windows after event edges and checks source-derived behavior. It does not require pointwise equality at simulator timesteps.

## Public Behavior Checks

- continuous_code_to_bipolar_level
- monotonic_output_across_codes

## Output Contract

Return exactly one source artifact named `bipolar_dac_4b_continuous.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Description

Implement the source-derived voltage-domain behavior represented by `bipolar_dac_4b_continuous`. This benchmark case is included because it captures a reusable primitive from the deduplicated historical Verilog-A corpus while remaining small enough for deterministic EVAS/Spectre parity evaluation.
