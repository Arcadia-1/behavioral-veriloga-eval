# Bias Voltage Generator With Enable/Trim

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Bias Reference and Power Management
- Target artifact: `bias_voltage_generator_with_enable_trim.va`
- Implement only the requested Verilog-A DUT. Do not generate a Spectre testbench, checker logic, or auxiliary test hooks.
- Preserve the public module name, port order, starter parameters, and saved waveform observable names.
- The visible testbench is a public smoke scenario. Use it to understand wiring and observables, but do not hard-code its stop time, maxstep, or exact waveform breakpoints into the DUT behavior.

## Public Verilog-A Interface

```verilog
module bias_voltage_generator_with_enable_trim(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

Starter parameter declarations are part of the public contract:

- `tr = 100p`: output transition rise/fall time.
- `vth = 0.45`: voltage-coded logic threshold.

## Public Behavioral Contract

- `clk` and `rst` are voltage-coded logic signals, low near 0 V and high near 0.9 V.
- Treat `vin` as a combined enable/trim request voltage.
- A low `vin` request, below about 0.25 V, disables the bias generator: drive `out` near 0 V and keep `metric` low.
- When enabled, map higher trim/control voltage to a larger bounded bias target, roughly from 0.28 V to 0.82 V.
- `out` should move smoothly toward the trim target on clocked updates instead of jumping directly to rails.
- Higher trim/control voltage should increase `out` monotonically.
- Drive `metric` high only while the bias generator is enabled and driving a valid bias.
- Keep the model pure voltage-domain behavioral Verilog-A. Do not use branch-current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL regulation loops.

## Public Observables

Verification scenarios observe these scalar waveforms:

```text
clk rst vin out metric
```

Expected behavior categories:

- `disable_forces_bias_low`
- `trim_code_moves_bias_voltage`
- `metric_marks_enabled_bias`

## Output Contract

Return exactly one source artifact named `bias_voltage_generator_with_enable_trim.va`.
Do not include explanatory prose outside the source artifact contents.
