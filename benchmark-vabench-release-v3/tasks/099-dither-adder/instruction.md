# Dither Adder

Implement `dither_adder.va` in Verilog-A.

## Interface

```verilog
module dither_adder(
    input  electrical VRES_P,
    input  electrical VRES_N,
    input  electrical DPN,
    output electrical VOUT_P,
    output electrical VOUT_N
);
```

## Required Behavior

Implement a standalone differential dither injection block. The module receives
a differential residual signal on `VRES_P/VRES_N` and a voltage-coded dither
polarity input `DPN`. When `DPN` is above the threshold, inject a positive
differential dither; when it is below the threshold, inject a negative
differential dither.

The injected differential offset is controlled by parameter `DITHER_AMP`
and must be split symmetrically between the two outputs:

```text
dither_diff = +DITHER_AMP when V(DPN) > vth
dither_diff = -DITHER_AMP when V(DPN) <= vth
VOUT_P = VRES_P + dither_diff / 2
VOUT_N = VRES_N - dither_diff / 2
```

This keeps the output common-mode equal to the input common-mode while adding
only the requested differential dither. Keep the block usable with different
`DITHER_AMP` values selected by the testbench.

Use parameter `vth` with a default near 0.45 V to interpret the voltage-coded
`DPN` polarity input, and keep the model pure behavioral Verilog-A. Do not use
transistor-level devices, AC/noise analysis, private test hooks, or
simulator-private side channels.

Only `dither_adder.va` is graded as the candidate implementation.
