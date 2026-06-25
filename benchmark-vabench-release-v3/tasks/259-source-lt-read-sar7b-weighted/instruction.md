# Source LT Read SAR7B Weighted

Implement a continuous 8-input SAR readout using the source model weights D7..D0 = 1, 1/2, ..., 1/128 times vref, offset by -vref.

The module name and port list must match `lt_read_sar7b_weighted.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `gaoya/LT_READ_SAR7B.va`.
