# Thermometer Code Decoder

## Task Contract

Implement the requested Verilog-A artifact for `Thermometer Code Decoder`.
- Form: `dut`
- Level: `L1`
- Category: `testbench_utility_modules`
- Target artifact(s): `thermometer_decoder_guarded.va`

Implement `thermometer_decoder_guarded.va`, a small guarded binary-to-thermometer voltage-domain utility for compact AMS validation harnesses.

- This is a DUT/support-component task: implement only the requested Verilog-A source artifact.
- Do not generate a Spectre testbench or validation harness.
- Preserve the public module name, port order, port directions, and parameter names.
- Treat any public validation harness as an observable use case, not as values to hard-code into the DUT.

## Public Verilog-A Interface

```verilog
module thermometer_decoder_guarded(b0, b1, en, th0, th1, th2, th3);
```

All ports are electrical. Inputs are `b0`, `b1`, and `en`; outputs are `th0`, `th1`, `th2`, and `th3`.

## Public Parameter Contract

| Parameter | Default | Contract |
| --- | ---: | --- |
| `vdd` | `0.9` | Logic-high output voltage. |
| `vth` | `0.45` | Decision threshold for `b0`, `b1`, and `en`. |
| `tr` | `300p` | Output transition rise/fall smoothing time. |

## Required Behavior

- Decode `b1:b0` as an unsigned two-bit code with `b1` as the most significant bit.
- When `en` is high, drive a cumulative thermometer prefix: code 0 drives all outputs low, code 1 drives only `th0` high, code 2 drives `th0` and `th1` high, and code 3 drives `th0`, `th1`, and `th2` high.
- Keep `th3` guarded low for the two-bit input range.
- When `en` is low, force all thermometer outputs low regardless of the code.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Treat voltage-coded logic low as near 0 V and logic high as near `vdd`.
- Use `transition(...)` or equivalent smooth voltage contributions for driven logic outputs.
- Do not instantiate transistor-level devices, use current-branch contributions, AC/noise analysis, validation logic, validation-only hooks, or simulator-specific side channels.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete Verilog-A source file named `thermometer_decoder_guarded.va`.
