# PTAT/CTAT Reference Generator

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Bias Reference and Power Management
- Target artifact: `ptat_ctat_reference_generator.va`
- Implement only the requested Verilog-A DUT. Do not generate a Spectre testbench, checker logic, or auxiliary test hooks.
- Preserve the public module name, port order, starter parameters, and saved waveform observable names.
- The visible testbench is a public smoke scenario. Use it to understand wiring and observables, but do not hard-code its stop time, maxstep, or exact waveform breakpoints into the DUT behavior.

## Public Verilog-A Interface

```verilog
module ptat_ctat_reference_generator(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

Starter parameter declarations are part of the public contract:

- `tr = 100p`: output transition rise/fall time.
- `vth = 0.45`: voltage-coded logic threshold.

## Public Behavioral Contract

- `clk` and `rst` are voltage-coded logic signals.
- Treat `vin` as a normalized temperature/control voltage in the 0 V to 0.9 V range.
- Build opposing PTAT and CTAT branch abstractions.
- Drive `metric` as a public PTAT-like observable that increases with the temperature/control voltage.
- Combine PTAT and CTAT behavior so `out` stays near a bounded reference around mid-scale instead of strongly tracking `vin`.
- Reset should initialize `out` near mid-scale and keep `metric` low until valid updates occur.
- Clamp `out` and `metric` to the public 0 V to 0.9 V voltage-domain range.
- Keep the model pure voltage-domain behavioral Verilog-A. Do not use branch-current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL regulation loops.

## Public Observables

Verification scenarios observe these scalar waveforms:

```text
clk rst vin out metric
```

Expected behavior categories:

- `ptat_branch_monotonic_with_temperature`
- `ctat_compensation_flattens_reference`
- `reference_common_mode_bounded`

## Output Contract

Return exactly one source artifact named `ptat_ctat_reference_generator.va`.
Do not include explanatory prose outside the source artifact contents.
