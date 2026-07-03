# LDO Regulator Macro Model

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Bias Reference and Power Management
- Target artifact: `ldo_regulator_macro_model.va`
- Implement only the requested Verilog-A DUT. Do not generate a Spectre testbench, checker logic, or auxiliary test hooks.
- Preserve the public module name, port order, starter parameters, and saved waveform observable names.
- The visible testbench is a public smoke scenario. Use it to understand wiring and observables, but do not hard-code its stop time, maxstep, or exact waveform breakpoints into the DUT behavior.

## Public Verilog-A Interface

```verilog
module ldo_regulator_macro_model(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

Starter parameter declarations are part of the public contract:

- `tr = 100p`: output transition rise/fall time.
- `vth = 0.45`: voltage-coded logic threshold.

## Public Behavioral Contract

- `clk` and `rst` are voltage-coded logic signals.
- Treat `vin` as a bounded load/disturbance-control voltage, not as the regulator supply rail.
- Under light load, keep `out` bounded near the nominal regulated output around 0.60 V.
- Higher load/disturbance should cause visible droop from the nominal target, not rail-to-rail tracking.
- After a load reduction, `out` should recover gradually toward the regulation target over clocked updates.
- Drive `metric` high when regulation error is small and lower during droop/recovery.
- Keep all outputs in the 0 V to 0.9 V voltage-domain range.
- Keep the model pure voltage-domain behavioral Verilog-A. Do not use branch-current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL regulation loops.

## Public Observables

Verification scenarios observe these scalar waveforms:

```text
clk rst vin out metric
```

Expected behavior categories:

- `regulated_output_bounded`
- `load_step_causes_droop`
- `output_recovers_after_load_reduction`

## Output Contract

Return exactly one source artifact named `ldo_regulator_macro_model.va`.
Do not include explanatory prose outside the source artifact contents.
