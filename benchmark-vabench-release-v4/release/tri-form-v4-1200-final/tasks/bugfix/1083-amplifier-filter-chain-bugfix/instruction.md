# Amplifier Filter Chain Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `amplifier_filter_chain.va`: `amplifier_filter_chain`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_COMMON_MODE`: Initialization or active-high reset returns the preamp and both filter stages near 0.45 V and leaves settle_metric low.
- `P_BOUNDED_PREAMP`: At each rising clock edge, preamp_mon and metric equal gain times the sampled vin deviation about 0.45 V, clamped to 0 V through 0.9 V.
- `P_FIRST_FILTER_STAGE`: Filt1_mon applies the sampled first-order alpha update toward the bounded preamp target.
- `P_SECOND_FILTER_STAGE`: Filt2_mon applies a second sampled alpha update toward the newly updated first-stage value, and out follows filt2_mon.
- `P_CASCADE_LAG`: After a large input change, the second-stage output visibly lags the bounded preamp target while the two stage monitors preserve cascade order.
- `P_SETTLE_STATUS`: Settle_metric is 0.9 V when the output-target error is below 0.16 V and 0.1 V while the chain is recovering.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `amplifier_filter_chain.va`.
Every supplied `.va` file is editable; do not add or omit files.
