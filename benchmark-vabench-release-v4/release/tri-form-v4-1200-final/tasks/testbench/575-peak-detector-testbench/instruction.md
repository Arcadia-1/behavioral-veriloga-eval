# Peak Detector Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Peak Detector` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIAL_ZERO`: The retained peak and vout initialize to 0 V.
- `P_SAMPLED_MEASUREMENT`: When reset is inactive, vin is considered for peak updates at periodic 500 ps sample instants.
- `P_MAX_RETENTION`: At each sample, a vin value above the retained peak replaces it; lower or equal samples leave vout unchanged.
- `P_MONOTONIC_HOLD`: Between resets, the retained peak does not decrease and remains held between sample instants.
- `P_RESET_CLEAR`: While rst is above vth, the retained peak is cleared and vout returns to 0 V.
- `P_OUTPUT_SMOOTHING`: Changes of the retained peak appear on vout with finite transition smoothing set by tr.

The required trace names are: `time`, `vin`, `rst`, `vout`.

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
