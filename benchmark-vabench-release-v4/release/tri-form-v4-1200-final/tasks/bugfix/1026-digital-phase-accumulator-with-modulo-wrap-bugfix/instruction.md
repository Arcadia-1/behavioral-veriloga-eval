# Digital Phase Accumulator With Modulo Wrap Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `phase_accumulator_timer_wrap_ref.va`: `phase_accumulator_timer_wrap_ref`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_TIMER_INCREMENT`: On every dt timer event, normalized phase advances by phase_step.
- `P_MODULO_WRAP`: The phase state wraps modulo one and never grows unbounded.
- `P_PHASE_RAIL_SCALING`: Phase_out equals wrapped normalized phase scaled by the local VDD-minus-VSS rail span.
- `P_PHASE_DERIVED_CLOCK`: Clk_out is rail-high while normalized phase is below 0.5 and low while phase is at or above 0.5.
- `P_PARAMETERIZED_PERIOD`: Changing dt or phase_step changes the observable phase and clock cadence according to the same update and wrap rules.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `phase_accumulator_timer_wrap_ref.va`.
Every supplied `.va` file is editable; do not add or omit files.
