# Source LT Read SAR6B Weighted

Implement a continuous 6-bit SAR readout with source weights. D5..D1 contribute 1, 1/2, 1/4, 1/8, and 1/16 of vref; D0 is present but ignored, matching the source model.

The module name and port list must match `lt_read_sar6b_weighted.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `gaoya/LT_READ_SAR6B.va`.
