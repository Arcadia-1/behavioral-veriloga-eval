# Debounce Latch Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `debounce_latch.va`: `debounce_latch`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ACTIVE_LOW_RESET`: out is low and pending qualification is cancelled whenever rst_n is below vth.
- `P_RISE_QUALIFICATION`: A sig rising edge sets out high only after sig and rst_n remain high for stable seconds.
- `P_FALL_CLEAR`: A sig falling edge clears out and cancels pending qualification.
- `P_EVENT_HOLD`: out holds between reset, sig-edge, and qualification-timer events.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `debounce_latch.va`.
Every supplied `.va` file is editable; do not add or omit files.
