# Bandgap Reference Macro Model

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Bias Reference and Power Management
- Target artifact: `bandgap_reference_macro_model.va`
- Implement only the requested Verilog-A DUT. Do not generate a Spectre testbench, checker logic, or auxiliary test hooks.
- Preserve the public module name, port order, starter parameters, and saved waveform observable names.
- The visible testbench is a public smoke scenario. Use it to understand wiring and observables, but do not hard-code its stop time, maxstep, or exact waveform breakpoints into the DUT behavior.

## Public Verilog-A Interface

```verilog
module bandgap_reference_macro_model(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

Starter parameter declarations are part of the public contract:

- `tr = 100p`: output transition rise/fall time.
- `vth = 0.45`: voltage-coded logic threshold.
- `vstart = 0.58`: nominal startup supply threshold.
- `vref = 0.55`: nominal regulated reference target.

## Public Behavioral Contract

- `clk` and `rst` are voltage-coded logic signals, low near 0 V and high near 0.9 V.
- `vin` is a sub-1 V supply ramp for the reference macro.
- During reset or below the startup threshold, hold `out` near 0 V and keep `metric` low.
- After startup, regulate `out` near the nominal reference voltage and make it weakly sensitive to supply variation rather than supply-tracking.
- During brownout, return `out` near 0 V and mark the reference invalid.
- Drive `metric` as a voltage-coded reference-valid observable: low before startup/brownout, high while the reference is valid.
- Keep the model pure voltage-domain behavioral Verilog-A. Do not use branch-current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL regulation loops.

## Public Observables

Verification scenarios observe these scalar waveforms:

```text
clk rst vin out metric
```

Expected behavior categories:

- `startup_threshold_blocks_reference`
- `reference_settles_near_nominal`
- `line_regulation_is_bounded`

## Output Contract

Return exactly one source artifact named `bandgap_reference_macro_model.va`.
Do not include explanatory prose outside the source artifact contents.
