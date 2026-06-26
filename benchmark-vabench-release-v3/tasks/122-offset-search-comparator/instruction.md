Implement a voltage-domain comparator offset search helper.

The module must be named `offset_search_comparator` and use this port order:

`CLK, VOUT, VINP, VINN`

On each falling crossing of `CLK` through half `vdd`, compare `VOUT` to half
`vdd`. If `VOUT` is below threshold, move the differential output upward by the
current step; otherwise move it downward. When the sign changes relative to the
previous decision, halve the step before applying the update. Drive `VINP` and
`VINN` around common-mode `vcm` with `VINP - VINN` equal to the accumulated
differential search value.
