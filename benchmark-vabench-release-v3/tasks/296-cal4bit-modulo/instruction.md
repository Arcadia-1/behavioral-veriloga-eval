# CAL4bit Floor-Clamped Encoder

## Task Contract
Implement `cal4bit_modulo.va`, a scalar-to-4-bit voltage-coded calibration encoder. Despite the historical module name, the public behavior is floor-then-clamp encoding, not modulo wrapping.

## Public Verilog-A Interface
Declare module `cal4bit_modulo(ain, d0, d1, d2, d3)` with scalar electrical ports. `ain` is an analog code-level input. `d0..d3` are output bits ordered from least-significant bit to most-significant bit.

## Public Parameter Contract
Provide overrideable public parameter `vh = 0.9 V` for the output logic-high level. The output low level is `0 V`.

## Required Behavior
Floor `V(ain)` to an integer code, clamp the code to the valid 4-bit range `0..15`, and emit the clamped code on `d0..d3`. Active bits should be near `vh`; inactive bits should be near `0 V`.

## Modeling Constraints
Use deterministic voltage-domain Verilog-A and smooth voltage-coded output transitions. Do not emit a testbench, checker logic, out-of-band test hooks, hard-code testbench sample points, use current contributions, transistor-level devices, `ddt()`, `idt()`, or simulator side channels.

## Output Contract
Return exactly one source artifact named `cal4bit_modulo.va`.
