# SAR Weighted Sum 11b

## Task Contract

- Form: `dut`.
- Level: `L1`.
- Category: data-converter weighted decoder.
- Target artifact: `sar_sum_weighted_11b.va`.
- Role: nonbinary SAR bit-weight summing DAC/decoder.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

Declare the public module exactly as:

```verilog
module sar_sum_weighted_11b(din0, din1, din2, din3, din4, din5, din6, din7, din8, din9, din10, vout);
```

`din0..din10` are voltage-coded input bits and `vout` is the analog weighted-sum output. All ports are electrical.

## Public Parameter Contract

Provide overrideable parameter `vth = 0.45` for bit decisions. The public nonbinary weights from `din10` down to `din0` are `480, 256, 128, 64, 48, 20, 12, 8, 4, 2, 1`.

## Required Behavior

Treat each input as high when it is above `vth`. Sum the selected nonbinary SAR weights into `code` and drive the normalized bipolar analog output as `vout = code / 512.0 - 1.0`. This mapping makes zero selected weight equal to `-1.0` and keeps larger selected weights monotonic positive according to the public array basis.

## Modeling Constraints

Use deterministic voltage-domain Verilog-A with voltage contributions and event-driven state where needed. Do not add checker logic, hard-code testbench-only sample times, add simulator-private side channels, use transistor-level devices, or introduce current-domain behavior.

## Output Contract

Return exactly one complete Verilog-A source file named `sar_sum_weighted_11b.va`. Do not generate a testbench, checker, waveform postprocessor, companion support module, or explanatory prose outside the requested source artifact.
