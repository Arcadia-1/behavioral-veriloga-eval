# Task: vbr1_l1_edge_detector:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Digital and Event-Driven Logic
- Base function: Edge detector
- Domain: `voltage`
- Target artifact(s): `edge_detector.va`
- Supplied/reference support artifact(s): `tb_edge_detector_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `edge_detector.va` declares module `edge_detector` with positional ports: `sig`, `rst_n`, `pulse`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=180n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `sig`
- `rst_n`
- `pulse`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `pulse_high_at_safe_windows_after_rising_sig_edges`
- `pulse_low_before_next_falling_edge_windows`
- `reset_keeps_pulse_low_before_release`

## Output Contract

Return exactly one source artifact named `edge_detector.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_edge_detector_dut

Write a pure voltage-domain Verilog-A module named `edge_detector`.

The module has electrical ports `sig`, `rst_n`, and `pulse`. `rst_n` is active
low. After reset is released, each rising crossing of `sig` should generate a
short high pulse on `pulse`; falling crossings must not generate a pulse. Drive
outputs with `transition` and use voltage contributions only.

Return exactly one complete Verilog-A file named `edge_detector.va`.
