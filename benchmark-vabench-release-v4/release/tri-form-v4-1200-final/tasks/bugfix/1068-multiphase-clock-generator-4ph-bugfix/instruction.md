# Multiphase Clock Generator 4ph Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `multiphase_clock_generator_4ph.va`: `multiphase_clock_generator_4ph`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_PERIOD`: Each output repeats with a 20 ns period.
- `P_DUTY_CYCLE`: Each output has approximately 50 percent duty cycle.
- `P_PHASE_OFFSETS`: Relative to clk0, corresponding rising edges of clk90, clk180, and clk270 lag by 5 ns, 10 ns, and 15 ns respectively.
- `P_PHASE_STABILITY`: The output phase ordering and offsets remain stable across repeated periods.
- `P_OUTPUT_LEVELS`: All clocks use 0 V and vdd levels with finite transition smoothing set by tr.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `multiphase_clock_generator_4ph.va`.
Every supplied `.va` file is editable; do not add or omit files.
