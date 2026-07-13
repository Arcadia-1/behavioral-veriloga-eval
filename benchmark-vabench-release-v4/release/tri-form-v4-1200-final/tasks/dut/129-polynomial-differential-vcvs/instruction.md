# Polynomial Differential VCVS

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `polynomial_differential_vcvs.va`: `polynomial_differential_vcvs`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_POLYNOMIAL_DIFFERENTIAL_INPUT`: Compute the polynomial from `vid = V(inp, inn)` using coefficients `a1`, `a2`, `a3`, `a5`, and `a7` through seventh order.
- `P_HALF_SWING_SPLIT`: Divide the polynomial result by two and drive `outp = vcmo + limited_vod`, `outn = vcmo - limited_vod`.
- `P_SYMMETRIC_SATURATION`: Limit the half-swing to the inclusive interval `[-vsat, vsat]` before driving both outputs.
- `P_OUTPUT_COMMON_MODE`: Keep both outputs symmetric around the common-mode parameter `vcmo`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `polynomial_differential_vcvs.va`.
Do not add or omit artifacts.
