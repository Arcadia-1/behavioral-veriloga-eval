# Crossing Pulse Detector Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Crossing Pulse Detector` DUT. The evaluator runs the same submitted bytes
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

- `P_RISING_CROSS_PULSE`: A rising sigin crossing through sigcrossing initiates a sigout pulse.
- `P_FALLING_CROSS_PULSE`: A falling sigin crossing through sigcrossing also initiates a sigout pulse.
- `P_PULSE_WIDTH`: After each qualifying crossing, the output target remains at vlogic_high for pulse_width before returning to vlogic_low.
- `P_LOW_BETWEEN_EVENTS`: Sigout returns to vlogic_low between sufficiently separated threshold crossings.
- `P_REPEATABLE_BIDIRECTIONAL_EVENTS`: Alternating rising and falling crossings each produce corresponding pulses rather than only the first event or one polarity.
- `P_TRANSITION_TIMING`: Sigout changes use tdel delay with trise and tfall smoothing.

The required trace names are: `time`, `sigin`, `sigout`.

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
