# Source Coarse QTZ 3bit Residue

Implement a clipped 3-bit coarse quantizer over -VREF..+VREF. Drive binary code bits and the analog residue VIN - Vquantized.

The module name and port list must match `coarse_qtz_3bit_residue.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `liukezhuo/coarse_QTZ3bit.va`.
