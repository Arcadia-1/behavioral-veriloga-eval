Implement a differential pass-through buffer.

The module must be named `differential_buffer` and use this port order:

`VINP, VINN, VOUTP, VOUTN`

Continuously copy `VINP` to `VOUTP` and `VINN` to `VOUTN` without adding gain,
offset, or delay.
