# Source Single Shot Pulse

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Timing Primitive
- Base function: source-derived `source_single_shot`
- Domain: `voltage`
- Target artifact(s): `source_single_shot.va`
- Source provenance: `wangx/single_shot.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

## Public Verilog-A Interface

`source_single_shot.va` declares module `source_single_shot` with positional ports:

```text
vin, vout
```

## Public Testbench And Observable Contract

Public transient setting used by the evaluator:

```spectre
tran tran stop=45n maxstep=50p
```

The evaluator samples stable windows after event edges and checks the intended source-derived behavior. It does not require pointwise equality at simulator timesteps.

## Public Behavior Checks

- one_output_pulse_per_input_rising_edge
- pulse_width_matches_10ns_with_delay

## Output Contract

Return exactly one source artifact named `source_single_shot.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Description

Implement the source-derived voltage-domain behavior represented by `source_single_shot`. This benchmark case is included because it captures a reusable mixed-signal behavioral primitive from the deduplicated historical Verilog-A corpus while remaining small enough for deterministic EVAS/Spectre parity evaluation.
