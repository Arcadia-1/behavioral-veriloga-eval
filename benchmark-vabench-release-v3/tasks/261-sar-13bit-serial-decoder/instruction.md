# Source SAR 13bit Serial Decoder

Implement a 13-bit serial SAR decoder. CLKS rising publishes the previous accumulated result and resets the accumulator; READY rising consumes DIN into the current bit weight and counts high decisions.

The module name and port list must match `sar_13bit_serial_decoder.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `zhangm/SAR_13bit_decoder.va`.
