# Source DAC4bit Bipolar 252m

Implement a continuous 4-bit binary DAC. Bits d3..d0 encode 0..15 and drive vout = vref * (2*code/15 - 1) with the source model's 252 mV full-scale reference.

The module name and port list must match `dac4bit_bipolar_252m.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `chengqidong25/DAC4bit.va`.
