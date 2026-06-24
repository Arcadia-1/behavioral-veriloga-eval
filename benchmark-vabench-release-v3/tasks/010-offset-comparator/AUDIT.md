# Honest SOP Audit: Task 010 Offset Comparator

## Scope

Task boundary is one Verilog-A DUT, `cmp_offset_ref.va`, plus EVAS/Spectre-compatible `.scs` testbenches. The agent-facing surface is limited to `instruction.md`, `starter/`, and `test_visible/`; `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/` are evaluator-only.

## Four Standards

- Useful scenario: a clocked comparator with a deliberate input offset is a common behavioral primitive for mixed-signal decision circuits and offset-aware ADC/control modeling.
- Reasonable task: the public prompt states the exact module name, port order, electrical ports, 0/0.9 V logic convention, rising-clock sampling rule, about +5 mV positive offset threshold, rail-to-rail `OUT_P` levels, and smoothed voltage-domain transitions.
- Complete tests: visible smoke covers negative input, a below-offset positive input, an above-offset positive input, and delayed response until the next rising clock edge. Hidden stimulus extends the same public contract to seven rising-edge decisions and explicit between-edge hold samples after threshold-crossing input changes.
- Fair evaluation: the checker should use only saved `CLK`, `VINP`, `VINN`, and `OUT_P`; it should sample settled outputs after rising edges, require low below 0.09 V and high above 0.81 V, and require no asynchronous output response at the specified between-edge hold points. No hidden scoring behavior is absent from the public prompt.

Certification status: EVAS formal candidate. Gold passes under strict checker id `v3_010_offset_comparator`. All five concrete negatives compile and fail with `FAIL_SIM_CORRECTNESS`.

## Expected Gold And Negative Outcomes

- `solution/cmp_offset_ref.va`: PASS; expected hidden sequence is `LLLHHLL` at the settled post-rising-edge samples, with holds low/high/low at the between-edge async-check samples.
- `neg_001_zero_offset`: FAIL; +3 mV is below the required +5 mV offset but latches high.
- `neg_002_large_offset`: FAIL; +7 mV is above the required +5 mV offset but latches low.
- `neg_003_falling_edge`: FAIL; samples on falling clock edges instead of rising clock edges.
- `neg_004_async_response`: FAIL; updates output when the input changes between rising clock edges.
- `neg_005_weak_high`: FAIL; high decisions do not reach the required VDD-level high threshold.

## Runner Hookup Note

`test_harness/checks.yaml` declares checker id `v3_010_offset_comparator`. The runner maps that id to `check_v3_offset_comparator`, which first checks the seven-edge `LLLHHLL` decision sequence and then checks between-edge async-hold samples plus rail-level output thresholds.

## Certification Evidence

- EVAS/Python-engine hidden gold smoke: `PASS`.
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`.
- `neg_004_async_response` now fails on async-hold samples, and `neg_005_weak_high` fails on rail-level high thresholds.

## Remaining Risk

- Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
