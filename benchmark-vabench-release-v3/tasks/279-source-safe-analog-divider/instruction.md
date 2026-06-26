# Source Safe Analog Divider

Implement a guarded voltage divider. OUT equals NUM/DEN, except small-magnitude denominators are clamped to +/-0.2 V with the original sign.

The module name and port list must match `safe_analog_divider.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `wangx/divider.va`.
