# Muxed Track-hold Array Readout Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Muxed Track-hold Array Readout` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

The exact read-only source paths, modules, ports, instance names, and ordered
terminal bindings are declared in `solver_contract.json`.

## Public Parameter Contract

Honor the public parameter declarations in `solver_contract.json` when choosing
stimulus and coverage.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_ON_RESET_CLEAR_ALL_HELD_CHANNEL`: On reset, clear all held channel states, output, channel metric, and `valid`.
- `P_ON_EACH_ENABLED_SAMPLING_CLOCK_EDGE`: On each enabled sampling clock edge, capture all three input channels into separate hold states.
- `P_DECODE_SEL_1_SEL_0_AND`: Decode `sel_1..sel_0` and route the selected held channel to `vout`; invalid code 3 must hold the previous output and clear `valid`.
- `P_EXPOSE_THE_SELECTED_CHANNEL_INDEX_ON`: Expose the selected channel index on `channel_metric` as a voltage-coded metric.
- `P_HOLD_ALL_CHANNEL_SAMPLES_BETWEEN_SAMPLING`: Hold all channel samples between sampling events.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

The required trace names are: `time`, `vin0`, `vin1`, `vin2`, `clk`, `rst`, `sel_1`, `sel_0`, `sample_en`, `vout`, `channel_metric`, `valid`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the exact declared testbench include paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Respect every public resource limit in `solver_contract.json`.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one submission-root-relative artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
