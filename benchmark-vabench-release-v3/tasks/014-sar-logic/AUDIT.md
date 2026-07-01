# Audit: 014 SAR Logic

Gate 1: `independent_l1_ready`. This is a SAR ADC decision sequencer rather
than an analog transfer row: it controls trial bits, captures comparator
decisions, and asserts completion for a 4-bit conversion.

Gate 2: `cadence_modeling_ready`. The public prompt defines the target
interface, rising-clock conversion sequence, comparator-decision rule, bit
order, `RDY` behavior, output levels, transition time, and voltage-only
constraints. Current PR validation: EVAS gold PASS, Spectre AX hidden gold
PASS, and EVAS/Spectre negatives rejected with no Spectre errors. Spectre
emitted only environment/setup warnings.

Hidden/visible coverage: visible and hidden decks are structurally distinct.
The hidden deck checks sequencing and final conversion state beyond visible
compile/smoke coverage.

Checker coverage: `v3_014_sar_logic` evaluates the public SAR sequencing
contract and rejects wrong bit capture, wrong ready timing, bit-order errors,
missing ready, and wrong final decision code.
