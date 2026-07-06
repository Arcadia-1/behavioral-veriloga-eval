# Two Input AND Gate

## Task Contract

Implement the requested Verilog-A artifact for `Two Input AND Gate`.
- Form: `dut`
- Level: `L1`
- Category: `mixed_signal`
- Target artifact(s): `two_input_and_gate.va`

The module must be named `two_input_and_gate` and use this port order:

`out, in1, in2`

Interpret each input as logic high when it exceeds `vth`. Drive `out` to `vh`
only when both inputs are high; otherwise drive `vl`. Use `transition()` with
the configurable delay and transition time.

## Public Verilog-A Interface

The file `two_input_and_gate.va` must define `module two_input_and_gate(out, in1, in2);`. All ports are electrical. `in1` and `in2` are voltage-coded inputs, and `out` is the voltage-coded gate output.

## Public Parameter Contract

The public parameters declared by `two_input_and_gate.va` are part of the contract and may be overridden by validation harnesses:

- `parameter real vh = 0.9;`
- `parameter real vl = 0;`
- `parameter real vth = 0.45;`
- `parameter real td = 0 from [0:inf);`
- `parameter real tt = 0 from [0:inf);`

## Required Behavior

Implement a voltage-domain two-input AND gate. Interpret each input as high when it exceeds `vth`. Drive `out` to `vh` only when both `in1` and `in2` are high; otherwise drive `out` to `vl`. Apply the configured transition delay and transition time to the voltage output.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `two_input_and_gate.va`. Do not include explanatory prose outside the source artifact contents.
