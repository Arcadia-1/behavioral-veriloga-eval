# L3 SAR2 Logic 7b

## Task Contract

- Form: `dut`.
- Level: `L2`.
- Category: SAR ADC active-low comparator control logic.
- Target artifact: `l3_sar2_logic_7b.va`.
- Role: 7-bit SAR controller with active-low comparator decision pulses.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

Declare the public module exactly as:

```verilog
module l3_sar2_logic_7b(clk, dp, dn, cmpck, do0, do1, do2, do3, do4, do5, do6, sp1, sp2, sp3, sp4, sp5, sp6, sn1, sn2, sn3, sn4, sn5, sn6);
```

`clk` starts and resets conversion, `dp/dn` are active-low comparator decision pulses, `cmpck` requests comparator activity, `do0..do6` are published code bits, and `sp1..sp6`/`sn1..sn6` are capacitor-selection controls. All ports are electrical.

## Public Parameter Contract

Provide overrideable parameters `vdd = 0.9` and `t_logic_delay = 10p`. Use `vdd/2` as the threshold and 0/`vdd` as output levels.

## Required Behavior

On a falling `clk` edge, reset conversion state and clear the published code bits. On a rising `clk` edge, start the MSB-to-LSB sequence and assert `cmpck`. Each falling `dp` or `dn` edge records one active-low comparator decision; `dn` falling selects the current bit high, while `dp` falling selects it low. When the comparator outputs recover high, advance to the next bit and assert `cmpck` again while bits remain. After the final bit decision, publish `do6..do0` and leave `cmpck` low. The `sp`/`sn` controls should reflect the latched decisions for bits 6 down to 1.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `l3_sar2_logic_7b.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
