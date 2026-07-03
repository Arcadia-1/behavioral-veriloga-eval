# Offset Halving Search

Implement a voltage-domain comparator-driven offset-search primitive.

## Public Interface

Return exactly one Verilog-A source file named `offset_halving_search.va`.
Declare module `offset_halving_search` with positional ports `clk, dcmpp, vinp,
vinn`. All ports are electrical.

`clk` is the search update clock, `dcmpp` is the comparator decision input, and
`vinp/vinn` are the generated differential stimulus outputs.

## Public Parameter Contract

Provide overrideable parameter `vdd = 0.9 V`. Treat comparator decisions with
threshold `0.5*vdd`.

## Functional Contract

Initialize the differential residue to zero and the search step to `0.1 V`.
On each falling crossing of `clk`, sample `dcmpp`, update the signed search
residue in the direction opposite the comparator decision, and halve the step
for the next update. Drive `vinp` and `vinn` symmetrically around `0.5*vdd`
from the current residue.

## Modeling Constraints

Use voltage contributions only. Use event-updated behavioral state on clock
crossings and smooth event-updated output voltages with `transition(...)`. Do
not modify or emit the support testbench, add checker logic, hard-code private
waveform sample points, add simulator-private side channels, use current
contributions, transistor-level devices, `ddt()`, `idt()`, or AC/noise-analysis
behavior.
