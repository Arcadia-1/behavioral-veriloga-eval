# Source L2 SAR Logic 7b

Implement a scalarized 7-bit asynchronous SAR logic controller. Reset on CLKS rising, assert CMPCK on CLKC rising, consume DCMPP/DCMPN pulses from MSB to LSB, update DO and capacitor-control bits, and restart CMPCK after each comparator reset while bits remain.

The module name and port list must match `l2_sar_logic_7b.va`. Keep the model voltage-domain only and deterministic. The historical source normalized for this task is `yueyh/L2_7bit_sar_logic.va`.
