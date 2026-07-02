# Clocked SAR Comparator

Implement `clocked_sar_comparator.va` in Verilog-A.

## Public Interface

Declare module `clocked_sar_comparator(CMPCK, VINN, VINP, DCMPN, DCMPP)` with
scalar electrical voltage-domain ports. `CMPCK` is the comparator clock,
`VINP` and `VINN` are differential analog inputs, and `DCMPP`/`DCMPN` are
voltage-coded decision outputs.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vdd = 0.9 V`: logic high level and clock threshold reference.
- `td_cmp = 20p`: comparator output delay.
- `tr = 5p`: output transition smoothing time.

## Functional Contract

- Initialize both decision outputs high.
- Whenever `CMPCK` falls through `vdd/2`, precharge/reset both decision outputs
  high.
- Whenever `CMPCK` rises through `vdd/2`, latch a differential decision:
  `DCMPP` goes high when `VINP > VINN`, `DCMPN` goes high when `VINP < VINN`,
  and both outputs go low for an equal-input decision.
- Hold the latched or precharged state until the next clock event.
- Drive outputs as smooth voltage-domain levels using the configured delay and
  transition time.

## Modeling Constraints

Return only `clocked_sar_comparator.va`. Do not emit a Spectre testbench,
checker logic, private test hooks, or simulator-private side channels. Use
voltage contributions only; do not use current contributions, `ddt()`, or
`idt()`.
