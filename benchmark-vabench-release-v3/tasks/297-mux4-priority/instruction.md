# Mux4 Priority

## Task Contract
Implement `mux4_priority.va`, a voltage-domain 4-to-1 analog signal multiplexer selected by two voltage-coded control bits. This is an AMS routing/helper DUT rather than a pure Boolean gate.

## Public Verilog-A Interface
Declare module `mux4_priority(sel0, sel1, in0, in1, in2, in3, out)` with scalar electrical ports. `sel0` is the LSB select bit, `sel1` is the MSB select bit, `in0..in3` are analog input voltages, and `out` is the selected analog output.

## Public Parameter Contract
Provide overrideable public parameter `vth = 0.45 V` as the decision threshold for `sel0` and `sel1`.

## Required Behavior
Decode the select code as `sel0 + 2*sel1`. For code `0`, forward `in0` to `out`; for code `1`, forward `in1`; for code `2`, forward `in2`; for code `3`, forward `in3`. The selected analog voltage should pass through without quantization or rail coding.

## Modeling Constraints
Use deterministic voltage-domain Verilog-A and voltage contributions only. Do not emit a testbench, checker logic, out-of-band test hooks, hard-code testbench sample points, use current contributions, transistor-level devices, `ddt()`, `idt()`, or simulator side channels.

## Output Contract
Return exactly one source artifact named `mux4_priority.va`.
