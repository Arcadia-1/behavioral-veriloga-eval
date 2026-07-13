# Downconversion Mixer with LO Polarity Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `downconversion_mixer_lo_polarity.va`: `downconversion_mixer_lo_polarity`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CENTER`: Reset or disable centers I/Q outputs and clears LO metrics and polarity_ok.
- `P_LO_POLARITY_METRICS`: Each LO threshold state selects signed polarity and is mirrored by its public metric.
- `P_IQ_CONVERSION`: I and Q outputs follow the declared common-mode referenced conversion-gain equations with independent LO signs.
- `P_OUTPUT_CLAMP`: Both baseband outputs remain within the declared supply rails.
- `P_POLARITY_QUALIFICATION`: polarity_ok asserts only after both LO controls have toggled while enabled.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `downconversion_mixer_lo_polarity.va`.
Every supplied `.va` file is editable; do not add or omit files.
