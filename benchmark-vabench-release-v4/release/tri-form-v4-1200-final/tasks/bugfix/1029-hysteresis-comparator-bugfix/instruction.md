# Hysteresis Comparator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cmp_hysteresis.va`: `cmp_hysteresis`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_DECISION`: OUTP initializes high only when the initial differential exceeds positive vhys over two; otherwise OUTP initializes low and OUTN high.
- `P_POSITIVE_SWITCH_THRESHOLD`: The low OUTP state switches high only on a rising differential crossing of positive vhys over two.
- `P_NEGATIVE_SWITCH_THRESHOLD`: The high OUTP state switches low only on a falling differential crossing of negative vhys over two.
- `P_HYSTERESIS_HOLD`: The previous decision is retained while the differential remains inside the hysteresis band.
- `P_COMPLEMENTARY_RAIL_OUTPUT`: OUTP and OUTN remain complementary and use the local VDD and VSS rail levels after smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cmp_hysteresis.va`.
Every supplied `.va` file is editable; do not add or omit files.
