# Reference Startup Enable Flow

## Task Contract

- Form: `dut`
- Level: `L2`
- Category: Bias Reference and Power Management
- Target artifact: `reference_startup_enable_flow.va`
- Implement only the requested Verilog-A flow DUT. Do not generate a Spectre testbench, checker logic, or auxiliary test hooks.
- Preserve the public module name, port order, starter parameters, and saved waveform observable names.
- The visible testbench is a public smoke scenario. Use it to understand wiring and observables, but do not hard-code its stop time, maxstep, or exact waveform breakpoints into the DUT behavior.

## Public Verilog-A Interface

```verilog
module reference_startup_enable_flow(clk, rst, vdd_in, en, out, metric, supply_ok, enable_mon, state_mon, startup_mon);
input clk, rst, vdd_in, en;
output out, metric, supply_ok, enable_mon, state_mon, startup_mon;
electrical clk, rst, vdd_in, en, out, metric, supply_ok, enable_mon, state_mon, startup_mon;
```

Starter parameter declarations are part of the public contract:

- `tr = 100p`: output transition rise/fall time.
- `vth = 0.45`: voltage-coded logic threshold.

## Public Behavioral Contract

- `clk`, `rst`, and `en` are voltage-coded logic signals.
- `vdd_in` is the monitored supply waveform for the reference-startup flow.
- `supply_ok` should expose supply-good detection.
- `enable_mon` should expose the enable latch/command state.
- `state_mon` should expose the off, disabled, startup, and valid flow states as bounded voltage-coded monitor levels.
- `startup_mon` should expose bounded startup progress.
- Hold `out` low when reset is active, supply is not good, or enable is low.
- Once supply is good and enable is asserted, start the reference gradually toward a settled value near 0.55 V.
- Drive `metric` high only after the reference has settled to a valid state.
- A supply dip should reset valid status and startup progress; after the supply returns and enable remains asserted, the flow should recover.
- Keep the model pure voltage-domain behavioral Verilog-A. Do not use branch-current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL regulation loops.

## Public Observables

Verification scenarios observe these scalar waveforms:

```text
clk rst vdd_in en out metric supply_ok enable_mon state_mon startup_mon
```

Expected behavior categories:

- `supply_good_and_enable_monitors_are_visible`
- `pre_enable_reference_is_held_low`
- `enabled_reference_startup_settles`
- `startup_progress_and_state_transition_visible`
- `supply_dip_resets_valid_status`
- `state_and_valid_status_recover_after_supply_return`

## Output Contract

Return exactly one source artifact named `reference_startup_enable_flow.va`.
Do not include explanatory prose outside the source artifact contents.
