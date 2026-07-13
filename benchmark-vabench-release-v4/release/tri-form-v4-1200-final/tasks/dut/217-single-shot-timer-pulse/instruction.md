# Single Shot Timer Pulse

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `single_shot_timer_pulse.va`: `single_shot_timer_pulse`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DETECT_RISING_VIN_CROSSINGS_AT_VTRANS`: Detect rising `vin` crossings at `vtrans`.
- `P_ON_EACH_QUALIFYING_RISING_EDGE_DRIVE`: On each qualifying rising edge, drive `vout` high after the configured transition delay.
- `P_USE_A_TIMER_TO_SCHEDULE_THE`: Use a timer to schedule the low-going state update at `edge_time + pulse_width + trise`, where `edge_time` is the qualifying rising input edge time. The voltage contribution still uses the public `tdel`, `trise`, and `tfall` transition parameters.
- `P_GENERATE_ONE_OUTPUT_PULSE_PER_INPUT`: Generate one output pulse per input rising edge.
- `P_HOLD_THE_LOW_OUTPUT_LEVEL_BETWEEN`: Hold the low output level between pulses.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `single_shot_timer_pulse.va`.
Do not add or omit artifacts.
