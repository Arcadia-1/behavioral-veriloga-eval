# I/Q Upconversion Mixer Chain Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `I/Q Upconversion Mixer Chain` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation drives RF and debug outputs to vcm and clears quad_ok.
- `P_IQ_SIGNED_MIXING`: I and Q debug outputs equal vcm plus the specified signed LO products, including the negative Q-path convention.
- `P_RF_SUM_CLAMP`: rf_out equals the bounded sum of the I and Q path contributions about vcm.
- `P_QUADRATURE_ACTIVITY`: quad_ok asserts only after each LO input has crossed threshold since the latest reset or enable event.

The required trace names are: `time`, `i_in`, `q_in`, `lo_i`, `lo_q`, `rst`, `enable`, `rf_out`, `i_mix_dbg`, `q_mix_dbg`, `quad_ok`.

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
