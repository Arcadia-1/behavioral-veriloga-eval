# 4-bit Self-Timed SAR Logic

## Task Contract

- Form: `dut`.
- Level: `L2`.
- Category: SAR ADC self-timed control logic.
- Target artifact: `sar_logic_4b_self_timed.va`.
- Role: four-decision self-timed SAR controller.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

Declare the public module exactly as:

```verilog
module sar_logic_4b_self_timed(vdd, gnd, clkc, rst, dcmpp, dcmpn, cmpck, dout1, dout2, dout3, dout4, dbotp1, dbotp2, dbotp3, dbotn1, dbotn2, dbotn3);
```

`vdd/gnd` provide logic rails, `clkc` starts comparator activity, `rst` resets the conversion, `dcmpp/dcmpn` are comparator outputs, `cmpck` is the comparator clock request, `dout1..dout4` are code bits, and `dbotp1..dbotp3`/`dbotn1..dbotn3` are bottom-plate controls. All ports are electrical.

## Public Parameter Contract

Provide overrideable parameter `t_logic_delay = 100p`. Derive logic high, low, and threshold from the `vdd` and `gnd` pins.

## Required Behavior

At initialization and on each rising `rst` transition, reset the conversion state, clear `cmpck` and `dout1..dout4`, and initialize bottom-plate controls high. A rising `clkc` transition schedules `cmpck` high after the logic delay. Each rising comparator pulse on `dcmpp` or `dcmpn` lowers `cmpck` after the logic delay, stores the current MSB-to-LSB decision, and updates the matching positive or negative bottom-plate control for the remaining steps. When the comparator pulse falls, advance to the next step and re-enable `cmpck` after the delay until all decisions are complete.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `sar_logic_4b_self_timed.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
