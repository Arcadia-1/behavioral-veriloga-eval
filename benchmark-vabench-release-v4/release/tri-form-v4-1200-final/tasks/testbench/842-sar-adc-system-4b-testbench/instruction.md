# 4-bit SAR ADC System Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `4-bit SAR ADC System` DUT. The evaluator runs the same submitted bytes
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

- `P_SAR_RESET_CLEAR`: Reset clears conversion state, code, done, sample_dbg, and dac_dbg.
- `P_SAR_SAMPLE_HOLD`: The first rising clock edge after start captures vin and sample_dbg holds that value through conversion.
- `P_SAR_FINAL_CODE`: Four MSB-first trials quantize the held sample to the clamped unsigned 4-bit SAR code.
- `P_SAR_DAC_TRIAL`: dac_dbg exposes vref times the active trial code divided by 16 and settles to the final-code DAC level.

The required trace names are: `time`, `vin`, `clk`, `rst`, `start`, `code_3`, `code_2`, `code_1`, `code_0`, `done`, `sample_dbg`, `dac_dbg`.

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
