# Source Limiting Diffamp

Implement a differential amplifier with hard output limits. OUT is 4*(INP-INN) clipped to +/-0.75 V.

The module name and port list must match `limiting_diffamp.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `wangx/limiting_diffamp.va`.
