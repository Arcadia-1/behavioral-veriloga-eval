# Sine Periodic Voltage Source

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `multitone.va`: `multitone`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_FIRST_TONE`: The output includes a zero-phase sine component with frequency f1 and signed amplitude a1.
- `P_SECOND_TONE`: The output includes a zero-phase sine component with frequency f2 and signed amplitude a2.
- `P_THIRD_TONE`: The output includes a zero-phase sine component with frequency f3 and signed amplitude a3.
- `P_LINEAR_SUPERPOSITION`: At every transient time t, OUT equals a1*sin(2*pi*f1*t) plus a2*sin(2*pi*f2*t) plus a3*sin(2*pi*f3*t).
- `P_ZERO_INITIAL_PHASE`: With no added offset and zero initial phase for all tones, OUT is 0 V at t = 0.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `multitone.va`.
Do not add or omit artifacts.
