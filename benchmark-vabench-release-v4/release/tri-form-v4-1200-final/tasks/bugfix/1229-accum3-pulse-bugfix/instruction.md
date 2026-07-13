# Accum3 Pulse Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `accum3_pulse.va`: `accum3_pulse`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIALIZE_THE_INTERNAL_3_BIT_COUNT`: Initialize the internal 3-bit count to 7.
- `P_INCREMENT_THE_COUNT_MODULO_8_ON`: Increment the count modulo 8 on each rising `clk` crossing.
- `P_DRIVE_OUT_HIGH_ONLY_WHEN_THE`: Drive `out` high only when the modulo count is 0.
- `P_DRIVE_OUT_LOW_FOR_ALL_OTHER`: Drive `out` low for all other count values.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `accum3_pulse.va`.
Every supplied `.va` file is editable; do not add or omit files.
