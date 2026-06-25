# Source Weighted Decoder 6bit

Implement a six-input weighted decoder. Inputs vd1..vd6 have weights 32,16,8,4,2,1 and VOUT equals VREF times the weighted sum divided by 32.

The module name and port list must match `weighted_decoder_6bit.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `lis/DEC_6bit.va`.
