# Bias Voltage Generator With Enable/Trim

## Task Contract

Implement the requested Verilog-A artifact for `Bias Voltage Generator With Enable Trim`.
- Form: `dut`
- Level: `L1`
- Category: `bias_reference_power_management`
- Target artifact(s): `bias_voltage_generator_with_enable_trim.va`

- Target artifact: `bias_voltage_generator_with_enable_trim.va`
- Implement only the requested Verilog-A DUT. Do not generate a Spectre testbench, validation logic, or auxiliary test hooks.
- Preserve the public module name, port order, starter parameters, and saved waveform observable names.

## Public Verilog-A Interface

```verilog
module bias_voltage_generator_with_enable_trim(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

## Public Parameter Contract

Starter parameter declarations are part of the public contract:

| Parameter | Default | Contract |
| --- | ---: | --- |
| `tr` | `100p` | Output transition rise/fall time. |
| `vth` | `0.45` | Voltage-coded clock/reset logic threshold. |

## Required Behavior

- `clk` and `rst` are voltage-coded logic signals, low near 0 V and high near 0.9 V.
- Treat `vin` as a combined enable/trim request voltage.
- A low `vin` request, below about 0.25 V, disables the bias generator: drive `out` near 0 V and keep `metric` low.
- When enabled, map higher trim/control voltage to a larger bounded bias target, roughly from 0.28 V to 0.82 V.
- `out` should move smoothly toward the trim target on clocked updates instead of jumping directly to rails.
- Higher trim/control voltage should increase `out` monotonically.
- Drive `metric` high only while the bias generator is enabled and driving a valid bias.
- Keep the model pure voltage-domain behavioral Verilog-A. Do not use branch-current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL regulation loops.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one source artifact named `bias_voltage_generator_with_enable_trim.va`.
Do not include explanatory prose outside the source artifact contents.
