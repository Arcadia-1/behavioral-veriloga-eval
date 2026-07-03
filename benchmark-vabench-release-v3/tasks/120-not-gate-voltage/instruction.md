# Source Not Gate Voltage

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Logic
- Base function: source-derived `source_not_gate`
- Domain: `voltage`
- Target artifact(s): `source_not_gate.va`
- Source provenance: `wangx/not_gate.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Output boundary: implement only the requested DUT artifact; validation harnesses and simulator-private hooks are external to the requested output.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

## Public Verilog-A Interface

`source_not_gate.va` declares module `source_not_gate` with positional ports:

```text
vin, vout
```

## Public Testbench And Observable Contract

The public testbench provides a voltage-coded input stimulus and saves `vin` and
`vout`. The observable contract samples stable windows after event edges and
checks source-derived behavior; it does not require pointwise equality at
simulator timesteps.

## Public Behavior Checks

- inverts_voltage_logic
- stable_after_propagation_delay

## Output Contract

Return exactly one source artifact named `source_not_gate.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Description

Implement the source-derived voltage-domain behavior represented by `source_not_gate`. This benchmark case is included because it captures a reusable primitive from the deduplicated historical Verilog-A corpus while remaining small enough for deterministic EVAS/Spectre parity evaluation.
