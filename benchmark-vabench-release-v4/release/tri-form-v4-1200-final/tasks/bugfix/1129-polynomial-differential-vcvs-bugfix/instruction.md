# Polynomial Differential VCVS Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `polynomial_differential_vcvs.va`: `polynomial_differential_vcvs`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_POLYNOMIAL_DIFFERENTIAL_INPUT`: Compute the polynomial from `vid = V(inp, inn)` using coefficients `a1`, `a2`, `a3`, `a5`, and `a7` through seventh order.
- `P_HALF_SWING_SPLIT`: Divide the polynomial result by two and drive `outp = vcmo + limited_vod`, `outn = vcmo - limited_vod`.
- `P_SYMMETRIC_SATURATION`: Limit the half-swing to the inclusive interval `[-vsat, vsat]` before driving both outputs.
- `P_OUTPUT_COMMON_MODE`: Keep both outputs symmetric around the common-mode parameter `vcmo`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `polynomial_differential_vcvs.va`.
Every supplied `.va` file is editable; do not add or omit files.
