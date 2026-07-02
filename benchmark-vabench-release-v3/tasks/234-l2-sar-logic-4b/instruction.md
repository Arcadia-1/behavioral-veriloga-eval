# 4-bit SAR Logic Controller

Implement the Verilog-A module `l2_sar_logic_4b` in `l2_sar_logic_4b.va`.

## Public Interface

Use the exact module interface:

```verilog
module l2_sar_logic_4b(clkc, clks, dcmpp, dcmpn, cmpck, do0, do1, do2, do3, dctrlp1, dctrlp2, dctrlp3, dctrln1, dctrln2, dctrln3);
input clkc, clks, dcmpp, dcmpn;
output cmpck, do0, do1, do2, do3, dctrlp1, dctrlp2, dctrlp3, dctrln1, dctrln2, dctrln3;
electrical clkc, clks, dcmpp, dcmpn, cmpck, do0, do1, do2, do3, dctrlp1, dctrlp2, dctrlp3, dctrln1, dctrln2, dctrln3;
```

Public parameters should include `vdd=1.1` and a comparator-clock logic delay, defaulting to 100 ps.

## Required Behavior

Model a standalone 4-bit SAR controller. A rising `clks` transition resets the conversion state, clears `cmpck`, clears `do0..do3`, and clears all `dctrlp*`/`dctrln*` outputs. A rising `clkc` transition starts comparison by driving `cmpck` high. Each comparator pulse on `dcmpp` or `dcmpn` closes `cmpck`, latches the current MSB-to-LSB decision into `do3`, `do2`, `do1`, then `do0`, and updates the corresponding positive or negative DAC control for the remaining comparison steps. When a comparator pulse falls, advance to the next step and re-enable `cmpck` until the four-bit conversion is complete.

## Modeling Contract

Treat all controls as voltage-domain logic referenced to `vdd`; this is an L1 controller task despite the historical module name. Keep the model event-driven and voltage-domain; do not use transistor-level devices, current injection, hidden test hooks, or checker-specific side channels.
