# Propagation Delay Comparator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cmp_delay.va`: `cmp_delay`
- `edge_interval_timer.va`: `edge_interval_timer`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_DECISION`: At each rising CLK crossing through half the VDD-to-VSS rail span, the comparator latches the sign of VINP minus VINN minus voffset into complementary DCMPP/DCMPN decisions, with LP mirroring DCMPP and LM mirroring DCMPN.
- `P_FALLING_RESET`: Each falling CLK crossing resets both comparator decision outputs low.
- `P_DELAY_MAGNITUDE_TREND`: For otherwise equal conditions, a smaller absolute effective differential input produces a longer clock-to-decision delay.
- `P_DELAY_CLAMP`: The scheduled comparator decision delay follows the public log-linear regeneration relation and remains within td_min through td_max.
- `P_EDGE_INTERVAL_MEASUREMENT`: After a rising CLK_1 crossing arms the timer, the next rising CLK_2 crossing updates OUT_PS to the elapsed interval expressed in picoseconds and holds that completed measurement.
- `P_BUNDLE_BINDING`: The timing helper observes the comparator clock as CLK_1 and the positive comparator decision as CLK_2, exposing their measured interval on delay_ps.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cmp_delay.va`, `edge_interval_timer.va`.
Do not add or omit artifacts.
