# SPI Shift Mux

Implement a voltage-domain serial configuration shift register for a mux-control word.

## Public Interface

Declare module `spi_shift_mux` with positional ports:

```verilog
module spi_shift_mux(scki, sdi, rst, out0, out1, out2, out3,
                     out4, out5, out6, out7, sdo, scko);
```

All ports are scalar `electrical` voltage-domain ports.

## Functional Contract

- Treat `scki`, `sdi`, and `rst` as 0/0.9 V logic with a 0.45 V threshold.
- Initialize the 8-bit configuration word to `10110010`, where the leftmost bit is exposed on `out7` and `sdo`, and the rightmost bit is exposed on `out0`.
- `rst` is active high. While `rst` is high, reload the configuration word to `10110010` and do not shift in serial data.
- On each `scki` threshold crossing after reset is inactive, shift the word toward `out7`: previous `out0` moves to `out1`, previous `out6` moves to `out7`, and sampled `sdi` enters `out0`.
- Drive `sdo` from the current `out7` bit.
- Forward `scki` to `scko` as a voltage-coded clock output.
- Drive all digital outputs near 0.9 V for logic high and near 0 V for logic low, using smooth Verilog-A transitions.

## Output

Return exactly one source artifact named `spi_shift_mux.va`. Do not generate a Spectre testbench.
