# Propagation Delay Comparator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cmp_delay.va`: `cmp_delay`
- `edge_interval_timer.va`: `edge_interval_timer`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLOCKED_DECISION`: At each rising CLK crossing through half the VDD-to-VSS rail span, the comparator latches the sign of VINP minus VINN minus voffset into complementary DCMPP/DCMPN decisions, with LP mirroring DCMPP and LM mirroring DCMPN.
- `P_FALLING_RESET`: Each falling CLK crossing resets both comparator decision outputs low.
- `P_DELAY_MAGNITUDE_TREND`: For otherwise equal conditions, a smaller absolute effective differential input produces a longer clock-to-decision delay.
- `P_DELAY_CLAMP`: The scheduled comparator decision delay follows the public log-linear regeneration relation and remains within td_min through td_max.
- `P_EDGE_INTERVAL_MEASUREMENT`: After a rising CLK_1 crossing arms the timer, the next rising CLK_2 crossing updates OUT_PS to the elapsed interval expressed in picoseconds and holds that completed measurement.
- `P_BUNDLE_BINDING`: The timing helper observes the comparator clock as CLK_1 and the positive comparator decision as CLK_2, exposing their measured interval on delay_ps.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cmp_delay.va`, `edge_interval_timer.va`.
Every supplied `.va` file is editable; do not add or omit files.
