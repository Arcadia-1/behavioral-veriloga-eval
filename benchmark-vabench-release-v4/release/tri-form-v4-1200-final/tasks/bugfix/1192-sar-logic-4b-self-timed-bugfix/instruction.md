# SAR Logic 4b Self Timed Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sar_logic_4b_self_timed.va`: `sar_logic_4b_self_timed`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_INITIALIZES_SELF_TIMED_STATE`: Initialization and rising `rst` reset the conversion step, clear `cmpck/dout`, and initialize DAC bottom-plate controls.
- `P_COMPARATOR_PULSE_DECISION_POLARITY`: Rising `dcmpp` or `dcmpn` pulses store comparator decisions with the declared polarity.
- `P_STEP_ADVANCE_ON_COMPARATOR_FALL`: Comparator-output falling events advance the SAR step and update the next control state.
- `P_CMPCK_TIMING_AND_LEVEL`: `cmpck` is scheduled low after `t_logic_delay` and driven with valid voltage-coded levels.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sar_logic_4b_self_timed.va`.
Every supplied `.va` file is editable; do not add or omit files.
