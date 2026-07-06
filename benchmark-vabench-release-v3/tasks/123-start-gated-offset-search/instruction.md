# Start Gated Offset Search

## Task Contract

Implement the requested Verilog-A artifact for `Start Gated Offset Search`.
- Form: `dut`
- Level: `L1`
- Category: `data_converter`
- Target artifact(s): `start_gated_offset_search.va`

Implement a standalone start-gated comparator-offset calibration search driver
for a converter calibration loop.

## Public Verilog-A Interface

Declare module `start_gated_offset_search` with positional ports `CLK, VOUT,
START, VINP, VINN`. All ports are electrical. `VINP` and `VINN` are the
differential calibration stimulus outputs.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vdd = 0.9 V`: logic high and decision reference scale.
- `vcm = 0.7 V`: common-mode voltage for `VINP` and `VINN`.
- `vstart_th = 0.45 V`: decision threshold for `START`.

## Required Behavior

Before `START` is asserted, hold both outputs at `vcm` and reset the internal
search state. After a rising `START`, update the search on falling `CLK`
crossings. Interpret `VOUT` as the comparator decision, reverse search
direction when the decision sign changes, and halve the search step on those
sign changes. Drive `VINP` and `VINN` symmetrically around `vcm` so their
difference equals the accumulated differential search value. When `START`
falls, return to the reset common-mode state.

## Modeling Constraints

Return only `start_gated_offset_search.va`. Use deterministic voltage-domain
Verilog-A. Do not modify or emit the provided testbench, add validation logic,
hard-code specific waveform sample points, add simulator-specific side channels,
use current contributions, `ddt()`, or `idt()`.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `start_gated_offset_search.va`. Do not include explanatory prose outside the source artifact contents.
