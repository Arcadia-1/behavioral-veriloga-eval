# Source LT Readout SAR4

Implement a continuous 4-bit SAR readout DAC. DIN0 is the LSB, DIN3 is the MSB, and VOUT equals the unsigned code times 1.8/16.

The module name and port list must match `lt_readout_sar4.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `gaoya/LT_READOUT_SAR4_NEW.va`.
