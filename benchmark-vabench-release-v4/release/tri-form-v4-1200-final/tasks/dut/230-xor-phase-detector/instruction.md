# XOR Phase Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `xor_phase_detector.va`: `xor_phase_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INTERPRET_REF_AND_FB_LOGIC_LEVELS`: Interpret `ref` and `fb` logic levels using a threshold of `vdd/2`.
- `P_DRIVE_UP_HIGH_WHEN_THE_INTERPRETED`: Drive `up` high when the interpreted `ref` and `fb` levels differ.
- `P_DRIVE_DOWN_HIGH_WHEN_THE_INTERPRETED`: Drive `down` high when the interpreted `ref` and `fb` levels match.
- `P_UPDATE_OUTPUTS_COMBINATIONALLY_FROM_THE_CURREN`: Update outputs combinationally from the current input voltages.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `xor_phase_detector.va`.
Do not add or omit artifacts.
