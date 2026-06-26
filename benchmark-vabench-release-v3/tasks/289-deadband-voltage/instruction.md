# Source Deadband Voltage

Implement a deadband shaper. OUT is zero within [-0.25 V, +0.25 V], otherwise it reports the excess beyond the nearest threshold.

The module name and port list must match `deadband_voltage.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `wangx/deadband.va`.
