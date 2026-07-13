# Safe Analog Divider Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Safe Analog Divider` DUT. The evaluator runs the same submitted bytes
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

- `P_USE_V_SIGDENOM_DIRECTLY_WHEN_ITS`: For denominator magnitudes at least `min_sigdenom`, use `V(sigdenom)` directly in the divider transfer.
- `P_WHEN_V_SIGDENOM_IS_POSITIVE_BUT`: For positive denominator magnitudes below `min_sigdenom`, use `+min_sigdenom` as the guarded denominator.
- `P_WHEN_V_SIGDENOM_IS_EXACTLY_ZERO`: For exactly zero denominator, use `+min_sigdenom` as the guarded denominator.
- `P_WHEN_V_SIGDENOM_IS_NEGATIVE_BUT`: For negative denominator magnitudes below `min_sigdenom`, use `-min_sigdenom` as the guarded denominator.
- `P_DRIVE_SIGOUT_TO_GAIN_V_SIGNUMER`: Drive `sigout` to the observable transfer `gain * V(signumer) / guarded_denominator`.

The required trace names are: `time`, `signumer`, `sigdenom`, `sigout`.

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
