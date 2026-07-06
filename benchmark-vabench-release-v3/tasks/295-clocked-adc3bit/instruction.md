# Clocked ADC3bit

## Task Contract
Implement `clocked_adc3bit.va`, a clocked 3-bit voltage-output ADC DUT. This is a data-converter L1 component with explicit bit-bus outputs rather than a scalar analog code output.

## Public Verilog-A Interface
Declare module `clocked_adc3bit(vd2, vd1, vd0, vin, vclk)` with scalar electrical ports. `vin` is the analog input, `vclk` is the sampling clock, `vd2` is the MSB output bit, and `vd0` is the LSB output bit.

## Public Parameter Contract
Provide overrideable public parameters:

- `vth_clk = 0.45 V`: rising-edge threshold for `vclk`.
- `vh = 0.9 V`: logic-high output level.

The output low level is `0 V`; the public input conversion range is `0 V` to `1 V`.

## Required Behavior
On each rising crossing of `vclk` through `vth_clk`, sample `vin` and quantize the `0 V` to `1 V` range into eight uniform lower-inclusive bins. Values below `0 V` clip to code `0`; values at or above `1 V` clip to code `7`. Drive `vd2`, `vd1`, and `vd0` as the binary representation of the held sampled code using `vh` for logic one and `0 V` for logic zero.

## Modeling Constraints
Use deterministic voltage-domain Verilog-A and voltage contributions only. Do not emit a testbench, checker logic, out-of-band test hooks, file I/O, random behavior, current contributions, transistor-level devices, `ddt()`, `idt()`, or simulator side channels.

## Output Contract
Return exactly one source artifact named `clocked_adc3bit.va`.
