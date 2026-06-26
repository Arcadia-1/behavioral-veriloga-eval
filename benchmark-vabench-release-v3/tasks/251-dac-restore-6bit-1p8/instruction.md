# Source DAC Restore 6bit 1p8

Implement a 1.8 V-threshold clocked 6-bit restore DAC with D1 as MSB and D6 as LSB. The output is `(code + 0.5) * 3.6 / 64 - 1.8`.

The module name and port list must match `dac_restore_6bit_1p8.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `wangxy/L1_DAC_restore_6bit.va`.
