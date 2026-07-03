# Offset RDAC Search Flow

Implement a voltage-domain RDAC calibration and offset-search flow.

## Public Interface

Return exactly one Verilog-A source file named `offset_rdac_search_flow.va`.
Declare module `offset_rdac_search_flow` with positional ports `ck, d, vinp,
vinn, vrefp, vrefn, dc0, dc1, dc2, dc3, dc4, dc5, dc6`. All ports are
electrical.

`ck` is the calibration/search clock, `d` is the comparator decision input,
`vinp/vinn` are the generated differential input stimulus, `vrefp/vrefn` are
the generated differential reference stimulus, and `dc0..dc6` are voltage-coded
RDAC control bits.

## Functional Contract

Implement a two-phase foreground flow. First refine the 7-bit RDAC code from
MSB toward LSB using comparator decisions, starting with the MSB trial bit set.
Then run a bounded comparator-directed offset search around the current
reference. The search should maintain a signed differential input residue,
halve its step when the comparator decision changes sign, and advance the
reference by one step after the search window. Use a 0.6 V common-mode level,
a 17-level reference sweep over a 1.0 V differential span, and a 40 mV initial
offset-search step. After each reference step, reset the differential input to
the new reference and restart the RDAC refinement phase.

## Modeling Constraints

Use voltage contributions only. Use event-updated behavioral state on clock
crossings and smooth discrete or event-updated output voltages with
`transition(...)`. Do not modify or emit the support testbench, add checker
logic, hard-code private waveform sample points, add simulator-private side
channels, use current contributions, transistor-level devices, `ddt()`, `idt()`,
or AC/noise-analysis behavior.
