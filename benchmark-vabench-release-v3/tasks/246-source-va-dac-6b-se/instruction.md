# Source VA DAC 6b SE

Implement a ready-triggered single-ended 6-bit weighted DAC. On each RDY rising edge, decode DIN5..DIN0 with weights 16, 8, 4, 2, 1, 0.5 and map the weighted sum to a bipolar output using the source model normalization.

The module name and port list must match `va_dac_6b_se.va`. Keep the model voltage-domain only and deterministic. The historical source normalized for this task is `zhangym/_va_6b_dac.va`.
