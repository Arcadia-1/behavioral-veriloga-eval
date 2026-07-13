# Charge-pump Voltage Multiplier Controller Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `phase_generator.va`: `phase_generator`
- `pump_stage_model.va`: `pump_stage_model`
- `regulation_comparator.va`: `regulation_comparator`
- `voltage_multiplier_top.va`: `voltage_multiplier_top`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset clears vout, pump control, readiness, and regulation state; disabled operation suppresses pumping.
- `P_NONOVERLAP_PHASES`: Enabled clock updates alternate phase_a and phase_b while never asserting both phases together.
- `P_PUMP_REGULATION`: While pump_en is active, enabled phase updates raise vout in bounded pump steps; without pumping, vout leaks downward and remains within rails.
- `P_ERROR_REPORTING`: regulation_error continuously reports target minus vout and pump_en requests pumping below the lower tolerance boundary.
- `P_READY_QUALIFICATION`: Ready asserts only after three consecutive enabled clock updates within the regulation tolerance and clears outside qualification.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `phase_generator.va`, `pump_stage_model.va`, `regulation_comparator.va`, `voltage_multiplier_top.va`.
Every supplied `.va` file is editable; do not add or omit files.
