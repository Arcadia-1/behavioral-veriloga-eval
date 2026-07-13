# LNA Blocker Compression Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `lna_blocker_compression_detector.va`: `lna_blocker_compression_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive output to `vcm` and clear compression outputs.
- `P_AMPLIFY_VIN_VCM_WITH_SMALL_SIGNAL`: Amplify `vin - vcm` with small-signal gain when `blocker` is low.
- `P_REDUCE_EFFECTIVE_GAIN_AS_BLOCKER_RISES`: Reduce effective gain as `blocker` rises above `blocker_start`.
- `P_EXPOSE_GAIN_REDUCTION_ON_COMPRESSION_METRIC`: Expose gain reduction on `compression_metric`.
- `P_ASSERT_COMPRESSED_ONLY_WHEN_THE_EFFECTIVE`: Assert `compressed` only when the effective gain is reduced by more than `compression_tol`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `lna_blocker_compression_detector.va`.
Do not add or omit artifacts.
