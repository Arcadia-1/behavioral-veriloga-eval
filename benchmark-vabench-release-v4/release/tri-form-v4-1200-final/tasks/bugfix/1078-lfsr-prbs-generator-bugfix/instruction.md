# LFSR PRBS Generator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `prbs7_ref.va`: `prbs7_ref`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_SEED`: When rst_n is below vth, the exposed seven-bit state is loaded from seed[6:0]; legal seed overrides are integers 0 through 127 inclusive, and seed 0 is remapped to 7'b0000001 to avoid the LFSR lock-up state.
- `P_ENABLE_GATING`: On rising clk crossings, the state advances only when rst_n and en are both above vth; otherwise it holds or resets as applicable.
- `P_FEEDBACK_POLYNOMIAL`: Each enabled update sets next state_0 to previous state_6 XOR previous state_5, implementing x^7 + x^6 + 1.
- `P_SHIFT_SEQUENCE`: Each enabled update sets next state_i to previous state_(i-1) for i from 1 through 6.
- `P_SERIAL_OUTPUT`: serial_out always represents the current state_6 bit.
- `P_OUTPUT_LEVELS`: serial_out and every state output use 0 V and vdd levels with delay td and transition smoothing trf.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `prbs7_ref.va`.
Every supplied `.va` file is editable; do not add or omit files.
