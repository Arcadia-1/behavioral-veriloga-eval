# SOP Audit: Fractional-N Divider Accumulator Flow

## Scope

PLL clock-and-timing system flow (L2). The DUT is a fractional-N PLL-style
behavioral module with a timer-scheduled DCO, accumulator-dithered feedback
divider, proportional plus bounded-integral phase correction, control-voltage
monitor, and lock indicator.

## Review Findings

- Gate 1: `l2_core_ready` as an integrated PLL timing/control flow candidate,
  pending upstream counting policy for extension rows outside the original
  full-300 denominator.
- Gate 2: `cadence_lint_pending`; EVAS lint is clean and targeted Spectre
  simulation passes, but a separate `spectre -ahdllint` oracle run has not
  been recorded in this public audit.
- Prompt hygiene: removed historical import language and private evaluator
  wording from the public contract and gold comments.
- Artifact boundary: target is only `fracn_pll_timer_ref.va`; the harness
  supplies `ref_step_clk.va` as support.
- Contract repair: the fractional divider wording now distinguishes
  feedback-output toggle count from a complete feedback rising-edge period.
  The average DCO-edge count per feedback-output toggle is
  `div_int - frac_word/acc_modulus`; a full feedback rising-edge period spans
  two toggles.
- Checker repair: in addition to lock/reacquire and bounded `vctrl_mon`, the
  checker now inspects late-window DCO edge counts between feedback rising
  edges to reject pure integer-divider behavior.
- Visible smoke repair: the visible reference-step deck now uses lock tolerance
  settings that allow the gold model to demonstrate pre-step lock and
  post-step reacquisition under the same checker as the hidden deck.

## Checker Context

- Checker id: `v3_505_fractional_n_divider_accumulator_flow`.
- The checker compares late feedback cadence against the stepped reference,
  requires lock to drop and reassert, verifies bounded control movement, and
  checks that fractional short-count behavior appears in the DCO-edge counts.

## Validation Status

Fresh validation from this clean branch:

- EVAS gold/negative: 504 and 505 gold PASS with ten negatives rejected after
  staging 502/503 as EVAS2-pending VCO extension rows.
- Spectre hidden gold: 505 PASS with late fractional DCO counts
  `[16, 15, 15, 15, 16, 15, 15, 15]` and lock reacquisition.
- EVAS AHDL-like lint preflight: visible and hidden decks PASS with zero
  diagnostics after smoothing the event-updated `vctrl_mon` contribution.
- Spectre visible gold: PASS after the visible smoke repair.
- Cadence `spectre -ahdllint`: not run as a separate oracle in this PR.
