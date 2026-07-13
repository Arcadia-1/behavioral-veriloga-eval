# Attenuator Gain

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `attenuator_gain.va`: `attenuator_gain`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ZERO_DB_UNITY`: With attenuation set to 0 dB, vout continuously equals vin.
- `P_DB_AMPLITUDE_RATIO`: For positive attenuation, the vout-to-vin amplitude ratio follows the standard voltage decibel attenuation relationship.
- `P_POLARITY_PRESERVATION`: The attenuator preserves input polarity and introduces no inversion or offset.
- `P_MONOTONIC_ATTENUATION`: For a fixed nonzero vin magnitude, increasing the nonnegative attenuation parameter cannot increase the magnitude of vout.
- `P_CONTINUOUS_RESPONSE`: vout is a continuous memoryless scaled version of vin without clocking, retained state, clipping, or added delay.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `attenuator_gain.va`.
Do not add or omit artifacts.
