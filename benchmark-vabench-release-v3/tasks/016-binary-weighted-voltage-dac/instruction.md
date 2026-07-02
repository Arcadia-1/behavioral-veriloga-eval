# Binary Weighted Voltage DAC

Implement a 4-bit binary-weighted voltage DAC.

## Public Interface

Declare module `simple_binary_voltage_dac_4b` with positional ports `code_0,
code_1, code_2, code_3, vref, vss, aout`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: digital decision threshold for each code bit.
- `tr = 500 ps`: output transition smoothing time.

## Functional Contract

Treat `code_0..code_3` as an unsigned 4-bit binary word with weights 1, 2, 4,
and 8. Drive `aout` linearly between `vss` and `vref`, with the all-zero input
at `vss` and the all-ones input at `vref`. The output should update
continuously with input bit changes.

## Modeling Constraints

Return only `simple_binary_voltage_dac_4b.va`. Use deterministic
voltage-domain Verilog-A and smooth output transitions. Do not modify or emit
the support testbench, add checker logic, hard-code private waveform sample
points, add simulator-private side channels, use current contributions,
`ddt()`, or `idt()`.
