# Source Clocked Comparator Dual Output

Implement a clocked comparator with complementary outputs. On each rising clock edge, latch VINP > VINN into OUTP/OUTN; on each falling clock edge, reset both outputs low after the comparator delay.

The module name and port list must match `clocked_comparator_dual_output.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `caiyizeng25/comp_ideal.va`.
