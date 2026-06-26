Implement a comparator offset-detect search source.

The module must be named `comp_os_detect` and use this port order:

`CLK, DCMPP, VINP, VINN`

On each falling crossing of `CLK`, read `DCMPP`. A high decision subtracts the
current step from the internal differential value, and a low decision adds it.
The step halves after every decision. Drive `VINP` and `VINN` around half `vdd`
with the accumulated differential value.
