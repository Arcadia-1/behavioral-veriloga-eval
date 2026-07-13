# Single Shot Pulse

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `source_single_shot.va`: `source_single_shot`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RISING_CROSS_TRIGGER`: Each qualifying rising vin crossing through vtrans initiates an output pulse.
- `P_NO_FALLING_TRIGGER`: Falling vin crossings do not initiate pulses.
- `P_PULSE_WIDTH`: After a qualifying trigger, the output target remains high for pulse_width before returning low.
- `P_OUTPUT_LEVELS`: The deasserted and asserted targets are vlogic_low and vlogic_high respectively.
- `P_REPEATABLE_ONE_SHOTS`: Distinct qualifying rising edges produce corresponding pulses and vout returns low between sufficiently separated events.
- `P_TRANSITION_TIMING`: Output changes use tdel delay with trise and tfall smoothing without altering the logical pulse duration contract.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `source_single_shot.va`.
Do not add or omit artifacts.
