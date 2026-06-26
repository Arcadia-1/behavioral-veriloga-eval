Implement a supply-referenced latched comparator.

The module must be named `latched_comparator_delay` and use this port order:

`DOUT, GND, VDD, CLK, VINN, VINP`

At initial step, derive output low, high, and clock threshold from `GND` and
`VDD`. On each rising clock crossing, latch whether `VINP - VINN` exceeds the
offset/noise term. Drive `DOUT` to the supply rails with the configured delay
and transition time.
