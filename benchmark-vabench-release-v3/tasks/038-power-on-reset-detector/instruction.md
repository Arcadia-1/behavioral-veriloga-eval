# Power-On Reset Detector

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Bias Reference and Power Management
- Target artifact: `power_on_reset_detector.va`
- Implement only the requested Verilog-A DUT. Do not generate a Spectre testbench, checker logic, or auxiliary test hooks.
- Preserve the public module name, port order, starter parameters, and saved waveform observable names.
- The visible testbench is a public smoke scenario. Use it to understand wiring and observables, but do not hard-code its stop time, maxstep, or exact waveform breakpoints into the DUT behavior.

## Public Verilog-A Interface

```verilog
module power_on_reset_detector(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

Starter parameter declarations are part of the public contract:

- `tr = 100p`: output transition rise/fall time.
- `vth = 0.45`: voltage-coded logic threshold.
- `vtrip = 0.62`: nominal supply-good threshold.

## Public Behavioral Contract

- `clk` and `rst` are voltage-coded logic signals.
- Treat `vin` as the monitored supply ramp and brownout stimulus.
- `out` is an active-high reset voltage.
- Keep `out` reset-asserted high while reset input is high or `vin` is below the supply-good threshold.
- After `vin` is power-good and reset is released, wait about four rising clock updates before deasserting `out` low.
- During the release delay, `metric` may indicate partial release; after release, `metric` should be high.
- If the supply falls below threshold or reset asserts again, immediately assert `out` high and clear the release delay.
- Keep the model pure voltage-domain behavioral Verilog-A. Do not use branch-current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL regulation loops.

## Public Observables

Verification scenarios observe these scalar waveforms:

```text
clk rst vin out metric
```

Expected behavior categories:

- `reset_asserted_below_supply_threshold`
- `release_delay_after_power_good`
- `brownout_reasserts_reset`

## Output Contract

Return exactly one source artifact named `power_on_reset_detector.va`.
Do not include explanatory prose outside the source artifact contents.
