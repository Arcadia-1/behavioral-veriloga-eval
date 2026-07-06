# DFF Set Reset Hold

## Task Contract

- Form: `dut`.
- Level: `L1`.
- Category: AMS clock/control support.
- Target artifact: `dff_set_reset_hold.va`.
- Role: clocked DFF with active-low set/reset hold behavior.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

Declare the public module exactly as:

```verilog
module dff_set_reset_hold(ck, d, rn, sn, qp);
```

`ck` is the clock, `d` is the data input, `rn` is active-low reset, `sn` is active-low set, and `qp` is the voltage-coded output. All ports are electrical.

## Public Parameter Contract

No overrideable public parameters are required. Use a 0.45 V logic threshold, output levels 0/0.9 V, 50 ps output delay, and 20 ps transition edges.

## Required Behavior

When `rn` is low, force `qp` low. When reset is inactive and `sn` is low, force `qp` high. Otherwise, on each rising `ck` crossing, capture `d` according to the logic threshold. Hold the stored output between asynchronous set/reset and clock events.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `dff_set_reset_hold.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
