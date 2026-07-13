# Configurable Pulse Train Generator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `configurable_pulse_train.va`: `configurable_pulse_train`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_IDLE_CAPTURE`: A sampled high start while idle captures unsigned period3:period0, width3:width0, and count3:count0 on a rising clk crossing.
- `P_ZERO_CODE_MINIMUM`: A zero-coded period, width, or count is interpreted as one clock sample rather than zero.
- `P_PULSE_COUNT`: Each accepted command emits exactly the captured count number of pulses.
- `P_WIDTH_AND_PERIOD`: Each pulse remains high for the captured width in clock samples and pulse starts are separated by the captured period in clock samples.
- `P_COMPLETION`: After the final pulse completes, pulse is low and done is asserted.
- `P_OUTPUT_LEVELS`: pulse and done use 0 V and vdd levels with finite transition smoothing set by tr.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `configurable_pulse_train.va`.
Every supplied `.va` file is editable; do not add or omit files.
