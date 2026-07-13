# Cyclic Decoder 10b Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Cyclic Decoder 10b` DUT. The evaluator runs the same submitted bytes
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

- `P_READY_SERIAL_CAPTURE`: After each publication clock, rising `ready` crossings collect up to `nbit` serial decisions MSB first.
- `P_TERNARY_WEIGHTING`: For each collected decision, high `dp` adds the full current binary weight and low `dp` with high `dn` adds half of that weight.
- `P_NORMALIZED_MIDSCALE_OUTPUT`: The decoded value is normalized by the public bit depth and shifted by the required midscale offset before driving `dout`.
- `P_CLOCKED_PUBLICATION_HOLD`: `dout` updates from event-driven ready/publication handling and holds between publication events.

The required trace names are: `time`, `dp`, `dn`, `ready`, `clks`, `dout`.

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
