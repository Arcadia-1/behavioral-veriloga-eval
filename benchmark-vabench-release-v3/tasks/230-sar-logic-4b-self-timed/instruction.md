# 4-bit Self-Timed SAR Logic

Implement the Verilog-A module `sar_logic_4b_self_timed` in `sar_logic_4b_self_timed.va`.

## Public Interface

Use the exact module interface:

```verilog
module sar_logic_4b_self_timed(vdd, gnd, clkc, rst, dcmpp, dcmpn, cmpck, dout1, dout2, dout3, dout4, dbotp1, dbotp2, dbotp3, dbotn1, dbotn2, dbotn3);
input vdd, gnd, clkc, rst, dcmpp, dcmpn;
output cmpck, dout1, dout2, dout3, dout4, dbotp1, dbotp2, dbotp3, dbotn1, dbotn2, dbotn3;
electrical vdd, gnd, clkc, rst, dcmpp, dcmpn, cmpck, dout1, dout2, dout3, dout4, dbotp1, dbotp2, dbotp3, dbotn1, dbotn2, dbotn3;
```

Public parameters should include a comparator-clock logic delay, defaulting to 100 ps.

## Required Behavior

Model a four-decision self-timed SAR controller. On `initial_step` and on each rising `rst` transition, reset the conversion state, clear `cmpck` and `dout1..dout4`, and initialize the bottom-plate control outputs high. A rising `clkc` transition schedules `cmpck` high after the logic delay. Each comparator pulse on `dcmpp` or `dcmpn` lowers `cmpck` after the logic delay, stores the current MSB-to-LSB decision into `dout4`, `dout3`, `dout2`, then `dout1`, and updates the matching positive or negative bottom-plate control for the remaining comparison steps. When the comparator pulse falls, advance to the next step and re-enable `cmpck` after the logic delay until all four decisions are complete.

## Modeling Contract

Use the `vdd` and `gnd` pins to derive logic levels and the switching threshold. Keep the model event-driven and voltage-domain; do not use transistor-level devices, current injection, hidden test hooks, or checker-specific side channels.
