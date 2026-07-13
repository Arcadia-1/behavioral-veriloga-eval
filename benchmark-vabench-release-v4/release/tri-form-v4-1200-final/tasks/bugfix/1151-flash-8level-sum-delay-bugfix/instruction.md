# Flash 8level Sum Delay Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `flash_8level_sum_delay.va`: `flash_8level_sum_delay`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLOCKED_FLASH_THRESHOLD_SUM`: Each rising `clks` crossing compares `V(vip,vim)` against the symmetric flash thresholds and updates `doutsum`.
- `P_REFERENCE_SCALING`: The flash thresholds use `V(refp)-V(refn)` multiplied by `ref_scaling`.
- `P_ONE_CYCLE_DELAYED_SUM`: `doutsumdelay` reports the previous sampled flash summary, not the current summary.
- `P_NORMALIZED_OUTPUT`: The flash summary is normalized by the eight-level count before being driven.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `flash_8level_sum_delay.va`.
Every supplied `.va` file is editable; do not add or omit files.
