# Source Vargain Diffamp Clip

Implement a voltage-controlled differential gain block with output clipping. The output is 3*(CTRL_P-CTRL_N)*((INP-INN)-0.05) limited to +/-1 V.

The module name and port list must match `vargain_diffamp_clip.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `wangx/vargain_diffamp.va`.
