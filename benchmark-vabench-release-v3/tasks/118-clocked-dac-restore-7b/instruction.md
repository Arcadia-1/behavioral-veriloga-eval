# Clocked DAC Restore 7b

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Data Converter Models
- Domain: voltage-domain behavioral Verilog-A
- Target artifact: `clocked_dac_restore_7b.va`
- Required module: `clocked_dac_restore_7b`

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, positional port order, parameters, and waveform observable names.
- Model a clocked 7-bit DAC restoration primitive.

## Public Verilog-A Interface

`clocked_dac_restore_7b.va` declares module `clocked_dac_restore_7b` with this
positional port order:

```verilog
module clocked_dac_restore_7b(D1, D2, D3, D4, D5, D6, D0, CLK, VOUT);
```

All ports are electrical. `D6` through `D0` are voltage-coded input bits, `CLK`
is the update clock, and `VOUT` is the restored analog output. The positional
interface intentionally places `D0` after `D6`; preserve that order while
interpreting `D6` as the MSB and `D0` as the LSB.

## Public Parameter Contract

- `vth = 0.45 V`: threshold for input bits and rising-clock detection.
- `lsb = 1.8 / 128.0 V`: midrise DAC step size.
- `tr = 20p`: transition smoothing time for `VOUT`.

## Required Behavior

On each rising crossing of `CLK` through `vth`, decode the voltage-coded input
word as a 7-bit unsigned code with weights `D6..D0 = 64, 32, 16, 8, 4, 2, 1`.
Hold the decoded code between clock edges.

Drive `VOUT` as a bipolar midrise restored level:

```text
VOUT = (code + 0.5) * lsb - 0.9
```

The public observable behavior includes stable restored levels after clock
edges and preservation of the MSB-to-LSB bit ordering above.

## Modeling Constraints

Use voltage-domain event-driven Verilog-A with smoothed output transitions. Do
not use current contributions, transistor-level devices, `ddt()`, `idt()`,
checker logic, or testbench-specific sample windows inside the DUT.

## Output Contract

Return exactly one complete Verilog-A source artifact named
`clocked_dac_restore_7b.va`. Do not include explanatory prose outside the source
artifact contents.
