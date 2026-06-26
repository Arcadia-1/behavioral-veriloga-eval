# Source Comparator Reset Low 1p8

Implement a 1.8 V clocked comparator. On CMPCK rising, compare VINP/VINN; on CMPCK falling, reset both outputs low.

The module name and port list must match `comparator_reset_low_1p8.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `zhangfm/comparator_ideal.va`.
