# Linearity RDAC Offset Sweep

## Task Contract

- Form: `dut`.
- Level: `L2`.
- Category: calibration/linearity measurement flow.
- Target artifact: `linearity_rdac_offset_sweep.va`.
- Role: RDAC-code sweep with repeated comparator-directed offset search.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

Declare the public module exactly as:

```verilog
module linearity_rdac_offset_sweep(ck, d, vinp, vinn, vrefp, vrefn, dc0, dc1, dc2, dc3, dc4, dc5, dc6);
```

`ck` is the sweep/search clock, `d` is the comparator decision, `vinp/vinn` are generated differential input stimulus outputs, `vrefp/vrefn` are generated reference stimulus outputs, and `dc0..dc6` expose the RDAC sweep code. All ports are electrical.

## Public Parameter Contract

Provide overrideable parameters `vcm = 0.6`, `vppd = 1.0`, `vdd = 1.0`, `nlvl = 17.0`, and integer `iter_num = 4`.

## Required Behavior

For each RDAC code, run a short comparator-directed offset search around the current reference. Track the comparator sign, halve the search step when the sign changes, and move the differential input residue in the indicated direction. After `iter_num` search updates, decrement the 7-bit RDAC code and restart the search from the current reference. When the RDAC code wraps from zero back to full scale, advance the reference by one LSB of the public reference sweep.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `linearity_rdac_offset_sweep.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
