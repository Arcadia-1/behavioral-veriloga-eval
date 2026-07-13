# Clock-and-data Valid Qualifier Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `clock_data_valid_qualifier.va`: `clock_data_valid_qualifier`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or disable clears valid, qualification, and the public age metric.
- `P_DATA_EDGE_RESTART`: Either polarity data edge restarts the age count at zero while enabled.
- `P_CLOCKED_AGE`: Each later rising clk edge increments age before qualification.
- `P_INCLUSIVE_WINDOW`: Ages one through max_age_cycles are qualified and older ages are not.
- `P_REGISTERED_METRIC`: valid_out is the registered qualified state and the metric reports saturated normalized age.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `clock_data_valid_qualifier.va`.
Every supplied `.va` file is editable; do not add or omit files.
