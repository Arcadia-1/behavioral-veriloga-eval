# DeepSeek v4 Flash Remaining-4 v2 Pilot

Date: 2026-06-24

Scope: run `deepseek-v4-flash` on the four vaBench v2 pilot tasks not covered
by the earlier low-pass bugfix smoke, then score generated artifacts with the
current EVAS/checker path.

Generation settings:

- Model: `deepseek-v4-flash`
- API format: OpenAI-compatible DeepSeek chat completion
- Thinking: `disabled`
- Max tokens: `8192`
- Local generation output: `/private/tmp/vabench_v2_deepseek_v4_flash_remaining4`
- Local scored output: `/private/tmp/vabench_v2_deepseek_v4_flash_remaining4_scored`

## Summary

| Task | Form | DeepSeek response | EVAS/checker status | Primary observation |
| --- | --- | ---: | --- | --- |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | L2 e2e | PASS | `FAIL_SIM_CORRECTNESS` | Candidate compiles and simulates, but checker reports `too_few_completed_conversions=0`. |
| `vbr1_l1_window_comparator_detector:tb` | L1 tb | PASS | `FAIL_DUT_COMPILE` | Candidate testbench uses multiline `wave=[...]` without Spectre continuations. |
| `vbr1_l1_aperture_delay_track_and_hold:dut` | L1 dut | PASS | `PASS` | Candidate passes EVAS/checker with exact delayed aperture sample sequence. |
| `vbr1_l2_gain_extraction_convergence_measurement_flow:e2e` | L2 support e2e | PASS | `FAIL_DUT_COMPILE` | Candidate triggers EVAS Rust full-model runtime failure; Python fallback timed out over 180 s. |

Overall EVAS/checker pass rate: `1/4`.

## Failure Classification

### CT01 SAR ADC/DAC loop

Observed result:

- Generated all four target files.
- EVAS compile/testbench execution succeeded.
- Behavior checker failed with `streaming_checker:too_few_completed_conversions=0`.

Likely classification:

- Primary: model functional failure under current checker.
- Possible benchmark issue: public spec may still be underspecified for reset
  release timing, conversion framing, scalarized bus wiring, and completed
  conversion observability.
- Spectre action: rerun generated candidate in Spectre to determine whether the
  no-completed-conversions result is simulator-independent or EVAS/checker
  specific.

### CT02 window comparator testbench

Observed result:

- Generated the target testbench.
- EVAS preflight rejected multiline PWL syntax:
  `multiline wave=[...] requires backslash line continuation`.

Likely classification:

- Primary: candidate syntax/style failure if Spectre also rejects the netlist.
- Benchmark issue: prompt currently asks for PWL/triangular waveform but does
  not explicitly require single-line PWL or Spectre line continuations.
- Spectre action: rerun candidate in Spectre. If Spectre rejects it, update
  public testbench-generation specs to include Spectre-safe PWL formatting. If
  Spectre accepts it, record this as an EVAS preflight false-negative.

### CT03 aperture-delay track-and-hold

Observed result:

- Generated the target DUT.
- EVAS/checker passed.
- Checker note: delayed aperture samples matched expected public sequence with
  zero mismatches.

Likely classification:

- Primary: v2 prompt is usable for this task.
- Spectre action: still rerun gold and DeepSeek candidate in Spectre before
  claiming dual-simulator validity.

### SUP01 gain extraction support flow

Observed result:

- Generated all five target files.
- EVAS Rust full-model path failed with:
  `runtime_failed:RustSim source+record program failed with code -841`.
- Python engine fallback did not complete within 180 s.

Likely classification:

- Primary: EVAS/Rust compatibility or robustness debt until Spectre proves the
  generated candidate is invalid.
- Possible benchmark issue: prompt permits a broad implementation space for
  LFSR, continuous sinusoidal source behavior, dither path, and testbench
  extras; this can produce candidates outside the current fast EVAS Rust subset.
- Spectre action: rerun generated candidate in Spectre. If Spectre passes, fix
  EVAS Rust/fallback handling before prompt-banning legal Verilog-A. If Spectre
  fails, tighten public spec around valid Spectre netlist constructs and allowed
  support-flow structure.

## Spectre Rerun Queue

Highest priority:

1. `SUP01` DeepSeek candidate: distinguish EVAS false negative from invalid
   generated Verilog-A/testbench.
2. `CT02` DeepSeek candidate: decide whether multiline PWL without continuation
   is genuinely Spectre-invalid.
3. `CT01` DeepSeek candidate: confirm whether the no-conversion behavior is
   simulator-independent.

Baseline certification:

4. Rerun all five v2 gold/reference forms in Spectre.
5. Rerun the two EVAS-passing DeepSeek candidates in Spectre:
   `CT03` and the latest low-pass `CT04` candidate.

## Current Benchmark Defects

1. Public specs mix task contracts with current EVAS subset expectations. The
   final benchmark should avoid overfitting prompts to EVAS limitations when
   Spectre accepts the construct.
2. Testbench-generation specs need a shared Spectre-safe formatting section for
   PWL, `simulator lang=spectre`, `global 0`, `ahdl_include` ordering, and bus
   save/connection conventions.
3. L2 e2e prompts may be too underspecified for model one-shot success. They
   expose functional goals but not enough execution protocol around reset,
   conversion framing, output observability, and sampling windows.
4. EVAS failure reporting still loses the most useful checker/error line in
   some summaries. The scoring harness should preserve first error, checker
   note, and waveform artifact path in a compact row-level report.
5. SUP01 remains a support-flow task, not a strong circuit-function benchmark
   task, unless the checker and prompt are tightened around a reproducible,
   simulator-portable measurement flow.
