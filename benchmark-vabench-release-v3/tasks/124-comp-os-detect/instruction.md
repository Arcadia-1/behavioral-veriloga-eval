# Comparator Offset Detect

Implement a comparator-offset detector that drives differential search outputs.

## Public Interface

Declare module `comp_os_detect` with positional ports `CLK, DCMPP, VINP,
VINN`. All ports are electrical. `DCMPP` is the comparator decision input and
`VINP/VINN` are the differential stimulus outputs.

## Public Parameter Contract

Provide this overrideable public parameter:

- `vdd = 0.9 V`: logic high, clock threshold scale, and output common-mode
  reference.

## Functional Contract

On each falling `CLK` crossing through half `vdd`, read `DCMPP`. A high
decision subtracts the current differential search step from the internal
offset estimate; a low decision adds the current step. Halve the step after
every decision. Drive `VINP` and `VINN` symmetrically around half `vdd` with
their difference equal to the accumulated differential search value.

## Modeling Constraints

Return only `comp_os_detect.va`. Use deterministic voltage-domain Verilog-A.
Do not modify or emit the support testbench, add checker logic, hard-code
private waveform sample points, add simulator-private side channels, use
current contributions, `ddt()`, or `idt()`.
