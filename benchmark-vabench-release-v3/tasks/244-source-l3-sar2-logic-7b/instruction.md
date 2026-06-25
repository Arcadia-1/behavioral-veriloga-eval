# Source L3 SAR2 Logic 7b

Implement the SAR2 controller whose comparator outputs are active-low decisions. Reset on CLK falling, start CMPCK on CLK rising, update SP/SN on DP/DN falling, decrement on comparator-output recovery, and publish DO after the final bit.

The module name and port list must match `l3_sar2_logic_7b.va`. Keep the model voltage-domain only and deterministic. The historical source normalized for this task is `caiyizeng25/L3_SAR2_logic_7b_ideal.va`.
