# Source DAC4bit Small Swing

Implement a continuous 4-bit small-swing DAC. Decode VD3..VD0 as an unsigned code and map it to `vref * (2*code/15 - 1)` with vref = 20 mV.

The module name and port list must match `dac4bit_small_swing.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `shigao/DAC4bit_1.va`.
