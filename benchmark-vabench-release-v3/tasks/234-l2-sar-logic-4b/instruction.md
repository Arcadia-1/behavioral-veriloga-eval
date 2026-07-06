# L2 SAR Logic 4b

## Task Contract

- Form: `dut`.
- Level: `L2`.
- Category: SAR ADC asynchronous control logic.
- Target artifact: `l2_sar_logic_4b.va`.
- Role: 4-bit SAR comparator-clock and capacitor-control sequencer.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

Declare the public module exactly as:

```verilog
module l2_sar_logic_4b(clkc, clks, dcmpp, dcmpn, cmpck, do0, do1, do2, do3, dctrlp1, dctrlp2, dctrlp3, dctrln1, dctrln2, dctrln3);
```

`clkc` starts comparator activity, `clks` resets conversion state, `dcmpp/dcmpn` are comparator outputs, `cmpck` is comparator clock request, `do0..do3` are code bits, and `dctrlp1..dctrlp3`/`dctrln1..dctrln3` are capacitor controls. All ports are electrical.

## Public Parameter Contract

Provide overrideable parameters `vdd = 1.1` and `t_logic_delay = 100p`. Use `vdd/2` as the threshold and 0/`vdd` as output levels.

## Required Behavior

On initialization and rising `clks`, reset the step counter, code bits, control bits, and `cmpck`. A rising `clkc` asserts `cmpck`. Each rising comparator pulse records the current MSB-to-LSB decision, lowers `cmpck`, and updates the matching capacitor-control side while bits remain. When the comparator output falls, advance to the next step and reassert `cmpck` until the conversion finishes.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `l2_sar_logic_4b.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
