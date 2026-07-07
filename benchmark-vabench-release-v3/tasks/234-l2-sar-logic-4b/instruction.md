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

On initialization and rising `clks`, reset the conversion to step 3, clear `do0..do3`, clear `dctrlp1..dctrlp3` and `dctrln1..dctrln3`, and clear `cmpck`. A rising `clkc` asserts `cmpck`.

Each rising comparator pulse on `dcmpp` or `dcmpn` records the current MSB-to-LSB decision and lowers `cmpck`. Treat `dcmpp > dcmpn` as a positive decision. For the current step sequence 3, 2, 1, 0, store the decision in `do{step}`. For steps 3, 2, and 1, a positive decision sets `dctrln{step}` high, while a negative decision sets `dctrlp{step}` high. Step 0 only latches `do0` and does not update a capacitor-control output. When the comparator output falls, decrement the step and reassert `cmpck` if the new step is still 0 or greater.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `l2_sar_logic_4b.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
