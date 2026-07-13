# Soft Hysteretic Limiter Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Soft Hysteretic Limiter` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_NEUTRAL`: Initialization or active reset sets out and metric to 0.45 V and clears the remembered hysteresis offset.
- `P_HYSTERESIS_STATE_UPDATE`: On rising clk crossings, vin above 0.62 V stores +hys_step, vin below 0.38 V stores -hys_step, and vin within the middle band preserves the prior offset.
- `P_GAINED_LIMITER_TRANSFER`: The held output target is 0.45 V plus gain times vin minus 0.45 V plus the remembered hysteresis offset.
- `P_OUTPUT_LIMITS`: Out is clamped to 0.10 V through 0.82 V with finite transition smoothing.
- `P_STATE_METRIC`: Metric equals 0.45 V plus twice the remembered offset, producing 0.61 V and 0.29 V for the default high- and low-memory states.

The required trace names are: `time`, `clk`, `rst`, `vin`, `out`, `metric`.

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
