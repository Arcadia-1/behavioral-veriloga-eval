# PAM4 Transmitter Driver Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `PAM4 Transmitter Driver` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_CLEAR`: Reset clears mapped level, transition delta, and output drive.
- `P_GRAY_LEVEL_MAP`: The input bits map to levels 0, 1, 2, 3 in the declared Gray order.
- `P_LEVEL_DAC`: The mapped level selects the corresponding level-step voltage.
- `P_PREEMPHASIS`: Enabled pre-emphasis follows the sign of the symbol-to-symbol mapped-level transition.
- `P_OUTPUT_CLAMP`: The driven output remains between VSS and VDD.

The required trace names are: `time`, `bit_msb`, `bit_lsb`, `clk`, `rst`, `emph_en`, `vout`, `level_1`, `level_0`, `delta_dbg`.

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
