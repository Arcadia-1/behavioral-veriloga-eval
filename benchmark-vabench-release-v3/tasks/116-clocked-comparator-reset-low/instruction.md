# Source Clocked Comparator Reset Low

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Data Converter
- Base function: source-derived `clocked_comparator_reset_low`
- Domain: `voltage`
- Target artifact(s): `clocked_comparator_reset_low.va`
- Source provenance: `caiyizeng25/comp_ideal.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

## Public Verilog-A Interface

`clocked_comparator_reset_low.va` declares module `clocked_comparator_reset_low` with positional ports:

```text
CMPCK, VINN, VINP, DCMPN, DCMPP
```

## Public Testbench And Observable Contract

The public and hidden smoke testbench uses the transient statement shown in `test_hidden/tests/tb_source_ref.scs`.
The evaluator samples stable windows after event edges and checks source-derived behavior. It does not require pointwise equality at simulator timesteps.

## Public Behavior Checks

- reset_low_when_clock_falls
- positive_and_negative_decisions_after_rising_edges

## Output Contract

Return exactly one source artifact named `clocked_comparator_reset_low.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Description

Implement the source-derived voltage-domain behavior represented by `clocked_comparator_reset_low`. This benchmark case is included because it captures a reusable primitive from the deduplicated historical Verilog-A corpus while remaining small enough for deterministic EVAS/Spectre parity evaluation.
