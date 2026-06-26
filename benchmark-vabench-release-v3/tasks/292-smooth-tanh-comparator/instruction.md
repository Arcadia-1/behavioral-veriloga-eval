# Source Smooth Tanh Comparator

Implement a smooth comparator macro. OUT follows tanh(4*(IN-REF-0.05)) and ranges from -1 V to +1 V.

The module name and port list must match `smooth_tanh_comparator.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `wangx/comparator.va`.
