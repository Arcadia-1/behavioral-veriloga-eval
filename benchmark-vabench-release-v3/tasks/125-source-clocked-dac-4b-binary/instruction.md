Implement a clocked 4-bit binary-weighted DAC.

The module must be named `clocked_dac_4b_binary` and use this port order:

`D1, D2, D3, D4, CLK, VOUT`

On each rising crossing of `CLK`, latch `D1` as the MSB and `D4` as the LSB.
Drive a mid-rise bipolar output `(code + 0.5) * lsb - 0.9`, where
`lsb = 1.8 / 16`.
