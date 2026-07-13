# Single Shot Timer Pulse Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `single_shot_timer_pulse.va`: `single_shot_timer_pulse`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_DETECT_RISING_VIN_CROSSINGS_AT_VTRANS`: Detect rising `vin` crossings at `vtrans`.
- `P_ON_EACH_QUALIFYING_RISING_EDGE_DRIVE`: On each qualifying rising edge, drive `vout` high after the configured transition delay.
- `P_USE_A_TIMER_TO_SCHEDULE_THE`: Use a timer to schedule the low-going state update at `edge_time + pulse_width + trise`, where `edge_time` is the qualifying rising input edge time. The voltage contribution still uses the public `tdel`, `trise`, and `tfall` transition parameters.
- `P_GENERATE_ONE_OUTPUT_PULSE_PER_INPUT`: Generate one output pulse per input rising edge.
- `P_HOLD_THE_LOW_OUTPUT_LEVEL_BETWEEN`: Hold the low output level between pulses.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `single_shot_timer_pulse.va`.
Every supplied `.va` file is editable; do not add or omit files.
