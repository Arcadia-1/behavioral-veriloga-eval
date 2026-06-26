# Source DAC Serial 16b Nobridge

Implement the serial SAR DAC accumulator. CLK_SAMPLE falling resets state and counter; each CLK_SARREADY falling edge consumes DATA and adds the next capacitor weight before driving a bipolar output.

The module name and port list must match `dac_serial_16b_nobridge.va`. Keep the implementation deterministic and voltage-domain only. The historical source normalized for this task is `zhangz/DAC_serial_16b_nobridge_va.va`.
