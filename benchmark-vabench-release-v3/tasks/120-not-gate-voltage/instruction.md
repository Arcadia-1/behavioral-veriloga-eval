# Source Not Gate Voltage

## Task Contract

Implement the requested Verilog-A artifact for `Not Gate Voltage`.
- Form: `dut`
- Level: `L1`
- Category: `logic`
- Target artifact(s): `source_not_gate.va`

- Base function: source-derived `source_not_gate`
- Domain: `voltage`
- Source provenance: `wangx/not_gate.va`

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

## Public Verilog-A Interface

`source_not_gate.va` declares module `source_not_gate` with positional ports:

```text
vin, vout
```

## Public Parameter Contract

The public parameters declared by `source_not_gate.va` are part of the contract and may be overridden by validation harnesses:

- `parameter real vlogic_high = 0.9;`
- `parameter real vlogic_low = 0.0;`
- `parameter real vtrans = 0.45;`
- `parameter real tdel = 500p from [0:inf);`
- `parameter real trise = 20p from (0:inf);`
- `parameter real tfall = 20p from (0:inf);`

## Required Behavior

Implement a voltage-domain inverter. Interpret `vin` as logic high when `V(vin)` is above `vtrans`; otherwise interpret it as logic low. Drive `vout` to `vlogic_low` for a high input and to `vlogic_high` for a low input. The output must respond to both rising and falling input threshold crossings and use the configured transition delay/rise/fall smoothing.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one source artifact named `source_not_gate.va`.
Do not include explanatory prose outside the source artifact contents.
