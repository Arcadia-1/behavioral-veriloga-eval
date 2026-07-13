# Pipeline ADC Stage Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Pipeline ADC Stage` DUT. The evaluator runs the same submitted bytes
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

- `P_TWO_PHASE_SAMPLING`: VIN is sampled on a rising PHI1 edge and converted on a rising PHI2 edge.
- `P_SUBADC_REGIONS`: Upper, middle, and lower sampled-input regions produce decision codes 10, 01, and 00 respectively.
- `P_RESIDUE_MAPPING`: The residue is gain-two with the specified half-reference subtraction, no offset, or addition for the three regions.
- `P_RESIDUE_CLAMP`: VRES remains within the VSS-to-VDD supply range.

The required trace names are: `time`, `phi1`, `phi2`, `vin`, `vref`, `vres`, `d1`, `d0`, `vdd`, `vss`.

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
