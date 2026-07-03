# Comparator Offset Driver

Implement a clocked binary-search stimulus driver for comparator offset
calibration.

## Public Interface

Declare module `comparator_offset_binary_driver` with positional ports `clk,
dcmpp, vinp, vinn`. All ports are electrical. `clk` is the update clock,
`dcmpp` is the comparator decision input, and `vinp`/`vinn` are the generated
differential stimulus outputs.

## Public Parameter Contract

Provide this overrideable public parameter:

- `vdd = 0.9 V`: logic high level, decision threshold reference, and default
  common-mode reference for the generated differential stimulus.

## Functional Contract

- Initialize the differential search value to zero and the differential search
  step to `100m V`.
- On each falling crossing of `clk` through `vdd/2`, sample `dcmpp` against
  `vdd/2`.
- If the sampled decision is high, decrease the signed differential search
  value; if the sampled decision is low, increase it.
- Halve the search step after each update.
- Drive `vinp` and `vinn` symmetrically around `vdd/2` so their difference is
  the current signed search value.
- Hold the generated stimulus between update events.

## Modeling Constraints

Return only `comparator_offset_binary_driver.va`. Use voltage contributions
only. Do not modify or emit the support testbench, add checker logic, hard-code
waveform sample points, add simulator-private side channels, use current
contributions, `ddt()`, or `idt()`. Update search state in analog event blocks
and drive voltage outputs outside those event blocks.
