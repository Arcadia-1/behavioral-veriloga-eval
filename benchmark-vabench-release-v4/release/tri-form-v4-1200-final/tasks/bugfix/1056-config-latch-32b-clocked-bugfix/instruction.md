# Config Latch 32b Clocked Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `config_latch_32b.va`: `config_latch_32b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ENABLED_PASS`: When en is high, every q bit equals the corresponding voltage-coded d bit.
- `P_DISABLED_CLEAR`: When en is low, every q bit is driven low regardless of the data input.
- `P_STATIC_ENABLE_BEHAVIOR`: The public interface is combinational enable gating: q follows data changes while enabled and does not retain a prior word while disabled.
- `P_BIT_ALIGNMENT`: Each d[N] controls only the same-index q[N]; bus order is not reversed or shifted.
- `P_OUTPUT_LEVELS`: Each q bit uses 0 V for logic low and vdd for logic high with finite transition smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `config_latch_32b.va`.
Every supplied `.va` file is editable; do not add or omit files.
