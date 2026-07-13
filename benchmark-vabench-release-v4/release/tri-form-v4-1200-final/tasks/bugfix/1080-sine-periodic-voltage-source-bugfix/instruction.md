# Sine Periodic Voltage Source Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `multitone.va`: `multitone`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_FIRST_TONE`: The output includes a zero-phase sine component with frequency f1 and signed amplitude a1.
- `P_SECOND_TONE`: The output includes a zero-phase sine component with frequency f2 and signed amplitude a2.
- `P_THIRD_TONE`: The output includes a zero-phase sine component with frequency f3 and signed amplitude a3.
- `P_LINEAR_SUPERPOSITION`: At every transient time t, OUT equals a1*sin(2*pi*f1*t) plus a2*sin(2*pi*f2*t) plus a3*sin(2*pi*f3*t).
- `P_ZERO_INITIAL_PHASE`: With no added offset and zero initial phase for all tones, OUT is 0 V at t = 0.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `multitone.va`.
Every supplied `.va` file is editable; do not add or omit files.
