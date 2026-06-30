# AUDIT: Task 009 Lock Detector

## Scope

Task boundary is one Verilog-A DUT, `lock_detector.va`, plus EVAS/Spectre-compatible `.scs` testbenches. I only audited and changed files under this task directory. No `meta.json` is present or needed.

Agent-visible files are limited to:

- `instruction.md`
- `starter/lock_detector.va`
- `test_visible/visible.scs`

Evaluator-only files are:

- `solution/lock_detector.va`
- `test_hidden/hidden.scs`
- `CHECKS.json`
- `test_harness/visible_hidden_manifest.json`
- `negative_variants/`

## Four Standards

- Useful scenario: a reference/feedback lock detector is a common PLL behavioral control primitive. It is small enough for an L1/D2 behavioral Verilog-A task but still exercises event ordering, state retention, reset, and timing-window logic.
- Reasonable task: the public prompt states the exact module name, positional port order, electrical voltage-domain interface, active-low reset behavior, `2 ns` reference/feedback alignment window, three-consecutive-aligned-reference lock rule, no-early-lock requirement, mismatch clearing rule, and relock-after-reset requirement.
- Complete tests: the visible SCS is a useful smoke for syntax, reset low, acquisition after three aligned reference events, and loss of lock on a later mismatch. The hidden SCS adds post-acquisition active-low reset, a second acquisition sequence, and a later out-of-window mismatch. The negative set now contains concrete Verilog-A variants for late lock, over-wide tolerance, mismatch not clearing lock, reset not clearing lock, and counting feedback events instead of reference comparisons.
- Fair evaluation: `CHECKS.json` declares a trace-based checker contract over saved `time`, `ref_clk`, `fb_clk`, `rst_n`, and `lock`. The checker should reconstruct rising threshold crossings and enforce only behavior described in `instruction.md`; it should not rely on hidden-only stimulus knowledge.

Certification status: EVAS formal candidate. The task assets are self-consistent and the public runner has a `CHECKS` entry for this task-specific checker.

## Trace And Scoring Logic

At each `ref_clk` rising threshold crossing while `rst_n` is high, find the most recent `fb_clk` rising threshold crossing. The event is aligned only when the absolute time difference is at most 2 ns. The expected model clears state during active-low reset, increments a consecutive-hit counter on aligned reference events, asserts `lock` at the third consecutive hit, and clears both the counter and `lock` on any out-of-window reference event.

## Gold And Negative Expectations

- Gold `solution/lock_detector.va`: expected PASS on `test_visible/visible.scs` and `test_hidden/hidden.scs`.
- Starter `starter/lock_detector.va`: expected FAIL behavior because it does not drive `lock`.
- `neg_001_requires_four_hits`: expected FAIL because `lock` remains low after the third aligned reference event.
- `neg_002_tolerance_too_wide`: expected FAIL because a feedback edge about 5.9 ns from a reference edge is accepted as aligned.
- `neg_003_does_not_reset_on_mismatch`: expected FAIL because `lock` remains high after an out-of-window reference comparison.
- `neg_004_reset_ignored`: expected FAIL because active-low reset after acquisition does not clear `lock`.
- `neg_005_counts_feedback_events`: expected FAIL because it advances lock state on feedback edges instead of reference-edge comparisons and can assert early.

## Runner Integration Needed

The task declares `checker_id/check_name = v3_009_lock_detector` in the top-level indexes. The main runner maps:

```python
CHECKS["v3_009_lock_detector"] = check_v3_009_lock_detector
```

`check_v3_009_lock_detector` implements the trace logic above. It also samples `lock` during the second active-low reset window after lock acquisition, so a reset-ignored implementation cannot pass. Do not alias this to the old `main120_stable_checks.check_lock_detector`; that checker samples a legacy sequence and does not cover this hidden reset/mismatch contract.

## Certification Evidence

- EVAS/Python-engine hidden gold smoke: `PASS`.
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`.
- The previous reset-ignored negative now fails because the checker verifies lock is low during the post-acquisition reset window.
