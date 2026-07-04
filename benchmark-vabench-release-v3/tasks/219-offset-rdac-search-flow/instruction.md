# Offset RDAC Search Flow

## Task Contract

- Form: `dut`
- Level: `L2`
- Category: Calibration, Trim, and DEM Control
- Base function: RDAC calibration and comparator-offset search flow
- Domain: `voltage`
- Target artifact(s): `offset_rdac_search_flow.va`
- Output boundary: implement only the requested DUT artifact; validation harnesses and simulator-private hooks are external to the requested output.

## Form-Specific Requirements

- Return exactly one Verilog-A source file named `offset_rdac_search_flow.va`.
- Preserve the public module name, positional port order, electrical disciplines, generated stimulus outputs, and RDAC bit order.
- Do not generate or modify a Spectre testbench.

## Public Verilog-A Interface

Declare module `offset_rdac_search_flow` with positional ports:

```verilog
module offset_rdac_search_flow(ck, d,
    vinp, vinn, vrefp, vrefn,
    dc0, dc1, dc2, dc3, dc4, dc5, dc6);
```

All ports are electrical. `ck` is the calibration/search clock, `d` is the
comparator decision input, `vinp/vinn` are the generated differential input
stimulus, `vrefp/vrefn` are the generated differential reference stimulus, and
`dc0..dc6` are voltage-coded RDAC control bits.

## Public Parameter Contract

No overrideable public parameters are required. Use the operating constants in
the required behavior: 0/1 V logic convention, mid-rail decision threshold,
0.6 V common-mode level, 17 reference levels across a 1.0 V differential span,
and a 40 mV initial offset-search step.

## Required Behavior

Implement a two-phase foreground flow. First refine the 7-bit RDAC code from
MSB toward LSB using comparator decisions, starting with the MSB trial bit set.
Then run a bounded comparator-directed offset search around the current
reference. The search should maintain a signed differential input residue,
halve its step when the comparator decision changes sign, and advance the
reference by one step after the search window. After each reference step, reset
the differential input to the new reference and restart the RDAC refinement
phase.

## Modeling Constraints

Use voltage contributions only. Use event-updated behavioral state on clock
crossings and smooth discrete or event-updated output voltages with
`transition(...)`. Do not add checker logic, hard-code private waveform sample
points, add simulator-private side channels, use current contributions,
transistor-level devices, `ddt()`, `idt()`, or AC/noise-analysis behavior.

## Output Contract

Return exactly one complete Verilog-A file named `offset_rdac_search_flow.va`.
Do not include explanatory prose outside the source artifact contents.
