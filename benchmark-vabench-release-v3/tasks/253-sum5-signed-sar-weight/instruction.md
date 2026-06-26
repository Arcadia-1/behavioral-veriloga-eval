# Source SUM5 Signed SAR Weight

Implement a 5-input signed SAR weighted summer. Each bit is interpreted as +1 above threshold and -1 below threshold, then combined with 1/2, 1/4, 1/8, 1/16, and 1/32 weights.

The module name and port list must match `sum5_signed_sar_weight.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `zhangz/DAC_serial_PPSAR_va.va`.
