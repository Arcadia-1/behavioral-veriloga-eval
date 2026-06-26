# Source DAC Restore 4bit Clocked

Implement a clocked 4-bit restore DAC. On CLK rising, decode D3..D0 as a binary word and output the centered bin voltage `(code + 0.5) * 1.8 / 16 - 0.9`.

The module name and port list must match `dac_restore_4bit_clocked.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `wangxy/DAC_restore_4bit.va`.
