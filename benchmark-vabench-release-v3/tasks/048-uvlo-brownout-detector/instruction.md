# UVLO Brownout Detector

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Bias Reference and Power Management
- Target artifact: `uvlo_brownout_detector.va`
- Implement only the requested Verilog-A DUT. Do not generate a Spectre testbench, checker logic, or auxiliary test hooks.
- Preserve the public module name, port order, starter parameters, and saved waveform observable names.
- The visible testbench is a public smoke scenario. Use it to understand wiring and observables, but do not hard-code its stop time, maxstep, or exact waveform breakpoints into the DUT behavior.

## Public Verilog-A Interface

```verilog
module uvlo_brownout_detector(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

Starter parameter declarations are part of the public contract:

- `tr = 100p`: output transition rise/fall time.
- `vth = 0.45`: voltage-coded logic threshold.

## Public Behavioral Contract

- `clk` and `rst` are voltage-coded logic signals.
- Treat `vin` as the monitored supply voltage.
- Assert the power-good output `out` high only after `vin` rises above the upper UVLO threshold, around 0.65 V.
- Keep `out` high while `vin` remains in the hysteresis band between the lower and upper UVLO thresholds.
- Clear `out` low on reset or brownout below the lower threshold, around 0.55 V.
- Drive `metric` to distinguish undervoltage/brownout fault from valid power-good operation.
- Keep the model pure voltage-domain behavioral Verilog-A. Do not use branch-current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL regulation loops.

## Public Observables

Verification scenarios observe these scalar waveforms:

```text
clk rst vin out metric
```

Expected behavior categories:

- `power_good_has_hysteresis`
- `brownout_clears_power_good`
- `recovery_requires_upper_threshold`

## Output Contract

Return exactly one source artifact named `uvlo_brownout_detector.va`.
Do not include explanatory prose outside the source artifact contents.
