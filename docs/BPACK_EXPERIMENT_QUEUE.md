# bpack48 Priority Experiment Queue

**Date**: 2026-05-08

This queue narrows `bpack48` experiments to the clean current mainline.  The
first P1/P2 cycle has run; the next work should be targeted residual repair, not
another broad full-matrix expansion.

## Prerequisites

| Step | Output | Status |
| --- | --- | --- |
| B0 inventory | `docs/BPACK_V1_INVENTORY.json` | drafted |
| B1 benchmark root | `benchmark-bpack-v1/` | frozen bpack48: 48/48 tasks |
| B2 gold validation | EVAS+Spectre gold validation summary | strict-EVAS 48/48; Spectre 48/48 |
| Provider availability | Valid model API key in environment | MiMo key available for smoke/model runs |

Model experiments can start because B1 and B2 pass.

Current draft status is summarized in
`docs/BPACK_V1_MATERIALIZATION_REPORT.md` and
`docs/BPACK_V1_FREEZE_CANDIDATE_REPORT.md`.  The benchmark is runnable,
task-form complete, and gold-validated by both strict-EVAS and Spectre.

## Completed Main Chain

All rows below use `provider=mimo`, `model_id=mimo-v2.5-pro`,
`MIMO_THINKING_TYPE=disabled`, `MAX_TOKENS=8192`, `temperature=0`, `top_p=1`,
and strict-EVAS on `benchmark-bpack-v1`.

| Condition | Scope | PASS | Compile failures | Behavior failures | Incremental LLM cost | Status |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `prompt-only` | full 48 | 15/48 | 25 | 8 | 48 calls, 86818 tokens | clean baseline |
| `rules-only` | full 48 | 16/48 | 20 | 12 | 48 calls, 141161 tokens | public-rule baseline |
| `compile-loop` | full 48 | 16/48 | 18 | 14 | 20 repair calls, 84388 tokens | compile closure improves, PASS does not |
| `compile-skill-prompt` | full 48 | 21/48 | 10 | 17 | 21 repair calls, 101481 tokens | current best full row |
| `compile-skill-local` | full 48 replay | 19/48 | 10 | 19 | 0 extra beyond `compile-loop` | local replay row |
| `compile-skill-accept` | full 48 replay | 19/48 | 10 | 19 | 0 extra beyond `compile-loop` | accept/reject row |
| `compile-skill-advanced` | full 48 replay | 19/48 | 10 | 19 | 0 extra beyond `compile-loop` | advanced local registry row |

Primary questions:

1. `rules-only` is only a weak improvement over `prompt-only` on MiMo bpack48.
2. `compile-loop` improves compile closure but not PASS.
3. Prompt-side compile skill guidance is currently the strongest full-row
   mechanism.
4. Local accept/reject skills are useful infrastructure but do not beat
   prompt-side skill guidance on this run.

## Completed Targeted Smokes

| Condition | Scope | PASS | Compile failures | Behavior failures | Cost | Current interpretation |
| --- | --- | ---: | ---: | ---: | --- | --- |
| CE-v2 residual smoke | 7 compile residual tasks | 2/7 | 4 | 1 | 7 calls, 33015 tokens | Context engineering has targeted value. |
| PSE-CE residual smoke | same 7 tasks | 2/7 | 4 | 1 | 14 calls, 63014 tokens | More auditable but no status gain over CE-v2. |
| controller `pass-efficient` v0.3 | same 7 tasks | 1/7 | 5 | 1 | 2 projected calls, 7426 projected tokens | Tool routing/cost triage only. |
| controller `compile-coverage` v0.3 | same 7 tasks | 1/7 | 4 | 2 | 3 projected calls, 11739 projected tokens | Compile-coverage triage only. |

Older controller rows that reported `2/7` are diagnostic only.  They trusted
cached result files before current strict-EVAS re-score was enforced.

## Next Priority: Targeted Residual Repairs

Do not run another full bpack48 condition until a targeted residual smoke gives
a positive signal.

| Order | Family | Tasks | Expected fix |
| --- | --- | --- | --- |
| R1 | Empty PWL TB stimulus | `bpack_hysteresis_comparator_tb`, `bpack_sample_hold_tb` | Public TB stimulus skill; accept only if strict-EVAS rank improves. |
| R2 | Required module alias/wrapper | `bpack_prbs7_lfsr_e2e` | Materialize public module-name alias/wrapper. |
| R3 | Public port-role/order | `bpack_analog_limiter_dut`, `bpack_analog_limiter_tb`, `bpack_pulse_stretcher_dut`, `bpack_threshold_detector_tb`, `bpack_window_detector_tb` | Public port-contract skill; no task-id routing. |
| R4 | DWA multi-module interface | `bpack_dwa_pointer_bugfix`, `bpack_dwa_pointer_dut`, `bpack_dwa_pointer_tb` | Specialized interface/materialization skill. |

### R1-R4 Smoke Outcome

These smokes have now run from the `compile-skill-prompt` source row.

| Run | Accepted | Status delta | Decision |
| --- | ---: | --- | --- |
| R1 Empty PWL TB stimulus | 2/2 | one PASS, one behavior fail | Keep `pwl_inline_wave_vector`. |
| R2 Required module alias/wrapper | 1/1 | one behavior fail | Keep `module_alias_duplicate` and `verilog_binary_literal_decimal`. |
| R3 Public port-role/order | 1/4 | one behavior fail | Current detach repair is narrow; next work is public port-order/header repair. |
| R4 DWA multi-module interface | 0/3 | no improvement | Needs specialized DWA/interface skill. |

Combined over the 10 `compile-skill-prompt` compile residuals: `1/10 PASS`,
`6/10` compile failures, `3/10` behavior failures, 0 LLM calls.  Treat the
full-row impact as projected until a full 48 materialization/re-score is run:
`21/48 -> 22/48`, compile failures `10 -> 6`.

## Still Excluded From Immediate Runs

| Condition | Reason |
| --- | --- |
| `evas-repair` | Generic repair negative control; appendix only after main chain stabilizes. |
| `mechanism-public` | Behavior mechanism hypothesis; wait until compile residuals are lower or behavior failures dominate. |
| `functional-ir` | IR hypothesis; wait for behavior residual family analysis. |
| full controller rerun | Only useful after stronger execution tools exist. |

## Reporting For Every Run

Report both task-level and pack-level metrics:

| Metric | Required |
| --- | --- |
| `PASS/48` | yes |
| `Pack success` | yes |
| `Avg forms/pass per pack` | yes |
| Pass by task form | yes |
| Compile pass rate | yes |
| Sim correctness rate | yes |
| Avg tokens/task | yes |
| Avg API time/task | yes |
| Exact provider | yes |
| Exact model id | yes |
| Model thinking/reasoning mode | yes |

## Provider Probe Before Full Runs

Before running a new model/provider on the full bpack benchmark, run the fixed
high-output probe:

```bash
MODEL=<model> GEN_WORKERS=8 MAX_TOKENS=4096 runners/run_bpack_provider_probe.sh
```

The current MiMo controlled setting is:

- `provider=mimo`
- `MODEL=mimo-v2.5-pro`
- `MIMO_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1`
- `MIMO_THINKING_TYPE=disabled`
- `MAX_TOKENS=4096`
- `GEN_WORKERS=8`
- `temperature=0`, `top_p=1`

The 2026-05-08 MiMo probe passed the provider gate:

- 8/8 high-output tasks generated extractable code.
- 0 API errors at `GEN_WORKERS=8`.
- 0 hidden reasoning tokens with `MIMO_THINKING_TYPE=disabled`.
- 1/8 tasks still hit `finish_reason=length`, now due to visible output length
  rather than hidden reasoning.

A follow-up reasoning ablation on the same 8 tasks rejected provider-default
reasoning for mainline runs:

| Mode | Max tokens | Generated | No code | Hidden reasoning tokens | Avg API s/task | strict-EVAS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `thinking=disabled` | 4096 | 8/8 | 0/8 | 0 | 21.2 | 1/8 |
| provider default | 4096 | 1/8 | 7/8 | 29,534 | 63.5 | 0/8 |
| provider default | 8192 | 3/8 | 5/8 | 57,582 | 117.2 | 1/8 |

Conclusion: use `thinking=disabled` for controlled MiMo rows.  Provider-default
reasoning is diagnostic only unless a future model/prompt passes the same
artifact gate.

The Kimi reference rows should be reported as:

- `provider=bailian` / Bailian-Anthropic-compatible route
- `model_id=kimi-k2.5`
- `reasoning_mode=provider-default/not-reported`

Do not report broad model-family labels such as only `Kimi` or only `MiMo` in
tables; use the exact provider/model id pair.

## Stop/Go Gates

| Gate | Decision |
| --- | --- |
| Gold validation fails | Do not run models; fix benchmark. |
| `rules-only` fails to generate usable artifacts | Fix prompt/provider extraction before P1.3. |
| A targeted repair does not improve affected tasks | Do not promote it to full bpack48. |
| A cached/tool-controller candidate is not re-scored with current strict-EVAS | Result is invalid. |
| A key PASS delta lacks Spectre audit | It can be internal evidence only, not paper evidence. |
