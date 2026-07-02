# Flash ADC Selected Threshold Taps

Implement a clocked selected-tap flash ADC thermometer output.

## Public Interface

Declare module `flash_adc_threshold_taps` with positional ports `vin, clk,
dout0, dout1, dout2, dout3, dout4, dout5, dout6`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vrefp = 0.125 V`: upper endpoint of the flash reference range.
- `vrefn = -0.125 V`: lower endpoint of the flash reference range.
- `vl = 0.0 V`: low output level.
- `vh = 0.9 V`: high output level.
- `vth = 0.45 V`: rising-edge threshold for `clk`.

## Functional Contract

On each rising `clk` edge, sample analog input `vin` and update seven scalar
thermometer outputs. Use the parameterized flash range from `vrefn` to `vrefp`
and expose selected thresholds from a 31-level flash ADC ladder. The selected
tap indices are 1, 5, 10, 15, 20, 25, and 30, where threshold index `k`
corresponds to the kth subdivision between `vrefn` and `vrefp`.

Each output should drive `vh` when the sampled `vin` is above its selected
threshold and `vl` otherwise.

## Modeling Constraints

Return only `flash_adc_threshold_taps.va`. Use deterministic voltage-domain
Verilog-A and smooth output transitions. Do not modify or emit the support
testbench, add checker logic, hard-code private waveform sample points, add
simulator-private side channels, use current contributions, `ddt()`, or
`idt()`.
