# Differential Amplifier Core Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `differential_amplifier_core.va`: `differential_amplifier_core`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_DIFFERENTIAL_INPUT`: Use `V(sigin_p, sigin_n)` as the input signal.
- `P_INPUT_OFFSET`: Subtract the fixed 0.05 V input-referred offset before applying gain.
- `P_GAIN_TWO_OUTPUT`: Drive `sigout` to `2.0 * (V(sigin_p, sigin_n) - 0.05)`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `differential_amplifier_core.va`.
Every supplied `.va` file is editable; do not add or omit files.
