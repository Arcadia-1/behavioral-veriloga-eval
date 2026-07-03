# Clocked Comparator Reset Low

Implement a clocked differential comparator with reset-low voltage-coded
decision outputs.

## Public Interface

Declare module `clocked_comparator_reset_low` with positional ports `CMPCK,
VINN, VINP, DCMPN, DCMPP`. All ports are electrical. `CMPCK` is the comparator
clock, `VINP` and `VINN` are the differential analog inputs, and
`DCMPP`/`DCMPN` are complementary decision outputs.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vdd = 0.9 V`: logic high level and clock threshold reference.
- `td_cmp = 100p`: output decision delay.
- `tr = 10p`: output transition smoothing time.

## Functional Contract

- Initialize both decision outputs low.
- Whenever `CMPCK` falls through `vdd/2`, reset both decision outputs low.
- Whenever `CMPCK` rises through `vdd/2`, latch a differential decision:
  `DCMPP` high for `VINP > VINN`, `DCMPN` high for `VINP < VINN`, and both
  outputs remain low for an equal-input decision.
- Hold the latched or reset state until the next clock event.
- Drive outputs as smooth voltage-domain levels using the configured delay and
  transition time.

## Modeling Constraints

Return only `clocked_comparator_reset_low.va`. Use voltage contributions only.
Do not modify or emit the support testbench, add checker logic, hard-code
waveform sample points, add simulator-private side channels, use current
contributions, `ddt()`, or `idt()`. Update local decision state in analog event
blocks and drive smoothed output contributions outside those event blocks.
