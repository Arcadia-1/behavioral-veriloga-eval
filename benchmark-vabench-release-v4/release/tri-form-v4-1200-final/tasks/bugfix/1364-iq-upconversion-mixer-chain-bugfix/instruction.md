# I/Q Upconversion Mixer Chain Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `iq_upconversion_mixer.va`: `iq_upconversion_mixer`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation drives RF and debug outputs to vcm and clears quad_ok.
- `P_IQ_SIGNED_MIXING`: I and Q debug outputs equal vcm plus the specified signed LO products, including the negative Q-path convention.
- `P_RF_SUM_CLAMP`: rf_out equals the bounded sum of the I and Q path contributions about vcm.
- `P_QUADRATURE_ACTIVITY`: quad_ok asserts only after each LO input has crossed threshold since the latest reset or enable event.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `iq_upconversion_mixer.va`.
Every supplied `.va` file is editable; do not add or omit files.
