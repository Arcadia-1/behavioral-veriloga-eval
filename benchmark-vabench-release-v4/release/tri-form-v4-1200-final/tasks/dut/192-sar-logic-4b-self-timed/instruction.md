# SAR Logic 4b Self Timed

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sar_logic_4b_self_timed.va`: `sar_logic_4b_self_timed`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_INITIALIZES_SELF_TIMED_STATE`: Initialization and rising `rst` reset the conversion step, clear `cmpck/dout`, and initialize DAC bottom-plate controls.
- `P_COMPARATOR_PULSE_DECISION_POLARITY`: Rising `dcmpp` or `dcmpn` pulses store comparator decisions with the declared polarity.
- `P_STEP_ADVANCE_ON_COMPARATOR_FALL`: Comparator-output falling events advance the SAR step and update the next control state.
- `P_CMPCK_TIMING_AND_LEVEL`: `cmpck` is scheduled low after `t_logic_delay` and driven with valid voltage-coded levels.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sar_logic_4b_self_timed.va`.
Do not add or omit artifacts.
