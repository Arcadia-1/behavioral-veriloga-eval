# Voltage-Coded NOT Gate

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Voltage-Coded Logic Support
- Domain: voltage-domain behavioral Verilog-A
- Target artifact: `source_not_gate.va`
- Required module: `source_not_gate`

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Model a reusable voltage-coded logic inverter for AMS control paths.

## Public Verilog-A Interface

`source_not_gate.va` declares module `source_not_gate` with positional ports:

```verilog
module source_not_gate(vin, vout);
```

Both ports are electrical. `vin` is the voltage-coded logic input and `vout` is
the inverted voltage-coded output.

## Public Parameter Contract

- `vlogic_high = 0.9 V`: output level for logic 1.
- `vlogic_low = 0.0 V`: output level for logic 0.
- `vtrans = 0.45 V`: input decision threshold.
- `tdel = 500p`: output propagation delay.
- `trise = 20p`: output rising transition time.
- `tfall = 20p`: output falling transition time.

## Required Behavior

Treat `vin > vtrans` as input logic 1 and `vin <= vtrans` as input logic 0.
Drive `vout` to the opposite logic value using `vlogic_high` and `vlogic_low`,
with the configured delay and transition times. The output should settle
stably after input threshold crossings.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A and smoothed voltage contributions
only. Do not use current contributions, transistor-level devices, `ddt()`,
`idt()`, hidden state unrelated to inversion, checker logic, or test-specific
sample times.

## Output Contract

Return exactly one complete Verilog-A source artifact named
`source_not_gate.va`. Do not include explanatory prose outside the source
artifact contents.
