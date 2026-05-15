# vaBench Main120 Review Samples

Date: 2026-05-13

## Purpose

This is the first manual review sheet for materializing `vabench-main-v1-main120`
from validated result evidence into source-controlled benchmark tasks. The goal
is to review five representative rows before scaling the same protocol to all
120 rows.

Scope clarification: main120 already has task-by-task reference/checker result
evidence. See `docs/VABENCH_MAIN120_REFERENCE_CHECKER_AUDIT.md`. The review
here is not asking whether the gold answers pass the current checker; it is
asking whether the release-facing `prompt.md`, `meta.json`, and `checks.yaml`
we materialize will faithfully describe that validated gold/checker contract.

The five samples cover all four task forms plus one PLL-clock/event-heavy case:

| Task ID | Form | Target family | Category | Why selected |
| --- | --- | --- | --- | --- |
| `vbm1_cdac_calibration_dut` | `dut` | `spec-to-va` | `dac` | Small calibration controller with bounded analog output. |
| `vbm1_offset_comparator_e2e` | `e2e` | `end-to-end` | `comparator` | Clocked comparator decision with offset threshold. |
| `vbm1_pfd_reset_race_bugfix` | `bugfix` | `bugfix` | `phase-detector` | Historical event-order/reset-race style risk. |
| `vbm1_file_metric_writer_tb` | `tb` | `tb-generation` | `measurement` | File I/O plus testbench-generation form. |
| `vbm1_vco_phase_integrator_e2e` | `e2e` | `end-to-end` | `pll-clock` | Timer-driven phase integration and edge-rate behavior. |

All five have EVAS PASS and Spectre PASS in the main120 gold evidence. Their
staged `.va`/`.scs` source files match between the EVAS and Spectre runs.

## Review Protocol

For each row, review these three source-task files:

1. `prompt.md`: user-visible task statement. It should specify behavior,
   ports, output file/module contract, and public evaluation observables without
   leaking the gold implementation.
2. `meta.json`: machine-readable task identity and promotion metadata. It
   should set `id`, `family`, `category`, `domain`, `difficulty`,
   `expected_backend`, `inputs`, `artifacts`, `scoring`, and `source_files`.
3. `checks.yaml`: public constraints and validation contract. It should include
   syntax guardrails, EVAS compile/sim axes, behavior-check intent, and Spectre
   parity evidence placeholders or paths.

The staged `.va`/`.scs` files are validated gold evidence, not by themselves a
release-quality benchmark source task.

## Sample 1: `vbm1_cdac_calibration_dut`

### Evidence

- Gold DUT: `cdac_calibration.va`
- Gold testbench: `tb_cdac_calibration_ref.scs`
- Module: `cdac_calibration(clk,rst,err,trim)`
- Key behavior: on rising `clk`, reset drives `trim` back to `0.45`; otherwise
  `err` increments/decrements an accumulator by `0.06`; output is clamped to
  `[0.05, 0.85]` and driven through `transition`.
- Testbench: `stop=220n`, `maxstep=500p`, saves `clk rst err trim`.
- Gold notes: `first=0.630 mid=0.570 late=0.630`.

### Draft Source-Task Shape

- `prompt.md`: ask for a voltage-domain CDAC calibration trim controller, not a
  full capacitor-array CDAC. This is important because current tracked
  `cdac_cal` is semantically different.
- `meta.json` seed:
  - `id`: `vbm1_cdac_calibration_dut`
  - `family`: `spec-to-va`
  - `category`: `dac`
  - `difficulty`: `easy` or `medium`
  - `artifacts`: `["cdac_calibration.va"]`
  - `scoring`: `["dut_compile", "tb_compile", "sim_correct"]`
- `checks.yaml` seed:
  - require `@(cross(`, `transition(`, clamping behavior, and no current
    contribution.
  - behavior check should cover reset, increment, decrement, and clamp windows.

### Human Review Questions

- Is the intended public task "CDAC calibration trim controller" rather than
  "10-bit CDAC model"?
- Should this be categorized as `dac`, `calibration`, or both via metadata tags?

## Sample 2: `vbm1_offset_comparator_e2e`

### Evidence

- Gold DUT: `cmp_offset_ref.va`
- Gold testbench: `tb_comparator_offset_ref.scs`
- Module: `cmp_offset_ref(VDD, VSS, CLK, VINP, VINN, OUT_P)`
- Key behavior: samples on rising `CLK`; outputs high when
  `VINP - VINN > vos`; default `vos=1m`; output uses rail-scaled `transition`.
- Testbench: `stop=28n`, `maxstep=20p`, saves `CLK VINP VINN OUT_P`.
- Gold notes: `clock_decisions=7`, `high_ok=1`, `low_ok=1`.

### Draft Source-Task Shape

- `prompt.md`: ask for an end-to-end clocked offset comparator plus reference
  testbench behavior; public contract should disclose clock, input swing around
  threshold, and required saved columns.
- `meta.json` seed:
  - `id`: `vbm1_offset_comparator_e2e`
  - `family`: `end-to-end`
  - `category`: `comparator`
  - `difficulty`: `easy`
  - `artifacts`: `["cmp_offset_ref.va", "tb_comparator_offset_ref.scs"]`
  - `scoring`: `["dut_compile", "tb_compile", "sim_correct"]`
- `checks.yaml` seed:
  - require `@(cross(` and `transition(`.
  - behavior check should verify both high and low sampled decisions.

### Human Review Questions

- Should the task expose `vos=1m` explicitly in the prompt, or only say
  "small positive input offset"?
- Should the module name be fixed to `cmp_offset_ref` or changed before release
  to a less gold-looking name?

## Sample 3: `vbm1_pfd_reset_race_bugfix`

### Evidence

- Gold DUT: `pfd_updn.va`
- Gold testbench: `tb_pfd_reset_race_ref.scs`
- Module: `pfd_updn(VDD, VSS, REF, DIV, UP, DN)`
- Key behavior: `REF` rising edge sets `UP`, `DIV` rising edge sets `DN`; when
  both states are high, both reset to zero. The testbench changes which clock
  leads halfway through the run.
- Testbench: `stop=300n`, `maxstep=10p`, `errpreset=conservative`, saves
  `ref div up dn`.
- Gold notes: first half has UP pulses, second half has DN pulses, overlap
  fraction is zero.

### Draft Source-Task Shape

- `prompt.md`: present a buggy PFD reset-priority/race implementation and ask
  for a fixed `pfd_updn.va`, or explicitly define the intended edge-reset
  semantics if the original buggy code cannot be restored.
- `meta.json` seed:
  - `id`: `vbm1_pfd_reset_race_bugfix`
  - `family`: `bugfix`
  - `category`: `phase-detector`
  - `difficulty`: `medium`
  - `artifacts`: `["pfd_updn.va"]`
  - `scoring`: `["dut_compile", "tb_compile", "sim_correct"]`
- `checks.yaml` seed:
  - require `@(cross(` and `transition(`.
  - must not allow UP/DN overlap after both events have occurred.
  - behavior check should count UP-leading and DN-leading windows separately.

### Human Review Questions

- Do we have the original buggy PFD code? If not, this may need to be converted
  from `bugfix` to a normal `spec-to-va` task or reconstructed carefully.
- Is simultaneous/near-simultaneous edge behavior in scope for the public
  benchmark, or should it be a conformance regression instead?

## Sample 4: `vbm1_file_metric_writer_tb`

### Evidence

- Gold DUT: `file_metric_writer.va`
- Gold testbench: `tb_file_metric_writer_ref.scs`
- Module: `file_metric_writer(vin,done)`
- Key behavior: opens `metric.out`, writes first crossing time when `vin`
  crosses `vth`, then drives `done` high.
- Testbench: `stop=90n`, `maxstep=500p`, saves `vin done`, drives a crossing
  at about `31n`.
- Gold notes: `pre=0.000 post=0.900`.

### Draft Source-Task Shape

- `prompt.md`: because the form is `tb`, the likely task should provide the DUT
  and ask for a testbench that exercises one threshold crossing and saves
  `vin done`.
- `meta.json` seed:
  - `id`: `vbm1_file_metric_writer_tb`
  - `family`: `tb-generation`
  - `category`: `measurement`
  - `difficulty`: `medium`
  - `artifacts`: `["tb_file_metric_writer_ref.scs"]`
  - `source_files`: `["gold/file_metric_writer.va"]`
  - `scoring`: `["dut_compile", "tb_compile", "sim_correct"]` if the file
    metric is scored; otherwise use compile/sim only and mark parity policy.
- `checks.yaml` seed:
  - require `ahdl_include`, `tran`, `save vin done`, and a PWL crossing.
  - behavior check should verify `done` is low before crossing and high after
    crossing; optional file-output check for `metric.out`.

### Human Review Questions

- Should `tb-generation` tasks in main120 include `sim_correct` when the DUT
  writes a file, or should they stay compile/smoke-only like some current
  tracked `tb-generation` tasks?
- Should `metric.out` be a checked artifact or only an internal side effect?

## Sample 5: `vbm1_vco_phase_integrator_e2e`

### Evidence

- Gold DUT: `vco_phase_integrator.va`
- Gold testbench: `tb_vco_phase_integrator_ref.scs`
- Module: `vco_phase_integrator(vctrl,phase,clk)`
- Key behavior: `timer(0,1n)` integrates phase by `0.03 + 0.09*V(vctrl)`;
  phase wraps at `1.0`; clock toggles on wrap.
- Testbench: `stop=180n`, `maxstep=500p`, saves `vctrl phase clk`, steps
  `vctrl` from `0.1` to `0.8` around `81n`.
- Gold notes: early edge count is lower than late edge count; phase span is
  about one cycle. For the discrete model, `timer(0,1n)` fires as part of the
  initial solve: with `vctrl=0.1`, the first saved `phase` is `0.039`, and the
  expected phase span is about `0.992`.

### Draft Source-Task Shape

- `prompt.md`: ask for a timer-driven behavioral VCO phase integrator with
  monotonic phase, wraparound, and clock edge rate controlled by `vctrl`.
- `meta.json` seed:
  - `id`: `vbm1_vco_phase_integrator_e2e`
  - `family`: `end-to-end`
  - `category`: `pll-clock`
  - `difficulty`: `medium`
  - `artifacts`: `["vco_phase_integrator.va", "tb_vco_phase_integrator_ref.scs"]`
  - `scoring`: `["dut_compile", "tb_compile", "sim_correct"]`
- `checks.yaml` seed:
  - require `@(timer(` and `transition(`.
  - behavior check should verify initial `timer(0,...)` phase update, phase
    span/wrap, and increased clock edge rate after the control voltage step.

### Human Review Questions

- Is a fixed 1 ns timer grid acceptable for the public EVAS subset claim?
- Should the prompt permit this discrete-time VCO approximation, or require a
  more continuous phase model?

## Shared Review Decisions

Before materializing all 120 rows, decide these policies:

1. Whether `bugfix` rows require recovered original buggy code. If not, convert
   some rows to `spec-to-va` instead of pretending a bugfix prompt exists.
2. Whether `tb-generation` rows require `sim_correct` by default, or only
   compile/run/parity smoke evidence.
3. Whether released module names should keep `_ref` suffixes from gold evidence
   or be renamed in the task prompt/gold files.
4. Whether behavior checker names in `checks.yaml` must correspond to concrete
   code paths before promotion, or can start as review labels.
