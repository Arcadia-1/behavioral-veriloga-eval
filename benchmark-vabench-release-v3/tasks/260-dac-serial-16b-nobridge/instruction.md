# DAC Serial 16b Nobridge

Implement a serial SAR-DAC prefix accumulator driven by sample and SAR-ready
clocks.

## Public Interface

Declare module `dac_serial_16b_nobridge` with positional ports `clk_sample,
clk_sarready, data, out`. All ports are electrical. `clk_sample`,
`clk_sarready`, and `data` are inputs, and `out` is the output.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vdd = 1.1 V`: output scaling reference for the bipolar single-ended output.
- `vcm = 0.55 V`: logic threshold and common-mode reference for the sample
  clock, SAR-ready clock, and serial data input.

## Functional Contract

On initial step and on falling crossings of `clk_sample` through `vcm`, reset
the accumulated DAC state to zero and restart the serial weight counter.

On each falling crossing of `clk_sarready` through `vcm`, sample `data`. A high
data value contributes the next serial capacitor weight, while a low data value
contributes zero; then advance the serial weight counter.

Use the front-end SAR-DAC serial prefix sequence `64, 32, 16, 16, 8` for the
modeled ready events. Normalize those prefix decisions against the complete
16-bit CDAC array basis, not just the prefix sum. The full array basis continues
with lower weights `4, 2, 1, 1, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625,
0.015625` and includes one fixed LSB dummy/reference element of weight
`0.015625`. These lower continuation weights define the normalization basis;
later SAR-ready events after the modeled prefix do not add additional weight in
this task contract.

Drive `out` as a bipolar single-ended voltage scaled by `vdd` from the
accumulated normalized code, with a small transition smoothing suitable for
transient simulation.

## Modeling Constraints

Return only `dac_serial_16b_nobridge.va`. Use voltage contributions only. Do
not modify or emit the support testbench, add checker logic, hard-code private
waveform sample points, add simulator-private side channels, use current
contributions, `ddt()`, or `idt()`.
