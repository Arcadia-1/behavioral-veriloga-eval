# Bipolar DFF Sample

## Task Contract
Implement `bipolar_dff_sample.va`, a rising-edge voltage-domain D flip-flop with complementary bipolar outputs. This is a clocked AMS control/helper component.

## Public Verilog-A Interface
Declare module `bipolar_dff_sample(vin_d, vclk, vout_q, vout_qbar)` with scalar electrical ports. `vin_d` is the sampled data input, `vclk` is the clock, and `vout_q`/`vout_qbar` are complementary bipolar outputs.

## Public Parameter Contract
Provide overrideable public parameters:

- `vth = 0.0 V`: data threshold for `vin_d`.
- `vclk_th = 0.45 V`: rising-edge threshold for `vclk`.

Output levels are `+1 V` and `-1 V`.

## Required Behavior
On each rising crossing of `vclk` through `vclk_th`, sample whether `vin_d` is above `vth`. Hold the sampled state between clock edges. Drive `vout_q` to `+1 V` for sampled high and `-1 V` for sampled low. Drive `vout_qbar` as the complementary bipolar output.

## Modeling Constraints
Use deterministic voltage-domain Verilog-A and smooth voltage-coded output transitions. Do not emit a testbench, checker logic, out-of-band test hooks, hard-code testbench sample points, use current contributions, transistor-level devices, AC/noise analysis, `ddt()`, `idt()`, or simulator side channels.

## Output Contract
Return exactly one source artifact named `bipolar_dff_sample.va`.
