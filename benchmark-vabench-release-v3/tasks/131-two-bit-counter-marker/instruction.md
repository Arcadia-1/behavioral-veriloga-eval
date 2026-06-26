Implement a two-bit counter marker.

The module must be named `two_bit_counter_marker` and use this port order:

`CLKIN, MC`

Initialize the counter and marker low. On each rising crossing of `CLKIN`
through 0.5 V, increment a modulo-four counter. Drive `MC` high only on the edge
that wraps the counter from 3 back to 0.
