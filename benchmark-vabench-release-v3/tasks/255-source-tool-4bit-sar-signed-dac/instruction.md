# Source Tool 4bit SAR Signed DAC

Implement a sample-triggered signed 4-bit SAR helper DAC. On SH rising, each bit contributes +weight if high and -weight if low, with weights 8, 4, 2, 1 and gain 1.8/16.

The module name and port list must match `tool_4bit_sar_signed_dac.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `liaoyuhui/_tool_4bit_sar.va`.
