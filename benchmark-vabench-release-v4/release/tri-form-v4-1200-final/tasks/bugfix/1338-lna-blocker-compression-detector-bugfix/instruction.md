# LNA Blocker Compression Detector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `lna_blocker_compression_detector.va`: `lna_blocker_compression_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive output to `vcm` and clear compression outputs.
- `P_AMPLIFY_VIN_VCM_WITH_SMALL_SIGNAL`: Amplify `vin - vcm` with small-signal gain when `blocker` is low.
- `P_REDUCE_EFFECTIVE_GAIN_AS_BLOCKER_RISES`: Reduce effective gain as `blocker` rises above `blocker_start`.
- `P_EXPOSE_GAIN_REDUCTION_ON_COMPRESSION_METRIC`: Expose gain reduction on `compression_metric`.
- `P_ASSERT_COMPRESSED_ONLY_WHEN_THE_EFFECTIVE`: Assert `compressed` only when the effective gain is reduced by more than `compression_tol`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `lna_blocker_compression_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
