# Verilog-A Language-Semantics Extension Tasks

The default `tasks/` tree is now the standalone-Spectre-compatible v3
denominator:

- numbered default rows: `466`
- unnumbered replacement candidates: `0`
- archived Spectre-rejected rows: `54`

Numbering is intentionally non-contiguous while issue #109 replacement work is
in progress. The benchmark keeps the historical task ids, but rows that
Cadence/Spectre rejects as written are archived under
`spectre-unsupported-tasks/` and removed from `TASKS.json` and `CHECKS.yaml`.
See `reports/spectre_unsupported_removed_20260703.md` for the exact task list
and removal reason for each row.

This boundary is stricter than “EVAS can parse or run it”. A row belongs in the
default denominator only if it is intended to be legal in the current
standalone Spectre Verilog-A flow. Rows that require Verilog-AMS digital
semantics, a digital event kernel, unsupported user-task syntax, unsupported
runtime electrical-vector indexing, or version-gated system functions stay out
of the default EVAS/Spectre parity score.

## Default Coverage

Rows `001`-`300` remain the original behavior-certified surface with issue #109
backfills in the legacy gaps `052`-`057` and `075`. The old converter/vector
assets for those ids are archived, not deleted, because Spectre rejects their
procedural vector/electrical indexing patterns. The active `tasks/` ids now
point at reference-backed data-converter replacements.

Issue #109 also promotes seven former unnumbered bias/reference/power and
measurement candidates into the `495`-`501` holes as voltage-domain
replacements:
`495-supply-bias-validity-gate`,
`496-reference-settling-window-monitor`,
`497-power-enable-turnon-delay-gate`,
`498-power-mode-supply-current-metric`,
`499-dynamic-supply-level-driver`,
`500-rail-ramp-rate-startup-monitor`, and
`501-differential-common-mode-window-monitor`.

Issue #109 additionally replaces the archived user `task` / `endtask` holes
`373`-`378`, `421`, and `490` with Spectre-compatible voltage-domain
helper/monitor rows. These active rows use analog functions and event-body state
updates to model limiter recovery, sampled calibration/error updates, qualified
event-rate measurement, reset-release sequencing, adaptive threshold tracking,
rail-normalized metrics, affine calibration transforms, and PLL/clock
reacquisition lock detection.

Rows `301+` are language-extension candidates. The retained default rows cover
these Verilog-A-oriented surfaces:

- user-defined function declarations and calls
- `case` / `endcase` decoding
- `for`, `while`, and `repeat` loops that do not rely on Spectre-rejected
  runtime electrical indexing
- `initial_step`, `final_step`, `$fopen`, `$fwrite`, `$fclose`, `$fgets`,
  `$fscanf`, `$feof`, `$fseek`, `$ftell`, and `$rewind`
- `slew()`, `idtmod()`, `above()`, `last_crossing()`, `limexp()`, and selected
  continuous-time/KCL syntax rows that remain in the Verilog-A lane
- compiler directives and macro rows accepted by the current Spectre bridge
- parameter ranges, math functions, deterministic `$random`, seeded random
  helper rows that Spectre accepts, and `$bound_step`
- `white_noise()`, `flicker_noise()`, `noise_table()`, `analysis()`, and
  `ac_stim()` transient-compatible helper contracts
- one-dimensional and selected multi-dimensional `$table_model()` rows
- hierarchical module instantiation, named/ordered port maps, parameter
  overrides, and staged support artifacts
- scalar/vector arithmetic expressions that Spectre accepts as written
- string formatting/output rows that remain intended for Spectre-compatible
  syntax after audit cleanup
- Cadence helper calls such as `$vt`, `$temperature`, `$simparam()`,
  `$param_given()`, `$port_connected()`, conversion helpers, Monte Carlo/RF
  helper candidates, branch declarations, indirect branch syntax, and selected
  analog primitive/current-contribution rows

Default membership does not mean every retained extension row already has a
final passing Spectre behavior certificate. It means the row is not currently
classified as categorically outside standalone Spectre. Remaining Spectre
failures in retained rows should be treated as benchmark rewrites or
case-by-case EVAS/Spectre audit items, not as reasons to count unsupported
syntax in the default denominator.

The preprocessor/control rows `409-macro-functionlike-clamp`,
`410-macro-ifdef-gain-select`, `411-escaped-identifier-state`,
`412-initial-final-step-lifecycle`, `413-while-loop-array-sum`, and
`414-parameter-range-real-control` are retained as L0/support language-semantics
rows. They are not independent AMS circuit-function benchmarks, but their public
contracts now use the mandatory prompt shape and have EVAS2, Python EVAS,
targeted Spectre validation, and AHDL-like lint coverage for their support boundary.

As of the 2026-07-04 Spectre-parity audit, six retained rows are explicitly
marked `spectre-divergent` rather than full Spectre-certified:
`391-rdist-exponential-jitter`, `392-rdist-poisson-count-noise`,
`393-rdist-normal-offset-dither`, `396-rdist-erlang-latency`,
`404-vector-part-select-window`, and `405-vector-concat-code-build`. Spectre
compiles and simulates these rows, but EVAS/checker behavior was previously
using EVAS-side expectations for seeded random sequences, integer select and
concatenation semantics.
Their golden/checker contracts must be recalibrated against Spectre output
before they can be counted in a full Spectre-certified claim.

`492-kcl-inductor-idt-voltage` was restored after aligning EVAS branch-current
polarity for independent current sources with Spectre and lowering the
`V(p,n) <+ L*idt(I(p,n),0)` branch-current integral into `evas-rust`.

`494-continuous-zi-nd-filter` was restored after recalibrating the checker to
Spectre sampled `zi_nd()` values and adding `evas-rust` sample-interval
breakpoints so the operator updates at the exact configured interval even when
the netlist does not specify `maxstep`.

## Archived Rows

The 54 archived rows fall into these groups:

- Verilog-AMS/digital constructs outside standalone Spectre Verilog-A:
  `wreal`, `logic`, continuous `assign`, edge-triggered `always`,
  `connectmodule`, `connectrules`, `specify`, `specparam`, and packed logic
  bus rows.
- User `task` / `endtask` rows rejected by the current standalone Spectre
  compiler.
- Procedural or runtime vector/electrical indexing rows rejected by Spectre;
  static generate-style expansion is a separate, more constrained question.
- `$rdist_chi_square()` and `$rdist_t()` rows rejected by the current Spectre
  environment and therefore requiring version-gating before promotion.
- A small set of recursive-function, `do ... while`, and preprocessor-subset
  rows rejected by the current Spectre bridge.

Archived rows are preserved for future AMS/digital suites, version-gated
extensions, or deliberate EVAS extension-mode tests. They are not part of the
current default Spectre-compatible benchmark score.

## Certification Boundary

The original full-300 behavior claim should be read with the archived-row and
issue #109 notes above: seven historical support/vector assets are no longer in
the default Spectre-compatible denominator because Spectre rejects their syntax
as written, and their active ids now contain reference-backed data-converter
replacement tasks.

For the retained extension layer, continue to separate these claims:

- repository behavior-checker evidence
- EVAS Python/Rust execution evidence
- Spectre visible/hidden execution evidence
- continuous-time accuracy claims
- KCL/MNA solver claims

Continuous-time rows such as `ddt`, `idt`, Laplace, Z-domain, and `limexp`
remain a separate tier from event-style behavioral rows. KCL/current rows remain
a separate tier from pure voltage/event helper rows. Do not collapse those
layers into one “full behavior-certified” statement without matching Spectre
and checker evidence.
