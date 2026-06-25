Implement a start-gated voltage-domain comparator offset search helper.

The module must be named `start_gated_offset_search` and use this port order:

`CLK, VOUT, START, VINP, VINN`

Before `START` is high, hold both outputs at `vcm` and reset the search state.
After a rising `START`, update on falling `CLK` crossings. Use the source
algorithm: interpret high `VOUT` as a positive decision, halve the step on sign
changes, and drive `VINP`/`VINN` symmetrically around `vcm`.
