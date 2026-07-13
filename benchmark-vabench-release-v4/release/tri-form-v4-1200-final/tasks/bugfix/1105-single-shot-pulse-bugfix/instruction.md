# Single Shot Pulse Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `source_single_shot.va`: `source_single_shot`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RISING_CROSS_TRIGGER`: Each qualifying rising vin crossing through vtrans initiates an output pulse.
- `P_NO_FALLING_TRIGGER`: Falling vin crossings do not initiate pulses.
- `P_PULSE_WIDTH`: After a qualifying trigger, the output target remains high for pulse_width before returning low.
- `P_OUTPUT_LEVELS`: The deasserted and asserted targets are vlogic_low and vlogic_high respectively.
- `P_REPEATABLE_ONE_SHOTS`: Distinct qualifying rising edges produce corresponding pulses and vout returns low between sufficiently separated events.
- `P_TRANSITION_TIMING`: Output changes use tdel delay with trise and tfall smoothing without altering the logical pulse duration contract.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `source_single_shot.va`.
Every supplied `.va` file is editable; do not add or omit files.
