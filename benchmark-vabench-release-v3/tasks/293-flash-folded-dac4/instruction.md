# Flash Folded DAC4

## Task Contract
Implement `flash_folded_dac4.va`, a 4-input folded flash-style voltage DAC. This is a data-converter L1 DUT whose MSB both contributes the coarse half-scale decision and selects the folded direction for the lower bits.

## Public Verilog-A Interface
Declare module `flash_folded_dac4(vd4, vd3, vd2, vd1, vout)` with scalar electrical ports. `vd4` is the MSB/fold select, `vd3..vd1` are lower weighted input bits, and `vout` is the analog output.

## Public Parameter Contract
Provide overrideable public parameters:

- `vth = 0.45 V`: decision threshold for each voltage-coded input bit.
- `vref = 1.0 V`: output reference/full-scale voltage.

## Required Behavior
Treat each input bit as logic one when its voltage is above `vth`. The MSB selects the folded half of the transfer. When `vd4` is high, add the lower-bit weighted value above midscale. When `vd4` is low, subtract the lower-bit weighted value from midscale. The lower bits use binary weights `4`, `2`, and `1`, and the output is scaled by `vref/16`.

## Modeling Constraints
Use deterministic voltage-domain Verilog-A and voltage contributions only. Do not emit a testbench, checker logic, out-of-band test hooks, hard-code testbench sample points, use current contributions, transistor-level devices, `ddt()`, `idt()`, or simulator side channels.

## Output Contract
Return exactly one source artifact named `flash_folded_dac4.va`.
