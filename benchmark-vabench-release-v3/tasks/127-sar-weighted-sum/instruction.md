Implement a voltage-domain SAR weighted-sum source.

The module must be named `sar_weighted_sum` and use this port order:

`D10, D9, D8, D7, D6, D5, D4, D3, D2, D1, D0, VOUT`

Each input is interpreted as logic high when its voltage exceeds `vth`. Drive a
continuous analog output equal to the weighted sum

`(448*D10 + 256*D9 + 128*D8 + 80*D7 + 48*D6 + 32*D5 + 16*D4 + 8*D3 + 4*D2 + 2*D1 + D0) / 512 - 1`.
