# SAR Logic

## Task Contract

Implement the requested Verilog-A artifact for `SAR Logic`.
- Form: `dut`
- Level: `L1`
- Category: `data_converter`
- Target artifact(s): `sar_logic_4b.va`

Implement a 4-bit voltage-domain SAR decision sequencer.

## Public Verilog-A Interface

Declare module `sar_logic_4b` with positional ports `VDD, VSS, CLKS, DCOMP,
DP_DAC_3, DP_DAC_2, DP_DAC_1, DP_DAC_0, RDY`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: decision threshold for `CLKS` and `DCOMP`.
- `tedge = 1 ns`: output transition smoothing time.

## Required Behavior

Implement a 4-bit successive-approximation state machine clocked by rising
`CLKS` edges. Initialize the conversion by trying the most significant DAC bit.
At each decision step, use `DCOMP` to decide whether the current trial bit stays
set or is cleared, then advance the trial to the next lower bit. A `DCOMP`
voltage at or above `vth` keeps the active trial bit set; a `DCOMP` voltage
below `vth` clears that trial bit before advancing. After bit 0 is resolved,
assert `RDY` and hold the final DAC decision pins. On the following clock,
restart the sequencer for the next conversion.

Drive `DP_DAC_3..DP_DAC_0` and `RDY` as voltage-coded outputs between `VSS`
and `VDD`.

## Modeling Constraints

Return only `sar_logic_4b.va`. Use deterministic voltage-domain Verilog-A and
smooth output transitions. Do not modify or emit the support testbench, add
validation logic, hard-code specific waveform sample points, add simulator-specific
side channels, use current contributions, `ddt()`, or `idt()`.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `sar_logic_4b.va`. Do not include explanatory prose outside the source artifact contents.
