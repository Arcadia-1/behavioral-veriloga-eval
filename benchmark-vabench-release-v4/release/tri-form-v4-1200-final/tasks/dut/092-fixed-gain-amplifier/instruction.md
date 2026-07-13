# Fixed Gain Amplifier

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `gain_amp_fixed.va`: `gain_amp_fixed`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DIFFERENTIAL_GAIN`: The output differential equals ACTUAL_GAIN times the input differential.
- `P_POSITIVE_POLARITY`: A positive input differential produces a positive output differential and a negative input differential produces a negative output differential.
- `P_OUTPUT_COMMON_MODE`: The output pair remains centered at vdd/2 independently of input common mode.
- `P_SYMMETRIC_OUTPUT_PAIR`: Half the amplified differential is added to VOUT_P and half is subtracted from VOUT_N.
- `P_PARAMETER_OVERRIDES`: Legal ACTUAL_GAIN and vdd overrides alter differential gain and output common mode according to their declared meanings.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `gain_amp_fixed.va`.
Do not add or omit artifacts.
