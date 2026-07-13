# LDO Regulator Macro Model Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ldo_regulator_macro_model.va`: `ldo_regulator_macro_model`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_AND_RESET_STATE`: Initialization or active-high reset sets out to 0.60 V and metric to 0.9 V.
- `P_LOAD_TARGET`: At each eligible rising clock crossing, vin is clamped to 0 through 0.9 V and target equals 0.62 V minus 0.055 times that load.
- `P_FIRST_ORDER_REGULATION`: Out advances by 0.35 of the remaining target error on each eligible rising clock crossing.
- `P_REGULATED_OUTPUT_CLAMP`: The held output remains within 0.25 V through 0.75 V.
- `P_ERROR_METRIC`: Metric equals 0.9 V minus four times the absolute output-to-target error, clamped to 0 through 0.9 V.
- `P_CLOCKED_HOLD`: Out and metric hold between rising clock crossings except for transition smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ldo_regulator_macro_model.va`.
Every supplied `.va` file is editable; do not add or omit files.
