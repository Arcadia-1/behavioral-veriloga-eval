# SAR Logic

Implement a 4-bit voltage-domain SAR decision sequencer.

## Public Interface

Declare module `sar_logic_4b` with positional ports `VDD, VSS, CLKS, DCOMP,
DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: decision threshold for `CLKS` and `DCOMP`.
- `tedge = 1 ns`: output transition smoothing time.

## Functional Contract

Implement a 4-bit successive-approximation state machine clocked by rising
`CLKS` edges. Initialize the conversion by trying the most significant DAC bit.
At each decision step, use `DCOMP` to decide whether the current trial bit stays
set or is cleared, then advance the trial to the next lower bit. After bit 0 is
resolved, assert `RDY` and hold the final DAC decision pins. On the following
clock, restart the sequencer for the next conversion.

Drive `DP_DAC_3..DP_DAC_0` and `RDY` as voltage-coded outputs between `VSS`
and `VDD`.

## Modeling Constraints

Return only `sar_logic_4b.va`. Use deterministic voltage-domain Verilog-A and
smooth output transitions. Do not modify or emit the support testbench, add
checker logic, hard-code private waveform sample points, add simulator-private
side channels, use current contributions, `ddt()`, or `idt()`.
