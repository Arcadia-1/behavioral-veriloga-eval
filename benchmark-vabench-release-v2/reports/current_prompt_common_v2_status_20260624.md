# vaBench v2 common-prompt status, 2026-06-24

## Scope

This note records the current five-task vaBench v2 prompt/render/check/score state after adding a shared agent-visible prompt layer.

## Current common-prompt change

- `config/common_agent_prompt.md` defines release-wide agent-facing rules:
  - produce only the requested artifacts;
  - preserve the required module, subcircuit, port, and top-level net names;
  - treat saved waveform signal names as part of the public contract;
  - use Spectre-valid multiline syntax for PWL sources;
  - treat support files as read-only context;
  - do not rely on private checker/gold/internal paths.
- `config/release_config.json` points `prompt_protocol.common_agent_prompt` to the common prompt.
- `scripts/render_agent_prompt.py` prepends the common prompt before each task-specific question and reports renderer version `vabench-release-v2-renderer-v2`.
- `scripts/audit_prompt_boundaries.py` verifies that rendered prompts include the common prompt and checks leak/anchor/saved-signal rules against the combined public text.
- `scripts/run_model_prompt_smoke.py` records `prompt_sha256` and `renderer_version` per row.
- `scripts/score_model_prompt_smoke_outputs.py` supports optional `--spectre` scoring in addition to EVAS scoring.

## Validation run

Executed from `behavioral-veriloga-eval`:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/evas_pycache python3 -m py_compile \
  benchmark-vabench-release-v2/scripts/render_agent_prompt.py \
  benchmark-vabench-release-v2/scripts/audit_prompt_boundaries.py \
  benchmark-vabench-release-v2/scripts/audit_spec_checker_map.py \
  benchmark-vabench-release-v2/scripts/run_model_prompt_smoke.py \
  benchmark-vabench-release-v2/scripts/score_model_prompt_smoke_outputs.py

python3 benchmark-vabench-release-v2/scripts/audit_prompt_boundaries.py \
  --root benchmark-vabench-release-v2 \
  --output /private/tmp/vabench_v2_prompt_boundaries_common_prompt.json

python3 benchmark-vabench-release-v2/scripts/audit_spec_checker_map.py \
  --root benchmark-vabench-release-v2 \
  --output /private/tmp/vabench_v2_spec_checker_common_prompt.json

python3 benchmark-vabench-release-v2/scripts/run_model_prompt_smoke.py \
  --root benchmark-vabench-release-v2 \
  --model deepseek-v4-flash \
  --limit 5 \
  --dry-run \
  --output-root /private/tmp/vabench_v2_current_prompt_dryrun_20260624
```

Result:

- prompt boundary audit: PASS, 5/5 forms.
- spec/checker map audit: PASS, 5/5 forms.
- prompt dry run: PASS, 5/5 rendered prompts.

Current prompt hashes:

| Task form | Prompt chars | SHA-256 |
| --- | ---: | --- |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | 4176 | `1fca35c5e4c5dddc604159b970dc7da7c36f6cddd8459357179b727f504615ed` |
| `vbr1_l1_window_comparator_detector:tb` | 4218 | `04718e65ed980e948016326054f0d05e709468c028fc0e7aba67e8d4df492b28` |
| `vbr1_l1_aperture_delay_track_and_hold:dut` | 3614 | `9cb3b86e0b430592f7b9c7009ef1ca318c43dc930269f562ace7bebef1d552bd` |
| `vbr1_l1_first_order_lowpass:bugfix` | 4187 | `82f5823ba9cc998a2845d695639304ba83453a674afe8ba607bff1912b3b7084` |
| `vbr1_l2_gain_extraction_convergence_measurement_flow:e2e` | 3916 | `2dadd4e337f1d72d3828f0a637a97801b6374f460232a56f5072aede55f03f9b` |

## Spectre score-path regression

Executed against the earlier DeepSeek output set, not a fresh current-prompt generation:

```bash
./scripts/run_with_bridge.sh python3 benchmark-vabench-release-v2/scripts/score_model_prompt_smoke_outputs.py \
  --root benchmark-vabench-release-v2 \
  --input-root benchmark-vabench-release-v2/reports/model_smoke/deepseek_v4_flash_5task_rerun_20260624 \
  --output-root /private/tmp/vabench_v2_score_script_spectre_regression_20260624 \
  --spectre \
  --timeout-s 300 \
  --spectre-mode ax
```

Result:

- score script executed EVAS and Spectre paths.
- old candidate pass count remains 1/5.
- `vbr1_l1_aperture_delay_track_and_hold:dut` passes both EVAS and Spectre.
- `vbr1_l1_window_comparator_detector:tb` demonstrates the saved-net failure mode: Spectre runs, but warns that `vin` and `out` are not top-level nodes and therefore does not save them. This is exactly why the common prompt now states that saved signal names are public contract names and must be real top-level Spectre nets.

## Fresh current-prompt generation

Fresh DeepSeek generation for the latest renderer/prompt hashes was run with a temporary API-key file under `/private/tmp`; the temporary key file was deleted after the run.

```bash
python3 benchmark-vabench-release-v2/scripts/run_model_prompt_smoke.py \
  --root benchmark-vabench-release-v2 \
  --model deepseek-v4-flash \
  --base-url https://api.deepseek.com \
  --api-key-file /private/tmp/vabench_deepseek_api_key_20260624 \
  --limit 5 \
  --max-tokens 4096 \
  --temperature 0 \
  --thinking disabled \
  --timeout-s 180 \
  --output-root benchmark-vabench-release-v2/reports/model_smoke/deepseek_v4_flash_current_prompt_common_v2_20260624
```

Result:

- API/model call status: PASS, 5/5 responses produced.
- output root: `benchmark-vabench-release-v2/reports/model_smoke/deepseek_v4_flash_current_prompt_common_v2_20260624`.
- prompt hashes match the current renderer-version table above.
- Raw model-smoke prompts, responses, candidate files, logs, and waveform outputs are disposable local artifacts and are intentionally excluded from the release-format PR.

## Fresh current-prompt scoring

The fresh current-prompt responses were scored with EVAS plus Spectre:

```bash
./scripts/run_with_bridge.sh python3 benchmark-vabench-release-v2/scripts/score_model_prompt_smoke_outputs.py \
  --root benchmark-vabench-release-v2 \
  --input-root benchmark-vabench-release-v2/reports/model_smoke/deepseek_v4_flash_current_prompt_common_v2_20260624 \
  --output-root benchmark-vabench-release-v2/reports/model_smoke/deepseek_v4_flash_current_prompt_common_v2_20260624_scored \
  --spectre \
  --timeout-s 300 \
  --spectre-mode ax
```

Result:

- final PASS: 0/5.
- generation success is no longer the bottleneck; task correctness is the bottleneck.

| Task form | EVAS status | EVAS weighted score | Spectre status | Primary failure |
| --- | --- | ---: | --- | --- |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | `FAIL_TB_COMPILE` | 0.3333 | `FAIL` | EVAS compile fails in `sar_adc_weighted_8b.va`: Python-side numeric conversion receives a tuple; Spectre does not produce `tran_spectre.csv`. |
| `vbr1_l1_window_comparator_detector:tb` | `FAIL_TB_COMPILE` | 0.3333 | `FAIL` | candidate PWL waveform has duplicate times at `1e-08`; no transient waveform is produced. |
| `vbr1_l1_aperture_delay_track_and_hold:dut` | `FAIL_SIM_CORRECTNESS` | 0.6667 | `FAIL` | candidate compiles but samples all expected aperture points as 0.000 instead of the public expected sequence. |
| `vbr1_l1_first_order_lowpass:bugfix` | `FAIL_SIM_CORRECTNESS` | 0.6667 | `FAIL` | candidate compiles but response is too slow for the public first-order low-pass behavior envelope. |
| `vbr1_l2_gain_extraction_convergence_measurement_flow:e2e` | `FAIL_TB_COMPILE` | 0.3333 | `FAIL` | EVAS parser rejects `vin_src.va` near `fin`; Spectre does not produce `tran_spectre.csv`. |

Additional failure audit:

- `vbr1_l2_weighted_sar_adc_dac_loop:e2e`: Spectre also fails during circuit read-in with `SFE-874` syntax errors. The candidate mixes vector-style Verilog-A ports with Spectre net names such as `dout<7>` in the testbench, so this should be treated first as model/prompt-interface failure, not an EVAS-only false negative.
- `vbr1_l1_window_comparator_detector:tb`: both EVAS and Spectre reject the PWL source because adjacent breakpoints reuse the same time (`10n`, `30n`, etc.). This is a model-format failure under Spectre-public syntax, not an EVAS debt.
- `vbr1_l1_aperture_delay_track_and_hold:dut`: Spectre runs successfully and produces `time`, `clk`, `vin`, `vout`, but the behavior checker fails with all sampled outputs at 0.000. This is a model behavioral failure.
- `vbr1_l1_first_order_lowpass:bugfix`: Spectre runs successfully and produces `time`, `vin`, `vout`, but the output is slower than the public envelope. This is a model behavioral failure or possible prompt-spec ambiguity around the expected time constant, not a simulator compatibility failure.
- `vbr1_l2_gain_extraction_convergence_measurement_flow:e2e`: EVAS rejects the generated `sin(2*`M_PI*fin*t)` expression area, while Spectre proceeds further but fails with convergence errors. This needs a smaller follow-up repro before assigning EVAS debt; it is not currently a clean Spectre PASS / EVAS FAIL.

## Interpretation

- The current v2 prompt structure is now less duplicated and has one shared place for Spectre-public formatting and artifact-contract rules.
- The common prompt does not ban EVAS false-negative features such as `laplace_nd()` or dynamic `timer()` periods.
- The fresh DeepSeek result set confirms that the renderer and API path work, but a simple one-shot baseline remains weak on these five tasks.
- The next evidence-producing step is not another prompt rerun; it is a focused failure audit:
  - classify each failure as model error, prompt/spec ambiguity, checker harshness, or EVAS false-negative;
  - inspect the CT01 bus/vector public interface because the model made a plausible but invalid interpretation;
  - decide whether CT04 should expose a more explicit public time-constant envelope or remain intentionally challenging;
  - distill SUP01 into a minimal EVAS parser repro only if a Spectre-passing variant still triggers the same EVAS parse failure.
