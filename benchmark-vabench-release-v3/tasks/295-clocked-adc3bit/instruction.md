# Source Clocked ADC3bit

Implement a clocked 3-bit ADC. On each rising clock edge, quantize VIN in [0,1] to code floor(8*VIN), clipped to 0..7.

The module name and port list must match `clocked_adc3bit.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `wangx/adc_8bit.va`.
