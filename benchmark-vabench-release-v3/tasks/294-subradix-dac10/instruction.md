# Subradix DAC10

## Task Contract
Implement `subradix_dac10.va`, a 10-bit voltage-coded sub-radix weighted DAC. This is a data-converter L1 DUT distinct from binary-weighted DAC rows because adjacent weights follow radix `1.8`.

## Public Verilog-A Interface
Declare module `subradix_dac10(vd9, vd8, vd7, vd6, vd5, vd4, vd3, vd2, vd1, vd0, vout)` with scalar electrical ports. `vd9` is the MSB and `vd0` is the LSB.

## Public Parameter Contract
Provide overrideable public parameters:

- `vth = 0.45 V`: decision threshold for each input bit.
- `vref = 1.0 V`: output full-scale/reference voltage.

## Required Behavior
Treat each input as logic one when its voltage is greater than `vth`. Decode `vd9..vd0` as a sub-radix word whose adjacent bit weights follow radix `1.8`, with `vd0` weight one and `vd9` weight `1.8^9`. Scale the active-weight sum by the all-ones sub-radix weight sum so that all ones maps to `vref`.

## Modeling Constraints
Use deterministic voltage-domain Verilog-A and voltage contributions only. It is acceptable to express sub-radix weights with portable real arithmetic such as `pow(1.8, k)`. Do not emit a testbench, checker logic, out-of-band test hooks, hard-code testbench sample points, use current contributions, transistor-level devices, `ddt()`, `idt()`, or simulator side channels.

## Output Contract
Return exactly one source artifact named `subradix_dac10.va`.
