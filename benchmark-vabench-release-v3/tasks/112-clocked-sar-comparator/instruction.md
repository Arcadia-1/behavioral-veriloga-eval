# Source Clocked SAR Comparator

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Data Converter
- Base function: source-derived `clocked_sar_comparator`
- Domain: `voltage`
- Target artifact(s): `clocked_sar_comparator.va`
- Source provenance: `caiyizeng25/L3_SAR_comparator_ideal.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

## Public Verilog-A Interface

`clocked_sar_comparator.va` declares module `clocked_sar_comparator` with positional ports:

```text
CMPCK, VINN, VINP, DCMPN, DCMPP
```

## Public Testbench And Observable Contract

Public transient setting used by the evaluator:

```spectre
tran tran stop=55n maxstep=50p
```

The evaluator samples stable windows after event edges and checks the intended source-derived behavior. It does not require pointwise equality at simulator timesteps.

## Public Behavior Checks

- reset_both_high_when_clock_low
- positive_and_negative_decisions_after_rising_edges

## Output Contract

Return exactly one source artifact named `clocked_sar_comparator.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Description

Implement the source-derived voltage-domain behavior represented by `clocked_sar_comparator`. This benchmark case is included because it captures a reusable mixed-signal behavioral primitive from the deduplicated historical Verilog-A corpus while remaining small enough for deterministic EVAS/Spectre parity evaluation.
