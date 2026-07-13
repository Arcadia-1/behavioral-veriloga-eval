# AGC Receiver Leveling Loop Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `AGC Receiver Leveling Loop` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_STATE`: Active-high reset restores out to 0.45 V, clears rssi_mon and metric, and represents the initial gain 2.2 on gain_mon.
- `P_CLOCKED_GAIN_LOOP`: The AGC samples and updates its held output and gain state only on rising clk crossings after reset releases.
- `P_OUTPUT_ENVELOPE`: Out is the current-gain amplification of vin about 0.45 V, clamped to 0.02 V through 0.88 V, and rssi_mon reports the normalized absolute output envelope.
- `P_GAIN_DIRECTION_AND_BOUNDS`: Envelope above target_amp plus deadband lowers gain by 0.18, envelope below target_amp minus deadband raises gain by 0.10, and gain remains in 0.45 through 3.0.
- `P_DEADBAND_HOLD`: When the observed envelope lies within the target deadband, the bounded gain state holds across the update.
- `P_SETTLING_METRIC`: Metric decreases with absolute envelope error from target_amp according to the public scaling and remains clamped to 0 V through 0.9 V.

The required trace names are: `time`, `clk`, `rst`, `vin`, `out`, `metric`, `gain_mon`, `rssi_mon`.

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
