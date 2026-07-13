# Analog Mux Threshold Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `analog_mux_threshold.va`: `analog_mux_threshold`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_HIGH_SELECTS_VIN1`: When vsel is above vth, vout follows vin1 rather than vin2.
- `P_LOW_SELECTS_VIN2`: When vsel is at or below vth, vout follows vin2 rather than vin1.
- `P_BIDIRECTIONAL_SELECTION`: The selected input updates after both rising and falling crossings of vsel through vth.
- `P_INITIAL_SELECTION`: Before any select transition, vout is selected from the initial vsel level using the same strict-greater-than threshold rule.
- `P_NO_MIXING`: The output represents one selected input and does not average or sum vin1 and vin2.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `analog_mux_threshold.va`.
Every supplied `.va` file is editable; do not add or omit files.
