# SAR Comparator Reset High

Implement a SAR-style clocked differential comparator with precharged-high
decision outputs.

## Public Interface

Declare module `sar_comparator_reset_high` with positional ports `cmpck, vinn,
vinp, dcmpn, dcmpp`. All ports are electrical. `cmpck` is the comparator clock,
`vinp` and `vinn` are the differential analog inputs, and `dcmpp`/`dcmpn` are
voltage-coded decision outputs.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vdd = 0.9 V`: logic high level and clock threshold reference.
- `td_cmp = 20p`: output decision delay.

## Functional Contract

- Initialize both decision outputs high.
- Whenever `cmpck` falls through `vdd/2`, reset both outputs high.
- Whenever `cmpck` rises through `vdd/2`, latch a differential decision:
  `dcmpp` high for `vinp > vinn`, `dcmpn` high for `vinp < vinn`, and both
  outputs low for an equal-input decision.
- Hold the latched or reset state until the next clock event.
- Drive outputs as smoothed voltage-domain levels from 0 V to `vdd`.

## Modeling Constraints

Return only `sar_comparator_reset_high.va`. Use voltage contributions only. Do
not modify or emit the support testbench, add checker logic, hard-code waveform
sample points, add simulator-private side channels, use current contributions,
`ddt()`, or `idt()`. Update local decision state in analog event blocks and
drive smoothed output contributions outside those event blocks.
