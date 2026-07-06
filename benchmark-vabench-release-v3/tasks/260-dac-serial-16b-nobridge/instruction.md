# DAC Serial 16b Nobridge

## Task Contract

Implement `dac_serial_16b_nobridge.va` as a serial SAR-DAC prefix accumulator DUT driven by sample and SAR-ready clocks. This is a higher-complexity data-converter control/readout component, not a Spectre testbench.

## Public Verilog-A Interface

Use this exact module signature:

```verilog
module dac_serial_16b_nobridge(clk_sample, clk_sarready, data, out);
```

All ports are electrical. `clk_sample` resets the conversion frame, `clk_sarready` advances serial decisions, `data` is the voltage-coded serial decision input, and `out` is the bipolar single-ended DAC output.

## Public Parameter Contract

Provide these overrideable public parameters:

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vdd` | `1.1` | Output scaling reference. |
| `vcm` | `0.55` | Logic threshold and common-mode reference for both clocks and `data`. |

## Required Behavior

On initial step and on falling crossings of `clk_sample` through `vcm`, reset the accumulated DAC state to zero and restart the serial weight counter. On each falling crossing of `clk_sarready` through `vcm`, sample `data`; a high value contributes the next serial capacitor weight and a low value contributes zero.

Use the public prefix sequence `64, 32, 16, 16, 8` for modeled SAR-ready events. Normalize those prefix decisions against the complete 16-bit CDAC array basis. The lower continuation weights are `4, 2, 1, 1, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.015625`, plus one fixed LSB dummy/reference element of weight `0.015625`. Later SAR-ready events after the modeled prefix advance the counter but do not add additional weight. Drive `out` as `state * 2 * vdd - vdd`.

## Modeling Constraints

Use event-driven voltage-domain Verilog-A. Do not add current contributions, transistor devices, checker logic, out-of-band test hooks, simulator side channels, or hard-coded testbench sample times.

## Output Contract

Return exactly one source artifact named `dac_serial_16b_nobridge.va`.
