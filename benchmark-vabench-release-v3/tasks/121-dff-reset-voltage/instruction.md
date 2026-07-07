# Source DFF Reset Voltage

## Task Contract

Implement the requested Verilog-A artifact for `DFF Reset Voltage`.
- Form: `dut`
- Level: `L1`
- Category: `logic`
- Target artifact(s): `source_dff_reset.va`

- Base function: source-derived `source_dff_reset`
- Domain: `voltage`
- Source provenance: `hexy/dff_rst.va`

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

## Public Verilog-A Interface

`source_dff_reset.va` declares module `source_dff_reset` with positional ports:

```text
vin_d, vclk, rst, vout_q, vout_qbar
```

## Public Parameter Contract

The public parameters declared by `source_dff_reset.va` are part of the contract and may be overridden by validation harnesses:

- `parameter real vlogic_high = 0.9;`
- `parameter real vlogic_low = 0.0;`
- `parameter real vtrans_clk = 0.45;`
- `parameter real vtrans = 0.45;`
- `parameter real tdel = 500p from [0:inf);`
- `parameter real trise = 20p from (0:inf);`
- `parameter real tfall = 20p from (0:inf);`

## Required Behavior

Implement a voltage-domain D flip-flop with reset and complementary outputs. On each rising crossing of `vclk` through `vtrans_clk`, sample `vin_d` using threshold `vtrans`; drive `vout_q` high and `vout_qbar` low for a sampled high data value, and the opposite for a sampled low data value. On a rising reset crossing, force both `vout_q` and `vout_qbar` to the configured low output level through the configured transition delay/rise/fall smoothing. Keep `vout_qbar` complementary to `vout_q` during normal sampled operation after data-sampling clock events.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one source artifact named `source_dff_reset.va`.
Do not include explanatory prose outside the source artifact contents.
