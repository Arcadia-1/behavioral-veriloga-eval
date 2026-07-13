# SARFEND Logic 4b Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `SARFEND Logic 4b` DUT. The evaluator runs the same submitted bytes
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

- `P_CONVERSION_RESET_AND_PREVIOUS_WORD`: Each rising `clks` crossing publishes the previous DAC-P word on `dout0..dout3`, resets the conversion pointer, and initializes controls for a new conversion.
- `P_SAMPLE_AND_COMPARATOR_DECISIONS`: The conversion captures comparator inputs and updates SAR decisions with the declared `dcomp/dcompb` polarity.
- `P_TEST_OVERRIDE_BEHAVIOR`: The public test override controls the DAC/control outputs when asserted and does not corrupt normal conversion state.
- `P_DOUT_BIT_MAPPING`: `dout0..dout3` preserve the declared bit order of the previous DAC-P state.
- `P_LOGIC_OUTPUT_LEVELS`: Handshake, DAC-control, and data outputs use full voltage-coded low/high levels.

The required trace names are: `time`, `clkc`, `clks`, `dcomp`, `dcompb`, `dm1`, `dm2`, `dm3`, `dm4`, `dout0`, `dout1`, `dout2`, `dout3`, `dp1`, `dp2`, `dp3`, `dp4`, `dtest0`, `dtest1`, `dtest2`, `dtest3`, `test`.

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
