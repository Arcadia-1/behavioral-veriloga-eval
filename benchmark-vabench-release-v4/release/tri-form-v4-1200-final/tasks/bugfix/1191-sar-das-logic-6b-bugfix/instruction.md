# SAR DAS Logic 6b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sar_das_logic_6b.va`: `sar_das_logic_6b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_SAMPLING_RESET_CONVERSION_STATE`: A rising `clk_sampling` transition clears controls and pulses, and a falling transition arms the SAR conversion sequence.
- `P_SAR_COMPARATOR_POLARITY`: Each rising `clk_sar` transition compares `vcomp` to `vcm` and drives `co/cob` with the declared polarity.
- `P_SIX_BIT_DECISION_SEQUENCE`: The SAR decisions update `d6..d1` in the declared order through the conversion.
- `P_CONTROL_OUTPUT_LEVELS`: Decision pulses and bit-control outputs use valid voltage-coded low/high levels.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sar_das_logic_6b.va`.
Every supplied `.va` file is editable; do not add or omit files.
