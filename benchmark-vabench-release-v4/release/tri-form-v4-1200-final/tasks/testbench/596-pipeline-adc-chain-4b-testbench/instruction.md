# Pipeline ADC Chain 4b Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Pipeline ADC Chain 4b` DUT. The evaluator runs the same submitted bytes
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

- `P_CLOCKED_SAMPLE_HOLD`: On each rising CLK crossing, the converter samples VIN and updates all stage residues and bits; outputs hold between conversions.
- `P_STAGE1_DECISION`: Stage 1 clips VIN to vrefn through vrefp, selects the correct quarter-scale bin, and exposes the two-bit coarse decision on S1B1/S1B0.
- `P_STAGE1_RESIDUE`: RES1 is four times the clipped sampled-input error from the selected stage-1 bin center, clipped to the conversion range.
- `P_STAGE2_DECISION`: Stage 2 applies the same quarter-scale two-bit decision to RES1 and exposes it on S2B1/S2B0.
- `P_STAGE2_RESIDUE`: RES2 is four times the stage-2 input error from its selected bin center, clipped to the conversion range.
- `P_FINAL_CODE_CONCATENATION`: DOUT3/DOUT2 equal the stage-1 bits and DOUT1/DOUT0 equal the stage-2 bits, using VDD for high and VSS for low.

The required trace names are: `time`, `vdd`, `vss`, `vin`, `clk`, `res1`, `res2`, `s1b1`, `s1b0`, `s2b1`, `s2b0`, `dout3`, `dout2`, `dout1`, `dout0`.

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
