# Source Trim Ctrl 5bit

Implement a scalar-to-5-bit trim control encoder. Round AIN to an integer code and drive DOUT0..DOUT4 as voltage-coded binary bits.

The module name and port list must match `trim_ctrl_5bit.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `guoxy/ideal_TRIM_CTRL_5BITS.va`.
