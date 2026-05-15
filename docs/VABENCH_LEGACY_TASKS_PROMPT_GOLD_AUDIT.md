# Legacy `tasks/` Prompt-Gold Audit

Date: 2026-05-13

Scope: legacy source-controlled `tasks/` set, 92 tasks.

Important scope note: this is **not** the current vaBench mainline. The current
mainline remains `vabench-main-v1-main120` materialization plus follow-on
benchmark expansion. The 92-task `tasks/` tree is a legacy/supporting set that
is useful for finding prompt/checker hygiene issues, but it should not be used
as the paper-facing benchmark count or mainline progress metric.

Question: does the legacy `tasks/` tree contain examples of the same class of
problem as the main120 CDAC example, where the public prompt asks for one
semantic target but the gold/checker actually validate another target?

## Summary

No reviewed legacy `tasks/` item appears to have a hard functional swap as severe as
"prompt asks for a full CDAC, gold/checker validate only a trim controller."

There are, however, release-blocking prompt/checker contract risks:

- Some prompts contain semantic wording that conflicts with the pure
  voltage-domain benchmark scope or with the gold behavior.
- Some `checks.yaml` files require tokens that the gold answer itself does not
  contain.
- Several `tb-generation` prompts contain duplicated DUT-instantiation lines.
- Six tasks still use `manual_review_expected_output`, so their behavioral
  contract is not yet public/checker-grade.

The existing prompt-contract audit still passes on this legacy tree:

```text
python3 runners/audit_prompt_contracts.py --output-dir results/prompt-contract-audit-current-2026-05-13
[prompt-audit] tasks=92 P0=0 P1=0 P2=92
```

That audit is useful for hard syntax/contract corruption, but it does not catch
the semantic overreach and prompt-gold intent issues below.

## Confirmed Contract Risks

| Severity | Task | Issue | Evidence | Recommended fix |
| --- | --- | --- | --- | --- |
| P1 | `tasks/spec-to-va/voltage/dac/segmented_dac` | Prompt says "Differential current-steering output", while `checks.yaml` forbids `I(` and the gold implements voltage outputs `VOUT_P/VOUT_N`. | Prompt asks for current-steering; gold comment says "behavioral model: voltage output"; `must_not_include: I(`. | Rewrite prompt as a pure voltage-domain behavioral approximation of a segmented current-steering DAC. |
| P1 | `tasks/spec-to-va/voltage/dac/cdac_cal` | Prompt asks for top-plate/bottom-plate charge redistribution with redundant calibration capacitors, but gold is a simplified voltage-domain code plus calibration offset model. | Gold computes `code + 32 * cal` and drives `VDAC_P/VDAC_N`; no explicit capacitor network; checker is manual. | Clarify that the task is a behavioral SAR CDAC transfer model, or strengthen the checker if physical charge-redistribution semantics are intended. |
| P1 | `tasks/end-to-end/voltage/sample_hold_smoke` | Prompt first specifies rising-edge sampling, then says `sample=high` tracks and `sample=low` holds, even though no `sample` port exists and gold is edge-triggered. | Prompt expected behavior conflicts with its own clocked-edge spec; gold samples on `@(cross(V(CLK)-vth,+1))`. | Remove level-sensitive `sample=high/low` wording and state rising-edge sample/hold only. |
| P1 | `tasks/bugfix/voltage/wrong_edge_sample_hold_bug` | Prompt says "correct clock edge (rising or falling per spec)" instead of explicitly naming the intended edge; ports section is duplicated/corrupted. | Buggy code samples on falling edge; gold fixes to rising edge. | State "fix falling-edge sampling to rising-edge sampling" and clean the port list. |
| P1 | `tasks/end-to-end/voltage/d2b_4bit_smoke` | `checks.yaml` requires `V(DOUT[`, but prompt and gold use scalar ports `DOUT3..DOUT0`. | Gold drives `V(DOUT3)`, `V(DOUT2)`, `V(DOUT1)`, `V(DOUT0)`. | Replace the token check with scalar-port checks or change the task to a true bus contract. |
| P1 | `tasks/spec-to-va/voltage/adc-sar/d2b_4bit` | `checks.yaml` requires `genvar`, but prompt does not require it and gold does not use it. | Gold is scalar/timer-based; `must_include: genvar`. | Remove `genvar` from required syntax or change gold/prompt consistently. |
| P1 | `tasks/spec-to-va/voltage/adc-sar/sar_logic` | `checks.yaml` requires `genvar`, but gold does not use it. | Gold uses explicit scalar outputs and integer arrays; `must_include: genvar`. | Remove `genvar` from required syntax or make the public contract explicitly array/generate based. |
| P2 | `tasks/end-to-end/voltage/dac_binary_clk_4b_smoke` | Prompt mixes public node names `rdy/din*/aout` with module port names `CLK/DIN*/AOUT`. Gold is aligned through positional instantiation, but the prompt can confuse authors. | Testbench instantiates `(din3 din2 din1 din0 rdy aout)` into module port `CLK`. | Make the prompt say module port `CLK` is driven by public stimulus node `rdy`, or use one name consistently. |

## Prompt Duplication Issues

These are not prompt-gold semantic swaps, but they are clear prompt corruption
and should be cleaned before release:

| Task | Repeated line |
| --- | --- |
| `tasks/tb-generation/voltage/clk_div_min_tb` | `DUT module to instantiate: clk_div_min` repeated 13x; `RST_N` and `CLK_OUT` port lines repeated 11x. |
| `tasks/tb-generation/voltage/comparator_offset_tb` | `DUT module to instantiate: cmp_offset_ref` repeated 13x. |
| `tasks/tb-generation/voltage/dac_ramp_tb` | `DUT module to instantiate: dac_ramp_ref` repeated 13x. |
| `tasks/tb-generation/voltage/dco_gain_step_tb` | `DUT module to instantiate: dco_gain_step_ref` repeated 13x. |
| `tasks/tb-generation/voltage/gain_step_tb` | `DUT module to instantiate: gain_step_ref` repeated 13x. |
| `tasks/tb-generation/voltage/nrz_prbs_jitter_tb` | `DUT module to instantiate: nrz_prbs_jitter_ref` repeated 13x. |
| `tasks/tb-generation/voltage/sample_hold_aperture_tb` | `DUT module to instantiate: sample_hold_aperture_ref` repeated 13x. |
| `tasks/tb-generation/voltage/sample_hold_step_tb` | `DUT module to instantiate: sample_hold_step_ref` repeated 13x. |
| `tasks/tb-generation/voltage/segmented_dac_glitch_tb` | `DUT module to instantiate: segmented_dac_glitch_ref` repeated 13x. |
| `tasks/tb-generation/voltage/testbench/inl_dnl_probe` | `DUT module to instantiate: dac_for_probe` repeated 13x. |
| `tasks/tb-generation/voltage/xor_phase_tb` | `DUT module to instantiate: xor_phase_ref` repeated 13x. |

## Manual Behavior Checks Still Present

These tasks cannot yet be treated as release-quality public behavioral
contracts without replacing the placeholder with concrete checker labels:

- `tasks/spec-to-va/voltage/dac/segmented_dac`
- `tasks/spec-to-va/voltage/dac/cdac_cal`
- `tasks/spec-to-va/voltage/adc-sar/d2b_4bit`
- `tasks/spec-to-va/voltage/adc-sar/sar_12bit`
- `tasks/spec-to-va/voltage/adc-sar/pipeline_stage`
- `tasks/spec-to-va/voltage/adc-sar/sar_logic`

## Reviewed False Positives

The semantic heuristic also flagged several candidates that appear aligned after
manual review:

- `dac_binary_clk_4b_smoke`: behavior is a real 4-bit clocked DAC; only naming
  cleanup is needed.
- `dac_ramp_tb`: prompt and gold are aligned; duplicated DUT line is the issue.
- `pipeline_stage`: `1.5-bit` was misread by the heuristic as `5-bit`; gold is
  a matching 1.5-bit pipeline stage.
- `sar_12bit`, `sar_logic`, `sar_logic_10b`: prompt/gold are semantically
  aligned despite non-`D0..Dn` output naming.
- `bbpd`, `bg_cal`: generic words such as comparator/phase detector caused
  false positives; gold matches the stated task.
- `prbs7`, `therm2bin`: prompt ports and gold ports align.
- `sample_hold_step_tb`: prompt/gold align apart from duplicated DUT line.

## Recommended Cleanup Order

1. Fix concrete `checks.yaml` vs gold contradictions:
   `d2b_4bit_smoke`, `adc-sar/d2b_4bit`, `adc-sar/sar_logic`.
2. Rewrite the prompt wording risks:
   `segmented_dac`, `cdac_cal`, `sample_hold_smoke`,
   `wrong_edge_sample_hold_bug`, `dac_binary_clk_4b_smoke`.
3. Deduplicate the 11 `tb-generation` prompts.
4. Replace all `manual_review_expected_output` placeholders with concrete
   public behavior-check labels.
5. Re-run EVAS gold validation and, for promoted tasks, Spectre parity.
