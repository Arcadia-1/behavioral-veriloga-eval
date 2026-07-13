# Charge-pump Voltage Multiplier Controller

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `phase_generator.va`: `phase_generator`
- `pump_stage_model.va`: `pump_stage_model`
- `regulation_comparator.va`: `regulation_comparator`
- `voltage_multiplier_top.va`: `voltage_multiplier_top`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset clears vout, pump control, readiness, and regulation state; disabled operation suppresses pumping.
- `P_NONOVERLAP_PHASES`: Enabled clock updates alternate phase_a and phase_b while never asserting both phases together.
- `P_PUMP_REGULATION`: While pump_en is active, enabled phase updates raise vout in bounded pump steps; without pumping, vout leaks downward and remains within rails.
- `P_ERROR_REPORTING`: regulation_error continuously reports target minus vout and pump_en requests pumping below the lower tolerance boundary.
- `P_READY_QUALIFICATION`: Ready asserts only after three consecutive enabled clock updates within the regulation tolerance and clears outside qualification.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `phase_generator.va`, `pump_stage_model.va`, `regulation_comparator.va`, `voltage_multiplier_top.va`.
Do not add or omit artifacts.
