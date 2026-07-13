# Resistor Ladder Monotonic Decoder

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `resistor_ladder_monotonic_decoder.va`: `resistor_ladder_monotonic_decoder`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` low, clear `step_metric`, and clear `monotonic_ok`.
- `P_DECODE_CODE_2_CODE_0_AS`: Decode `code_2..code_0` as an unsigned ladder tap index from 0 to 7.
- `P_DRIVE_VOUT_TO_THE_CORRESPONDING_EVENLY`: Drive `vout` to the corresponding evenly spaced ladder voltage between `vss` and `vdd`.
- `P_EXPOSE_ONE_LSB_STEP_ON_STEP`: Expose one LSB step on `step_metric` while enabled.
- `P_ASSERT_MONOTONIC_OK_WHEN_THE_ACTIVE`: Assert `monotonic_ok` when the active code-to-output mapping is nondecreasing.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `resistor_ladder_monotonic_decoder.va`.
Do not add or omit artifacts.
