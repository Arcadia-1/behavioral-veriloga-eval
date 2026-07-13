# Single Shot Pulse Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Single Shot Pulse` DUT. The evaluator runs the same submitted bytes
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

- `P_RISING_CROSS_TRIGGER`: Each qualifying rising vin crossing through vtrans initiates an output pulse.
- `P_NO_FALLING_TRIGGER`: Falling vin crossings do not initiate pulses.
- `P_PULSE_WIDTH`: After a qualifying trigger, the output target remains high for pulse_width before returning low.
- `P_OUTPUT_LEVELS`: The deasserted and asserted targets are vlogic_low and vlogic_high respectively.
- `P_REPEATABLE_ONE_SHOTS`: Distinct qualifying rising edges produce corresponding pulses and vout returns low between sufficiently separated events.
- `P_TRANSITION_TIMING`: Output changes use tdel delay with trise and tfall smoothing without altering the logical pulse duration contract.

The required trace names are: `time`, `vin`, `vout`.

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
