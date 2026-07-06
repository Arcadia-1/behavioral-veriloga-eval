# Offset RDAC Search Flow

## Task Contract

- Form: `dut`.
- Level: `L2`.
- Category: calibration/trim control flow.
- Target artifact: `offset_rdac_search_flow.va`.
- Role: combined RDAC refinement and comparator-offset search flow.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

Declare the public module exactly as:

```verilog
module offset_rdac_search_flow(ck, d, vinp, vinn, vrefp, vrefn, dc0, dc1, dc2, dc3, dc4, dc5, dc6);
```

`ck` is the flow clock, `d` is the comparator decision, `vinp/vinn` are generated differential input stimulus outputs, `vrefp/vrefn` are generated reference stimulus outputs, and `dc0..dc6` expose the RDAC code. All ports are electrical.

## Public Parameter Contract

No overrideable public parameters are required. Use 0/1 V logic, a 0.5 V decision threshold, a 0.6 V output common mode, 17 reference levels over a 1.0 V differential span, and a 40 mV initial offset-search step.

## Required Behavior

Implement a two-phase foreground flow. First refine the 7-bit RDAC code from MSB toward LSB using comparator decisions, starting from the MSB trial. Then run a bounded comparator-directed offset search around the current reference; maintain a signed differential input residue, halve the search step when the comparator decision changes sign, and advance the reference after the search window. After each reference step, reset the differential input to the new reference and restart the RDAC refinement phase.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `offset_rdac_search_flow.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
