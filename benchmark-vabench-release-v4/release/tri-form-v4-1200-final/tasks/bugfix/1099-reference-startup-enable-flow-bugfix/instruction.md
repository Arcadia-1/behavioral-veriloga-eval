# Reference Startup Enable Flow Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `reference_startup_enable_flow.va`: `reference_startup_enable_flow`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_SUPPLY_AND_ENABLE_MONITORS`: Supply_ok is 0.9 V exactly when vdd_in exceeds 0.32 V, while enable_mon is 0.9 V exactly when en exceeds vth.
- `P_RESET_OR_BROWNOUT`: Active reset or a bad supply clears out, metric, startup progress, and state; a supply dip also removes valid status.
- `P_DISABLED_REFERENCE`: With supply good and enable low, out is 0.05 V, metric is 0.1 V, startup progress is cleared, and state_mon represents state 1.
- `P_ENABLED_SETTLING`: On each rising clk crossing with supply good and enable high, out advances by 0.32 times its remaining error to 0.55 V and the startup count increments up to 8.
- `P_STARTUP_VALIDITY`: During enabled startup metric is 0.25 V and state is 2; after at least five enabled updates with out above 0.48 V, metric is 0.9 V and state is 3.
- `P_BROWNOUT_RECOVERY`: After a supply dip and restoration with enable asserted, the output and monitors repeat the same startup sequence before returning valid.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `reference_startup_enable_flow.va`.
Every supplied `.va` file is editable; do not add or omit files.
