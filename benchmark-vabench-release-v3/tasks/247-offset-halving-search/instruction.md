# Offset Halving Search

## Task Contract

- Form: `dut`.
- Level: `L1`.
- Category: comparator calibration/control primitive.
- Target artifact: `offset_halving_search.va`.
- Role: comparator-directed differential offset search with fixed step halving.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

Declare the public module exactly as:

```verilog
module offset_halving_search(clk, dcmpp, vinp, vinn);
```

`clk` is the update clock, `dcmpp` is the comparator decision input, and `vinp/vinn` are generated differential stimulus outputs. All ports are electrical.

## Public Parameter Contract

Provide overrideable parameter `vdd = 0.9`. Use `0.5*vdd` as the clock and decision threshold. Use a 0.1 V initial search step.

## Required Behavior

Initialize the differential residue to zero. On each falling `clk` crossing, sample `dcmpp`, update the signed search residue opposite the comparator decision, and halve the step for the next update. Drive `vinp` and `vinn` symmetrically around `0.5*vdd` from the current residue.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `offset_halving_search.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
