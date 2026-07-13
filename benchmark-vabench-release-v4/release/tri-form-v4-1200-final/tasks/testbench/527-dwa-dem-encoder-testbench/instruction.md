# DWA DEM Encoder Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `DWA DEM Encoder` DUT. The evaluator runs the same submitted bytes
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

- `P_V2B_ROUND_AND_CLAMP`: On each rising helper clock crossing, vin rounds to the nearest integer and clamps to a four-bit code from 0 through 15.
- `P_ACTIVE_LOW_RESET_POINTER`: A sampled active-low reset initializes ptr to the one-hot ptr_init position.
- `P_ROTATING_POINTER_UPDATE`: Each post-reset rising edge advances the circular pointer by the sampled unsigned code modulo 16.
- `P_POINTER_ONE_HOT`: Ptr remains exactly one-hot at the updated circular pointer position.
- `P_DWA_SELECTED_MASK`: Cell_en implements the public rotating span and LSB boundary-cell rule for the sampled code, including the code-zero boundary-cell case.
- `P_SYSTEM_CODE_BINDING`: The four helper outputs feed the DWA code bus in MSB-to-LSB order without bit reversal.

The required trace names are: `time`, `clk_i`, `rst_ni`, `code_3`, `code_2`, `code_1`, `code_0`, `cell_en_15`, `cell_en_14`, `cell_en_13`, `cell_en_12`, `cell_en_11`, `cell_en_10`, `cell_en_9`, `cell_en_8`, `cell_en_7`, `cell_en_6`, `cell_en_5`, `cell_en_4`, `cell_en_3`, `cell_en_2`, `cell_en_1`, `cell_en_0`, `ptr_15`, `ptr_14`, `ptr_13`, `ptr_12`, `ptr_11`, `ptr_10`, `ptr_9`, `ptr_8`, `ptr_7`, `ptr_6`, `ptr_5`, `ptr_4`, `ptr_3`, `ptr_2`, `ptr_1`, `ptr_0`, `vin_node`.

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
