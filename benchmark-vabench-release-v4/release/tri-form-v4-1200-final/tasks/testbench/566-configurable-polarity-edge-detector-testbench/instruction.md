# Configurable Polarity Edge Detector Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Configurable Polarity Edge Detector` DUT. The evaluator runs the same submitted bytes
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

- `P_RISING_SELECTION`: When rise_en is above vth, each rising crossing of sig through vth produces one output pulse.
- `P_FALLING_SELECTION`: When rise_en is below vth, each falling crossing of sig through vth produces one output pulse.
- `P_OPPOSITE_EDGE_REJECTION`: An edge opposite to the polarity selected by rise_en does not produce a pulse.
- `P_BOUNDED_PULSE`: Each detected edge produces a bounded short pulse with nominal width about 2 ns rather than a latched high level.
- `P_OUTPUT_LEVELS`: pulse uses 0 V and vdd levels with finite transition smoothing set by tr.

The required trace names are: `time`, `sig`, `rise_en`, `pulse`.

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
