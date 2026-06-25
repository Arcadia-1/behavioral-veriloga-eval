# Source Sample Hold 5v Clock

Implement an ideal sample-and-hold. When the 5 V clock crosses 2.5 V rising, sample VIN and hold that value on VOUT until the next sample edge.

The module name and port list must match `sample_hold_5v_clock.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `wangx/sah_ideal.va`.
