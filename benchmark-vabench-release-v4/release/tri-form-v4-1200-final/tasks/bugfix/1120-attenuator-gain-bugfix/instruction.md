# Attenuator Gain Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `attenuator_gain.va`: `attenuator_gain`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ZERO_DB_UNITY`: With attenuation set to 0 dB, vout continuously equals vin.
- `P_DB_AMPLITUDE_RATIO`: For positive attenuation, the vout-to-vin amplitude ratio follows the standard voltage decibel attenuation relationship.
- `P_POLARITY_PRESERVATION`: The attenuator preserves input polarity and introduces no inversion or offset.
- `P_MONOTONIC_ATTENUATION`: For a fixed nonzero vin magnitude, increasing the nonnegative attenuation parameter cannot increase the magnitude of vout.
- `P_CONTINUOUS_RESPONSE`: vout is a continuous memoryless scaled version of vin without clocking, retained state, clipping, or added delay.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `attenuator_gain.va`.
Every supplied `.va` file is editable; do not add or omit files.
