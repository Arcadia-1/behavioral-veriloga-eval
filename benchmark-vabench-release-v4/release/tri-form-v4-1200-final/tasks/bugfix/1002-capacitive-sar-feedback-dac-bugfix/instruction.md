# Capacitive Weighted SAR Feedback DAC Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cdac_cal.va`: `cdac_cal`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLOCKED_HOLD`: The DAC samples code and calibration inputs on rising CLK edges and holds the resulting output between edges.
- `P_CODE_MONOTONICITY`: Increasing effective code increases VDAC_P minus VDAC_N.
- `P_CALIBRATION_WEIGHT`: CAL0 contributes one calibration unit, CAL1 contributes two, and each unit offsets the main code by 32 codes.
- `P_DIFFERENTIAL_COMMON_MODE`: VDAC_P and VDAC_N are complementary about vcm.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cdac_cal.va`.
Every supplied `.va` file is editable; do not add or omit files.
