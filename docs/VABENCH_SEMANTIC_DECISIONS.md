# vaBench Semantic Decision Table

Date: 2026-05-14

Purpose: collect benchmark-semantic decisions that require human review before
main120 evidence is promoted into release-facing vaBench source tasks. This file
is intentionally separate from implementation logs: it records what the
benchmark should mean, not merely what currently passes.

## Decision Status Legend

| Status | Meaning |
| --- | --- |
| `proposed` | Current technical recommendation; needs human acceptance before it becomes policy. |
| `accepted` | Approved benchmark policy. |
| `accepted-with-validation` | Approved policy, but exact thresholds or examples still need fresh validation before release counting. |
| `needs-review` | Requires manual inspection of examples or paper framing. |
| `blocked` | Cannot be finalized until missing source/evidence is recovered. |

## Top-Level Decisions

| ID | Topic | Current Recommendation | Why It Matters | User Review Needed | Status |
| --- | --- | --- | --- | --- | --- |
| D001 | Release checker observables | Release-facing checkers should not rely on raw CSV row counts, row fractions, or final-row samples at source/clock transition boundaries. Use fixed safe sample points, state sequences, edge counts, time-weighted durations, or tolerance windows. | Prevents a task from passing while measuring simulator output-grid artifacts instead of circuit behavior. | Apply as a hard benchmark rule during materialization. | accepted |
| D002 | Missing badcase in `bugfix` rows | Do **not** automatically relabel a fixed-source-only historical `bugfix` row as `spec-to-va` or `e2e`. Instead mark it as `repair_provenance_incomplete` until a release form is chosen. | A missing-badcase repair task is not semantically identical to a normal spec task or an end-to-end task. Blind relabeling would hide provenance loss. | Decide which release forms are allowed for these rows. | accepted |
| D003 | Valid `bugfix` release form | A release-facing `bugfix` task should normally include a buggy input and a fixed expected contract. The checker should distinguish badcase failure from goodcase success when possible. | A bugfix benchmark tests repair ability, not just implementation ability. | Treat badcase+goodcase as the default public bugfix standard. | accepted |
| D004 | Historical repair without badcase | For fixed-source-only historical `bugfix` rows, first attempt to reconstruct a minimal single-cause buggy source and keep the row as `bugfix` once bad/fixed evidence is verified. Move EVAS/Spectre semantic cases to a separate conformance suite. Use behavior-regression or evidence-only only as fallback. | Preserves the repair benchmark claim without hiding missing provenance or mixing simulator conformance with model capability. | Apply per-row reconstruction review during materialization. | accepted |
| D005 | P2 tolerance policy | P2 cases should not trigger EVAS kernel changes unless binary behavior changes: edge/pulse counts diverge, state order changes, reset/decision polarity changes, or numeric drift exceeds documented tolerance. Exact edge/pulse/state assertions stay exact; continuous metrics use documented windows. | Avoids overfitting EVAS to Spectre's accepted-point sampling while still blocking real behavior mismatches. | Validate representative P2 cases before release counting. | accepted-with-validation |
| D006 | StrongARM final-boundary behavior | Ordinary benchmark tasks should avoid stopping exactly at source/clock transition boundaries. Boundary behavior belongs in atomic EVAS/Spectre conformance regressions outside normal vaBench task counts. | Keeps normal benchmark tasks stable while still testing simulator semantics separately. | Apply during task materialization. | accepted |
| D007 | Prompt specificity vs checker observables | Prompts should specify intended circuit behavior, ports, artifacts, and public observables, but should not leak gold implementation details, exact thresholds chosen only for checker convenience, or checker internals. | Balances benchmark fairness with checker reproducibility. | Manual prompt review per promoted task. | accepted-with-validation |
| D008 | main120 promotion order | Materialize schema/promotion contract first, then P1/D001 rows, D004 pilot bugfix reconstructions, standalone conformance pack, P2 tolerance rows, and finally the rest of main120 in 20-40 task batches. | Lets the known-risk rows define the benchmark policy before scaling. | Use this as the default work order. | accepted |
| D009 | Historical `thermometer_dac` naming | Keep `vbm1_thermometer_dac_bugfix` as the traceable main120 id, but describe the public task as a 4-bit binary DAC because the source uses binary-weighted `code_0..code_3`. Add a separate 4-bit thermometer DAC task with 15 segments when expanding benchmark coverage. | Prevents prompt/gold semantic mismatch while preserving historical evidence traceability. | New thermometer DAC task should explicitly expose or internally model 15 unit segments. | accepted |
| D010 | Duplicate calibration sign bug | `background_calibration_accumulator` and `cdac_calibration` share the same reset/clock/error/clamp accumulator kernel. Count only `cdac_calibration` as the current sign-direction bugfix; keep `background_calibration_accumulator` as evidence-only until a distinct defect is designed. Apply the same rule to other isomorphic kernels. | Avoids inflating bugfix diversity with two near-isomorphic repair tasks. | When expanding later, design different-root-cause cases instead of reusing the same repair pattern. | accepted |
| D011 | Measurement/file/VCO historical bugfix rows | Keep `file_metric_writer`, `settling_time_measurement_tb`, and `vco_phase_integrator` out of public bugfix counts by default. Their functions may still become `spec-to-va`, `tb-generation`, or `end-to-end` benchmark tasks when framed as normal implementation/measurement problems. | Prevents tool-conformance and measurement tasks from inflating model-repair claims while preserving useful benchmark coverage. | Move atomic simulator semantics into conformance; materialize normal tasks only under the appropriate non-bugfix family. | accepted |
| D012 | P2 functional badcase split | `leaky_hold`, `one_shot_timer`, and `track_hold_aperture` may be reconstructed as bugfixes only when the badcase is a functional one-root-cause defect checked in safe windows. Their exact timer/startup/aperture boundary semantics remain separate conformance watch items. | Preserves useful repair tasks without overfitting the benchmark to simulator accepted-point behavior. | EVAS and Spectre fixed-pass/buggy-fail confirmation completed on 2026-05-15; keep boundary semantics in conformance. | accepted |

## D002/D003/D004: Bugfix Rows With Missing Badcase

The earlier shorthand "reclassify to `spec-to-va` or `e2e`" is too coarse.
There are at least four distinct release options:

| Option | Name | Public Input | What It Tests | Pros | Risks | Recommended Use |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | True bugfix | Buggy source + prompt describing the defect | Ability to repair a concrete implementation | Cleanest benchmark semantics; comparable to software/hardware repair literature | Requires reconstructing or recovering a realistic badcase | Use when original or minimal buggy source is available. |
| B2 | Behavior-regression task | Behavioral spec + gold/testbench/checker; no buggy source | Ability to implement the corrected behavior that historically caused failures | Honest when badcase is missing; still useful for benchmark coverage | Not a repair task; should not be counted as bugfix capability | Use when the intended behavior is clear but buggy provenance is gone. |
| B3 | Separate conformance asset | Minimal DUT/TB designed around one failure mode under the EVAS/Spectre conformance suite | Simulator/checker semantic, not model repair | Good for EVAS/Spectre diagnostics | Must not be counted as normal vaBench model capability | Use for event ordering, syntax, source-boundary, or solver semantics. |
| B4 | Evidence-only row | Existing fixed gold + validation evidence only | Internal provenance / historical result | Avoids dishonest release | Not a public task yet | Use until a reviewer approves B1/B2/B3. |

Recommended policy:

1. If a bugfix row has both badcase and goodcase, keep `family=bugfix`.
2. If a bugfix row has only fixed gold but the original defect can be
   reconstructed as a small, realistic one-line or one-concept bug, promote it
   as B1 after manual review.
3. If the fixed-only row is actually about EVAS/Spectre semantics, move it into
   the separate conformance suite rather than the normal vaBench model
   benchmark. Do not encode this as `release_form=conformance-style` inside a
   normal vaBench task.
4. If the defect cannot be reconstructed honestly, do not call it `bugfix`.
   Promote as B2 only if the task is still valuable as a normal behavior
   implementation problem. Treat B2 as a fallback release form with provenance,
   not as a new primary family.
5. If neither B1 nor B2 is clearly appropriate, keep it B4 evidence-only.

Buggy source reconstruction rule:

- The reconstructed badcase must be a small, realistic one-root-cause defect
  that a human Verilog-A author or LLM plausibly makes for this task.
- The public checker must fail the buggy source and pass the fixed source.
- For behavioral bugfixes, both EVAS and Spectre should fail the buggy source
  on the public checker and pass the fixed source before the task is counted as
  public bugfix capability. Syntax bugfixes must state backend-specific compile
  expectations explicitly.
- The prompt must describe the defect to repair without leaking the exact patch.
- Metadata should record `badcase_origin: reconstructed` and the original
  `source_main120_id`.
- Do not invent a contrived bug just to preserve a `bugfix` label.

## D001: Checker Observable Policy

| Unsafe Observable | Why Unsafe | Preferred Replacement | Example |
| --- | --- | --- | --- |
| Raw high-sample count | EVAS and Spectre can save different numbers of accepted transient points. | Fixed safe-time state sequence or time-weighted duration. | `element_shuffler`, `rotating_element_selector` |
| `high rows / total rows` | Depends on output grid density near transitions. | Time-weighted high fraction, pulse width, or edge count. | `edge_detector`, `one_shot_timer`, `lock_detector` |
| Final row at source edge | Simulator endpoint/breakpoint policy can differ. | Stop away from transitions, or sample before/after explicitly. | `strongarm_comparator_behavior` |
| Exact note-string equality | Notes are diagnostic strings, not a semantic contract. | Structured metric comparison with tolerance. | lowpass/integrator/decay rows |

## D005: P2 Escalation Rules

P2 should stay tolerance/watchlist unless one of these happens:

| Escalation Trigger | Action |
| --- | --- |
| EVAS PASS / Spectre FAIL or Spectre PASS / EVAS FAIL on the same audited source task | Treat as P0/P1 depending on root cause; block promotion until explained. |
| Edge/pulse count changes | Add atomic event regression; inspect EVAS event scheduling or checker thresholding. |
| State sequence/order changes | Treat as behavior mismatch; inspect DUT semantics and checker. |
| Reset/decision polarity changes | Treat as behavior mismatch; inspect EVAS kernel/checker first. |
| Continuous metric exceeds declared tolerance by a meaningful margin | Add focused conformance or numeric regression before changing EVAS. |
| Same numeric drift repeats across a family of related kernels | Promote from watchlist to conformance investigation. |

Default interpretation:

- Edge count, pulse count, state order, reset polarity, and decision polarity are
  exact semantic checks, not tolerance checks.
- Continuous-valued metrics such as phase span, settling value, decay envelope,
  or window mean may use documented voltage/time/relative tolerances.
- Any sample helper used by release checks must reject out-of-range sample
  times instead of extrapolating from the first or last saved row.
- If a P2 case depends on accepted-point density, add a watchlist note or a
  conformance regression before changing the EVAS kernel.

## D006: Boundary and Conformance Split

Normal benchmark tasks should represent stable circuit behavior. They may use
source edges and clock events, but their release pass/fail decision should not
depend on the final saved point being exactly at a source or clock transition.

Boundary-sensitive questions are still important for EVAS, but they belong in a
separate EVAS/Spectre conformance asset with:

- `asset_type: evas_spectre_conformance`;
- one named semantic axis;
- explicit expected EVAS/Spectre relation;
- diagnostic log or waveform signature when the expected result is rejection;
- hard exclusion from vaBench model-capability counts.

## D007: Prompt Review Rule

Promoted source tasks need enough public specificity to make the intended
behavior clear without making the checker a hidden reverse-engineering puzzle.
The prompt should include:

- circuit role and behavioral contract;
- port names, directions, electrical discipline assumptions, and artifact name;
- public observables used for evaluation, such as sampled output sequence,
  pulse count, settling window, or file metric;
- allowed tolerance language when the task is continuous-valued.

The prompt should not include:

- gold implementation structure such as private state variable names;
- exact transition smoothing constants unless they are part of the public
  problem;
- checker-only sample times or thresholds that are not part of the circuit
  specification;
- historical notes that reveal the intended patch.

## D008: Promotion Order

The accepted promotion order is:

1. Freeze schema/materialization metadata and count filters.
2. Promote the D001/P1 checker-risk rows.
3. Reconstruct and review the first D004 bugfix pilot rows.
4. Create the standalone EVAS/Spectre conformance pack.
5. Promote D005/P2 tolerance-risk rows with documented metric helpers.
6. Promote the remaining main120 rows in 20-40 task batches.

## D011: P1 Measurement and Startup Rows

These rows pass EVAS and Spectre in historical main120 evidence, but their
historical `*_bugfix` rows should not be counted as public `bugfix` unless a
separate functional defect is reconstructed and reviewed. This does **not** mean
the functions are useless. The same base circuits can still be promoted through
their non-bugfix forms (`dut`, `tb`, or `e2e`) or through separately designed
normal tasks.

| Task ID | Current Source Behavior | Why It Is Not a Clean Bugfix | Recommended Release Path |
| --- | --- | --- | --- |
| `vbm1_file_metric_writer_bugfix` | Uses `$fopen` at `initial_step`, `$fwrite` at the first rising `vin` crossing, and a `done` voltage flag. | The meaningful risk is file I/O/final output semantics; the current checker only observes `done`, while the output artifact is tool behavior. | Do not count the historical row as bugfix. Promote as `tb-generation`/measurement only if public file-output semantics are explicitly part of the benchmark; keep atomic `$fopen/$fwrite` behavior in conformance. |
| `vbm1_settling_time_measurement_tb_bugfix` | Timer-driven first-order response with `done` asserted after `$abstime > 120n` and `y > 0.75`. | It is a generated measurement/testbench model, not a DUT repair pair. The natural defects are threshold/window/reporting defects rather than circuit implementation bugs. | Do not count the historical row as bugfix. Promote as `tb-generation` or `e2e` measurement task if the public goal is settling-time checking; keep threshold/window edge semantics in conformance if needed. |
| `vbm1_vco_phase_integrator_bugfix` | `timer(0,1n)` updates phase by `0.03 + 0.09*V(vctrl)` and toggles `clk` on phase wrap. | We already observed the EVAS/Spectre startup difference: Spectre samples `phase=0.039` at `t=0`, while EVAS starts at `0`. That is timer/initial scheduling semantics. | Do not count the historical row as bugfix. Promote the VCO function as `spec-to-va` or `e2e` using safe post-startup metrics; keep `timer(0)` startup in EVAS/Spectre conformance. |

## Immediate Review Queue

| Priority | Decision | Suggested Next Action |
| --- | --- | --- |
| 1 | Schema/count contract | Add machine checks for vaBench-vs-conformance asset separation and required provenance fields. |
| 2 | D004 pilot badcases | Review 3-5 reconstructed missing-badcase main120 bugfix rows before scaling. |
| 3 | D005 validation | Run representative P2 tolerance rows through EVAS/Spectre before release counting. |
| 4 | D007 prompt review | Review prompts for P1/P2-exposed rows before scaling materialization. |
| 5 | Report denominators | Report both row-level and base-clustered statistics so the four main120 forms do not overstate independence. |
