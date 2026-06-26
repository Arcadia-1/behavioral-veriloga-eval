# Source DAC Restore 7bit Clocked

Implement a clocked 7-bit restore DAC. On CLK rising, decode D6..D0 and output `(code + 0.5) * 1.8 / 128 - 0.9`.

The module name and port list must match `dac_restore_7bit_clocked.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `wangxy/DAC_restore_7bit.va`.
