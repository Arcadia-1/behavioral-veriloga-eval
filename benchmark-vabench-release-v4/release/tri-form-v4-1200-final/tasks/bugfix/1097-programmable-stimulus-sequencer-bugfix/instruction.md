# Programmable Stimulus Sequencer Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `programmable_stimulus_sequencer.va`: `programmable_stimulus_sequencer`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_IDLE`: When rst is above the 0.45 V control threshold, out is held near 0.45 V and metric is low.
- `P_RAMP_MODE`: For mode below 0.30 V outside reset, out produces a monotonic ramp segment from about 0.18 V toward 0.45 V and metric is near 0.20 V.
- `P_CHIRP_MODE`: For mode from 0.30 V through below 0.60 V, out is a sine segment centered near 0.45 V whose instantaneous frequency increases over the segment, with metric near 0.50 V.
- `P_BURST_GATE`: For mode at or above 0.60 V and gate high, out produces a deterministic PRBS-like burst between the low and high stimulus levels.
- `P_BURST_IDLE`: In burst mode with gate low, out returns near 0.45 V and metric reports the idle rather than active-burst status.
- `P_CONTROL_DRIVEN_SELECTION`: Mode and gate behavior follows the voltage-coded inputs over arbitrary legal control schedules rather than a fixed stimulus timeline.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `programmable_stimulus_sequencer.va`.
Every supplied `.va` file is editable; do not add or omit files.
