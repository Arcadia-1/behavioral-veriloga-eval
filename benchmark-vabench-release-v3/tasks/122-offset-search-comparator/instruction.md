# Offset Search Comparator

Implement a voltage-domain comparator-offset search helper that generates a
differential stimulus pair from comparator decisions.

## Public Interface

Declare module `offset_search_comparator` with positional ports `CLK, VOUT,
VINP, VINN`. All ports are electrical. `CLK` is the update clock, `VOUT` is the
comparator decision input, and `VINP`/`VINN` are the generated differential
stimulus outputs.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vdd = 0.9 V`: logic high level and clock/decision threshold reference.
- `vcm = 0.45 V`: common-mode center for the generated differential stimulus.

## Functional Contract

- Initialize the signed differential search value to zero and start with a
  `10m V` differential search step.
- On each falling crossing of `CLK` through `vdd/2`, sample `VOUT` against
  `vdd/2`.
- If the sampled decision is below threshold, increase `VINP - VINN`; otherwise
  decrease `VINP - VINN`.
- Halve the search step only when the sampled decision polarity changes from
  the previous update.
- Drive `VINP` and `VINN` symmetrically around `vcm` so their difference is the
  accumulated signed search value.
- Hold the generated stimulus between update events.

## Modeling Constraints

Return only `offset_search_comparator.va`. Use voltage contributions only. Do
not modify or emit the support testbench, add checker logic, hard-code waveform
sample points, add simulator-private side channels, use current contributions,
`ddt()`, or `idt()`. Update search state in analog event blocks and drive
voltage outputs outside those event blocks.
