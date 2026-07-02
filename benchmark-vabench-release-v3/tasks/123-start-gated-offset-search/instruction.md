# Start Gated Offset Search

Implement a standalone start-gated comparator-offset calibration search driver
for a converter calibration loop.

## Public Interface

Declare module `start_gated_offset_search` with positional ports `CLK, VOUT,
START, VINP, VINN`. All ports are electrical. `VINP` and `VINN` are the
differential calibration stimulus outputs.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vdd = 0.9 V`: logic high and decision reference scale.
- `vcm = 0.7 V`: common-mode voltage for `VINP` and `VINN`.
- `vstart_th = 0.45 V`: decision threshold for `START`.

## Functional Contract

Before `START` is asserted, hold both outputs at `vcm` and reset the internal
search state. After a rising `START`, update the search on falling `CLK`
crossings. Interpret `VOUT` as the comparator decision, reverse search
direction when the decision sign changes, and halve the search step on those
sign changes. Drive `VINP` and `VINN` symmetrically around `vcm` so their
difference equals the accumulated differential search value. When `START`
falls, return to the reset common-mode state.

## Modeling Constraints

Return only `start_gated_offset_search.va`. Use deterministic voltage-domain
Verilog-A. Do not modify or emit the provided testbench, add checker logic,
hard-code private waveform sample points, add simulator-private side channels,
use current contributions, `ddt()`, or `idt()`.
