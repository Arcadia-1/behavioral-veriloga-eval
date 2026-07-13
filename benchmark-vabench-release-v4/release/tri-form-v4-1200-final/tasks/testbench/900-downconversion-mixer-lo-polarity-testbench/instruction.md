# Downconversion Mixer with LO Polarity Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Downconversion Mixer with LO Polarity` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CENTER`: Reset or disable centers I/Q outputs and clears LO metrics and polarity_ok.
- `P_LO_POLARITY_METRICS`: Each LO threshold state selects signed polarity and is mirrored by its public metric.
- `P_IQ_CONVERSION`: I and Q outputs follow the declared common-mode referenced conversion-gain equations with independent LO signs.
- `P_OUTPUT_CLAMP`: Both baseband outputs remain within the declared supply rails.
- `P_POLARITY_QUALIFICATION`: polarity_ok asserts only after both LO controls have toggled while enabled.

The required trace names are: `time`, `rf_in`, `lo_i`, `lo_q`, `rst`, `enable`, `i_out`, `q_out`, `lo_i_metric`, `lo_q_metric`, `polarity_ok`.

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
