# Source Crossing Pulse Detector

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Timing Primitive
- Base function: source-derived `source_crossing_pulse_detector`
- Domain: `voltage`
- Target artifact(s): `source_crossing_pulse_detector.va`
- Source provenance: `zhangm/crossing_detector.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

## Public Verilog-A Interface

`source_crossing_pulse_detector.va` declares module `source_crossing_pulse_detector` with positional ports:

```text
sigin, sigout
```

## Public Testbench And Observable Contract

The public and hidden smoke testbench uses the transient statement shown in `test_hidden/tests/tb_source_ref.scs`.
The evaluator samples stable windows after event edges and checks source-derived behavior. It does not require pointwise equality at simulator timesteps.

## Public Behavior Checks

- pulse_after_each_input_crossing
- output_returns_low_after_fixed_width

## Output Contract

Return exactly one source artifact named `source_crossing_pulse_detector.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Description

Implement the source-derived voltage-domain behavior represented by `source_crossing_pulse_detector`. This benchmark case is included because it captures a reusable primitive from the deduplicated historical Verilog-A corpus while remaining small enough for deterministic EVAS/Spectre parity evaluation.
