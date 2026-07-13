# LFSR PRBS Generator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `LFSR PRBS Generator` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_SEED`: When rst_n is below vth, the exposed seven-bit state is loaded from seed[6:0]; legal seed overrides are integers 0 through 127 inclusive, and seed 0 is remapped to 7'b0000001 to avoid the LFSR lock-up state.
- `P_ENABLE_GATING`: On rising clk crossings, the state advances only when rst_n and en are both above vth; otherwise it holds or resets as applicable.
- `P_FEEDBACK_POLYNOMIAL`: Each enabled update sets next state_0 to previous state_6 XOR previous state_5, implementing x^7 + x^6 + 1.
- `P_SHIFT_SEQUENCE`: Each enabled update sets next state_i to previous state_(i-1) for i from 1 through 6.
- `P_SERIAL_OUTPUT`: serial_out always represents the current state_6 bit.
- `P_OUTPUT_LEVELS`: serial_out and every state output use 0 V and vdd levels with delay td and transition smoothing trf.

The required trace names are: `time`, `clk`, `rst_n`, `en`, `serial_out`, `state_0`, `state_1`, `state_2`, `state_3`, `state_4`, `state_5`, `state_6`.

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
