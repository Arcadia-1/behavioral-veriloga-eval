# ahdlLib to vaBench Coverage Review

Date: 2026-05-25

This note records a read-only inventory of the Cadence Virtuoso `ahdlLib`
available on `thu-sui` and maps it against the current paper-facing vaBench
release package. It is a coverage and task-design aid only. Do not import,
copy, or redistribute Cadence source code from this library.

## Source And Guardrails

| Item | Value |
| --- | --- |
| Remote host | `thu-sui` |
| Library path inspected | `/home/cadence/ICADVM/ICADVM201/tools.lnx86/dfII/samples/artist/ahdlLib` |
| Inspected mode | Read-only directory, cell-name, and text-pattern inventory |
| Direct source import | Forbidden |
| Allowed use | Coverage taxonomy, construct statistics, and clean-room task inspiration |
| Benchmark rule | Added tasks must be written from functional specifications, not copied code |

The release-facing vaBench goal is still an analog/mixed-signal Verilog-A
benchmark analogous to digital-domain VerilogEval/CVDP. `ahdlLib` is useful
because it gives an industrial reference distribution of behavioral modeling
idioms, but vaBench should not become a Cadence library extraction benchmark.

## ahdlLib Inventory Snapshot

The inventory found 171 cells with `veriloga` views and 513 Verilog-A-related
files under the inspected `ahdlLib` tree.

The following construct counts are quick text-scan indicators, not a formal
parser result:

| Construct family | File-level hits |
| --- | ---: |
| Voltage contribution style, `V(...) <+` | 135 |
| Current contribution style, `I(...) <+` | 22 |
| Charge contribution style, `Q(...) <+` | 1 |
| Continuous-time analog operators such as `ddt`, `idt`, `laplace`, `zi_`, `absdelay`, `table_model` | 40 |
| Event/transition family such as `cross`, `timer`, `transition`, `initial_step`, `final_step`, `$bound_step` | 112 |
| `cross` | 49 |
| `timer` | 25 |
| `transition` | 48 |
| `initial_step` | 95 |
| `final_step` | 17 |
| `$bound_step` | 12 |

A coarse EVAS-scope text filter found 112 cells that do not obviously contain
`I(...) <+`, `Q(...) <+`, `ddt`, `idt`, Laplace/ZI operators, `absdelay`, or
`table_model`, while still containing voltage contribution or event constructs.
This does not mean those cells are ready for EVAS; it means they are worth
clean-room review before any task design.

## Why Not Add Most Of The 171 Cells?

`ahdlLib` has many useful cells, but "useful as modeling evidence" is not the
same as "should become a scored vaBench entry." The release package should stay
compact and analog-IC-facing. The right target is to use the library to find
coverage gaps and weak tasks, then replace or refine selected vaBench entries.

| Bucket | Representative cells | Benchmark decision |
| --- | --- | --- |
| Already strongly covered by vaBench | `adc_8bit`, `dac_8bit`, `comparator`, `hysteresis`, `vco`, `phase_detector`, `charge_pump`, `sah_ideal`, `sampler` | Use for sanity checks and prompt/checker refinement. Do not add duplicates. |
| Valuable clean-room additions or replacements | `adc_dnl_8bit`, `adc_inl_8bit`, `dac_dnl_8bit`, `dac_inl_8bit`, `fullwave_rectifier_2p`, `halfwave_rectifier_2p`, `limiting_diffamp`, `lead_lag_compensator`, `swept_sine_src`, `varfreq_sin` | Candidate pool for a small replacement pass. These add real analog modeling value not fully emphasized in the current release. |
| Useful support/checker inspiration | `freq_meter`, `offset_meas`, `slew_rate_meas`, `find_slope`, `stat_probe`, `delta_probe`, `bit_error_rate` | Good for measurement semantics and checker audits. Keep mostly support-facing. |
| Mostly digital or RTL-like | `and_gate`, `or_gate`, `xor_gate`, `d_ff`, `jk_ff`, `serial_reg_8`, `parallel_reg_8`, `full_adder` | Exclude from scored analog benchmark unless embedded in a mixed-signal circuit flow. |
| Device/passive/current-domain primitives | `res`, `cap`, `ind`, `diode_simple`, `diode_sch`, `mos_level1`, `npn_bjt`, `cccs_hdl`, `vccs_hdl`, current clamps | Exclude from the current EVAS-aligned release. They require branch current/KCL/KVL or device semantics. |
| Non-IC physical-domain examples | `dc_motor`, `three_phase_motor`, `mass`, `spring`, `road`, `wheel`, `mag_core`, `mag_winding` | Exclude. They broaden the benchmark away from analog IC behavioral modeling. |
| Communication-system blocks | `qam_16ary_mod`, `qam_16ary_demod`, `qpsk_modulator`, `qpsk_demodulator`, `am_modulator`, `fm_modulator`, `pm_modulator` | Defer. They are interesting but would imply a new RF/communication behavioral category. |

The practical takeaway is: many ahdlLib cells are useful, but only a few should
enter the release because many are duplicates, outside scope, support-only, or
would require a new benchmark category.

## Current vaBench Coverage Baseline

Current release tracker: 64 entries, including 51 L1 entries and 13 L2 entries.

| vaBench category | Current entries | Current role |
| --- | ---: | --- |
| Data Converter Models | 13 | ADC/DAC, SAR, flash, compact pipeline residue, reconstruction chains |
| Comparator and Decision Circuits | 8 | Threshold, delay, hysteresis, window, offset, latch, offset measurement flow |
| PLL Clock and Timing Systems | 10 | VCO, PFD, bang-bang, divider, lock, charge pump, loop filter, ADPLL/CPPLL flows |
| Calibration, DEM, and Control | 7 | Trim, gain control, DEM/DWA, deadband, SAR calibration, shuffling, calibration loop |
| Measurement Instrumentation Flows | 7 | Crossing, settling, peak/gain, interval timing, measurement flows |
| Stimulus and Source Generators | 6 | PRBS, ramp/step, burst clock, dither/noise-like source, sine, sequencer |
| Baseband Signal Conditioning | 8 | Low-pass, resettable integrator, limiter, gain/PGA, higher-order filter, slew, chain |
| Sampling and Analog Memory | 5 | Aperture, droop/leakage, clocked S/H, acquisition limit, converter front-end |

## Category Mapping

| vaBench category | Existing coverage quality | ahdlLib names that map naturally | Action |
| --- | --- | --- | --- |
| Data Converter Models | Strong but converter-linearity tasks could be sharper. | `adc_8bit`, `adc_8bit_ideal`, `adc_dnl_8bit`, `adc_inl_8bit`, `dac_8bit`, `dac_8bit_ideal`, `dac_dnl_8bit`, `dac_inl_8bit`, `quantizer`, `sigmadelta_1storder` | Keep current core. Use INL/DNL cells as clean-room inspiration for checker/prompt strengthening or one future linearity-measurement L2. Keep sigma-delta deferred because it usually needs integration/continuous-time behavior outside the current EVAS mainline. |
| Comparator and Decision Circuits | Strong. | `comparator`, `hysteresis`, `deadband`, `deadband_diffamp`, `decider`, `crossing_detector`, `offset_meas` | No broad expansion needed. Use `deadband` and `offset_meas` to refine comparator nonidealities and measurement-flow wording. |
| PLL Clock and Timing Systems | Strong and well aligned with industrial library content. | `vco`, `dig_vco`, `pll`, `dig_pll`, `dig_pll_lpf`, `phase_detector`, `freq_ph_detector`, `charge_pump`, `single_shot` | Keep current coverage. Use ahdlLib only as a sanity check for the PFD/VCO/charge-pump/loop-filter decomposition. |
| Calibration, DEM, and Control | Adequate, but more controller/macromodel flavor is possible. | `p_controller`, `pi_controller`, `pd_controller`, `pid_controller`, `error_calc`, `tuning_res`, `untrimmed_res`, `untrimmed_cap`, `untrimmed_ind` | Do not add generic control tasks yet. Consider one future clean-room trim-element or error-to-trim loop only if it improves analog IC completeness without duplicating current calibration flow. |
| Measurement Instrumentation Flows | Strong support category; ahdlLib confirms this is a real Verilog-A usage pattern. | `freq_meter`, `voltmeter`, `ammeter`, `power_meter`, `qmeter`, `zmeter`, `offset_meas`, `slew_rate_meas`, `find_probe`, `find_slope`, `stat_probe`, `delta_probe` | Good source for L2/checker design. Keep these mostly support/non-core unless a measurement flow is circuit-facing and reusable. |
| Stimulus and Source Generators | Good, but swept/chirp behavior is an obvious industrial idiom. | `swept_sine_src`, `varfreq_sin`, `audio_src`, `three_phase_src`, `rand_bit_stream`, modulation source cells | Current programmable sequencer already covers ramp, sine, and burst/PRBS gating. A swept-sine/chirp extension is the cleanest possible future addition if stimulus coverage is judged thin. |
| Baseband Signal Conditioning | Good, but ahdlLib exposes more nonlinear and compensator-style blocks. | `amp`, `attenuator`, `limiting_diffamp`, `vargain_diffamp`, `vc_vg_diffamp`, `level_shifter`, `hard_voltage_clamp`, `soft_voltage_clamp`, `lpf_1storder`, `lead_compensator`, `lag_compensator`, `lead_lag_compensator`, `mixer`, `absolute_value`, `fullwave_rectifier_2p`, `halfwave_rectifier_2p`, `log_amp`, `polynomial` | Best area for selective improvement. Prefer one nonlinear conditioning task or one lead-lag/compensator task over increasing count broadly. |
| Sampling and Analog Memory | Strong. | `sah_ideal`, `sampler`, `switch_cap_integ` | Current S/H entries cover the important behavioral contracts. `switch_cap_integ` should be handled carefully because integrator behavior may cross the EVAS scope boundary. |

## Exclusion Buckets

These ahdlLib families should not enter the scored release as-is:

| Family | Examples | Reason |
| --- | --- | --- |
| Pure digital logic | `and_gate`, `or_gate`, `xor_gate`, `d_ff`, `jk_ff`, `serial_reg_8`, `parallel_reg_8`, `full_adder` | Duplicates digital VerilogEval-style scope and weakens analog benchmark positioning. Keep only when the logic is embedded in an analog-facing mixed-signal flow. |
| Device or passive primitives | `res`, `cap`, `ind`, `diode_simple`, `diode_sch`, `mos_level1`, `npn_bjt`, `n_jfet` | Often current/KCL/KVL or device-equation oriented; outside the current voltage-domain EVAS mainline. |
| Mechanical, magnetic, and physical-domain models | `dc_motor`, `three_phase_motor`, `mass`, `spring`, `road`, `wheel`, `mag_core`, `mag_winding` | Not central to analog IC behavioral Verilog-A benchmark claims. |
| Current-domain measurement/source blocks | `ammeter`, `current_dba`, `cccs_hdl`, `vccs_hdl`, current clamps | Useful Spectre examples but not directly compatible with the current EVAS scope. |
| Continuous-time solver-heavy blocks | `integrator`, `differentiator`, `sigmadelta_1storder`, many filter/compensator implementations | May require `idt`, `ddt`, branch behavior, or analog solver semantics; consider only after EVAS scope changes or with clean voltage-domain approximations. |

## Shortlist For Future Clean-Room Work

The best use of ahdlLib is not to expand the benchmark by dozens of entries.
It is to identify a small number of high-value replacements or refinements.

| Priority | Candidate task idea | ahdlLib inspiration | Suggested vaBench action |
| --- | --- | --- | --- |
| P1 | Converter static linearity measurement flow | `adc_dnl_8bit`, `adc_inl_8bit`, `dac_dnl_8bit`, `dac_inl_8bit` | Consider as a future L2 or checker-strengthening pass for Data Converter Models. This is more valuable than adding another basic DAC. |
| P1 | Nonlinear signal-conditioning block | `absolute_value`, `fullwave_rectifier_2p`, `halfwave_rectifier_2p`, `log_amp`, `limiting_diffamp` | Strong candidate if we need one more analog IC macromodel type. Prefer rectifier/envelope or limiting amplifier over generic math blocks. |
| P1 | Lead-lag or loop-compensator abstraction | `lead_compensator`, `lag_compensator`, `lead_lag_compensator` | Candidate replacement/addition under Baseband Signal Conditioning or PLL support if implemented in voltage-domain discrete/event style. |
| P1 | Swept-sine/chirp stimulus | `swept_sine_src`, `varfreq_sin` | Best stimulus improvement. Could extend the existing programmable sequencer instead of adding a new entry. |
| P2 | Deadband comparator/nonlinear amplifier behavior | `deadband`, `deadband_diffamp` | Existing comparator and calibration deadband tasks already cover part of this. Use mainly to sharpen specs. |
| P2 | Frequency/offset/slew measurement helpers | `freq_meter`, `offset_meas`, `slew_rate_meas`, `find_slope` | Use to improve measurement-flow semantics and checker audits, not necessarily to add scored core entries. |
| P2 | Trim-element macromodel | `tuning_res`, `untrimmed_res`, `untrimmed_cap`, `untrimmed_ind` | Only worth adding if framed as analog calibration hardware, not as passive primitive modeling. |
| P3 | Mixer/modulator/demodulator | `mixer`, `am_modulator`, `fm_modulator`, `qam_16ary_mod`, `qpsk_modulator` | Interesting but could broaden the benchmark into communication-system modeling. Defer unless we explicitly add an RF/communication behavioral category. |

## Current vaBench Risk Audit From ahdlLib

The current release categories are broadly reasonable, but ahdlLib exposes
several concrete risks in the current 64-entry package:

| Risk | Affected area | Why it matters | Preferred fix |
| --- | --- | --- | --- |
| Data converters may over-emphasize architecture variants and under-emphasize measurement goals. | Data Converter Models | `ahdlLib` contains explicit INL/DNL ADC/DAC models, while vaBench currently has many converter structures but no prominent static linearity measurement flow. | Add or replace with one clean-room converter INL/DNL measurement L2 task. |
| Signal conditioning is still too linear/basic. | Baseband Signal Conditioning | Industrial examples include rectifiers, log behavior, limiting amplifiers, clamps, lead-lag compensation, and nonlinear diffamps. | Replace one weak/basic conditioning row with nonlinear rectifier/envelope or limiting-amplifier behavior. |
| Stimulus coverage is close but should emphasize sweep semantics. | Stimulus and Source Generators | `swept_sine_src` and `varfreq_sin` are common reusable behavioral sources; current sequencer has ramp/sine/burst/PRBS but may not stress chirp/frequency continuity enough. | Extend `vbr1_l2_programmable_stimulus_sequencer` or replace a weaker source task with swept-sine/chirp behavior. |
| Measurement tasks could become support-only clutter if not tied to circuit decisions. | Measurement Instrumentation Flows | `ahdlLib` has many probes/meters. That validates the category, but reviewers may see it as testbench plumbing if scoring is not separated. | Keep support/core score separation explicit; use measurement entries to validate circuit-facing flows. |
| Some current categories contain digital-control-flavored entries. | PLL, Calibration/DEM, Stimulus | Digital-looking blocks can be justified only when they are analog-facing: SAR control, DEM for DAC mismatch, PFD/VCO timing, PRBS/dither stimulus. | Keep only analog-facing digital control. Do not add generic gates/registers from ahdlLib. |
| EVAS scope could hide valuable Spectre-only Verilog-A idioms. | Filters, integrators, device/passive models | Industrial Verilog-A often uses `I()<+`, `idt`, `ddt`, branch current, and continuous-time operators. vaBench intentionally excludes most of that today. | State this as a deliberate scope boundary, not as full Verilog-A coverage. Consider a future Spectre-only extension only after the current release is certified. |

## Recommended Next Step

Do not change the 64-entry release immediately. First use this review as an
audit lens:

1. Mark current entries that already align with ahdlLib industrial idioms.
2. Identify at most 3-5 weak or redundant current entries that could be replaced
   by stronger clean-room tasks.
3. Prefer replacements over count growth so the benchmark stays compact.
4. For each selected candidate, write a clean functional spec, public prompt,
   gold model, deterministic checker, and EVAS/Spectre validation plan.
5. Keep source provenance explicit: "inspired by public/installed library
   taxonomy; no proprietary source copied."

The current strongest candidate areas are nonlinear signal conditioning,
converter INL/DNL measurement flow, and swept-sine/chirp stimulus. The current
strongest "do not expand" areas are basic ADC/DAC, comparator, PLL timing, and
sample/hold, because vaBench already covers their main behavioral contracts.
