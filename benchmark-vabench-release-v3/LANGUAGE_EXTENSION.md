# Verilog-A Language-Semantics Extension Tasks

Tasks `001` through `300` remain the original certified full-300 vaBench surface.
Tasks `301` onward are extension candidates added to cover behavioral Verilog-A
and Verilog-AMS language features called out by the Cadence Verilog-A Language
Reference and the local training material.

These extension tasks keep the same behavioral boundary as the benchmark: no
transistor-level devices and no current contribution through `I(...)`. The AMS
rows intentionally exercise digital/mixed-signal syntax (`logic`, `wreal`,
`assign`, `always`) because practical behavioral models often need that surface.

## Coverage Added

- `301`-`305`: user-defined `function` declarations and calls.
- `306`-`310`: `case` / `endcase` mode decoding.
- `311`-`315`: `for` loops with small array state.
- `316`-`320`: `final_step`, `$fopen`, `$fwrite`, `$fclose`, and `$strobe`.
- `321`-`325`: `slew()` voltage-domain output limiting.
- `326`-`330`: `idtmod()` wrapped phase accumulation.
- `331`-`335`: `above()` and `last_crossing()` threshold timing.
- `336`-`340`: compiler directives, parameter ranges, math functions,
  deterministic `$random`, and `$bound_step`.
- `341`-`360`: Verilog-AMS `wreal`, `logic`, continuous `assign`, edge-triggered
  `always`, and mixed electrical/digital bridge tasks.
- `361`-`372`: `white_noise()`, `flicker_noise()`, `noise_table()`, `analysis()`,
  and `ac_stim()`.
- `373`-`378`: user-defined `task` declarations and calls.
- `379`-`384`: file-read and file-positioning helpers including `$fgets()`,
  `$feof()`, `$fseek()`, `$ftell()`, `$rewind()`, and `$fopen()` mode handling.
- `385`-`390`: one-dimensional `$table_model()` lookup tasks.
- `391`-`396`: seeded random distributions: `$rdist_exponential()`,
  `$rdist_poisson()`, `$rdist_normal()`, `$rdist_chi_square()`, `$rdist_t()`, and
  `$rdist_erlang()`.
- `397`-`402`: hierarchical module instantiation, named/ordered port maps, and
  parameter override patterns.
- `403`-`408`: bit-select, part-select, concatenation, replication, reduction,
  and shift/mask vector expressions.
- `409`-`414`: function-like macros, `ifdef` selection, escaped identifiers,
  combined `initial_step`/`final_step`, `while` loops, and parameter ranges.
- `415`-`420`: additional digital/mixed-signal vector, reduction, `always`,
  `wreal`, and electrical-to-logic bridge rows.
- `421`-`434`: explicit gap-fill rows for task-local variables, `$fscanf()`,
  combined file replay, string formatting with `$swrite()` / `$sformat()`,
  seed reproducibility, staged hierarchy, `ifndef` / `elsif` / `undef`, and
  `repeat` loops.
- `435`-`458`: manual syntax-completion rows for `ddt()`, `idt()`, Laplace
  filters, Z-domain filters, `limexp()`, `$fstrobe()`, system output calls,
  `$rdist_uniform()`, `generate` / `genvar`, custom nature/discipline,
  `connectmodule` / `connectrules`, `specify` / `specparam`, multi-dimensional
  arrays, packed bus declarations, analog event-or expressions, nested
  functions, and recursive function candidates.
- `459`: explicit `do ... while` control-flow candidate.
- `460`-`470`: course-material gap-fill rows for `analog initial`, `$vt`,
  `$discontinuity`, `$param_given()`, `$port_connected()`, `$temperature`,
  `$simparam()`, explicit `branch` declarations, and `I(...)` current
  contribution syntax.
- `471`-`494`: LRM gap-fill rows for indirect branch assignments,
  attribute/access functions, OOMR and alias helpers, inherited port/m-factor
  attributes, analog primitive instantiation, Cadence assert/conversion/Monte
  Carlo/RF helpers, 2D/string `$table_model()`, deeper analog event
  expressions, KCL `ddt`/`idt` current/voltage forms, and explicit
  continuous-time Laplace/Z-domain tier rows.

Each extension task contains:

- `instruction.md`
- `solution/`
- `starter/`
- `test_visible/`
- `test_hidden/`
- `test_harness/visible_hidden_manifest.json`
- five concrete negative variants under `negative_variants/`

## Certification Boundary

The extension tasks are marked as candidate rows in `TASKS.json` and
`CHECKS.yaml`. They are not part of the original full-300 certification claim.
Before any paper-facing full-suite claim, promote only the rows whose reference
solutions, hidden checks, and five negative variants are behavior-certified.

Current local EVAS compile status after this expansion:

- `001`-`300`: unchanged original benchmark surface.
- `301`-`459`: extension reference solutions currently parse and compile with
  local EVAS.
- `435`-`445`, `451`, `454`, and `458`: previously tracked as unsupported, but
  now compile with current local EVAS.
- `461`, `463`, `466`, `468`, `469`, and `470`: course-material gap-fill rows
  that currently compile with local EVAS.
- `460`, `462`, `464`, `465`, and `467`: course-material environment
  helper rows that now compile with current local EVAS.
- `471`-`494`: newly added LRM gap-fill rows; all reference solutions now
  compile with current local EVAS after the EVAS CLI helper allowlist update.
- `471`, `472`, `493`, and `494`: behavioral continuous-time candidates;
  these are compile-supported language rows, not full dynamic-solver accuracy
  claims.
- `469`, `470`, `481`, `482`, `491`, and `492`: KCL/current-contribution or
  analog-primitive syntax candidates only; they are not behavior-certified
  KCL/MNA claims.
- `367`, `368`, `369`, `370`, and `372` were adjusted so `transition()` is no
  longer inside conditionally executed `analysis()` branches.

## Remaining Language Gaps Worth Tracking

Upstream EVAS issues #35 and #36 are closed. The rows below are now
compile-supported by current local EVAS, but remain extension candidates until
their behavior checkers and negative-case scoring are promoted.

The newly added rows avoid current-domain KCL and still leave some manual
features as future work:

- behavior certification, beyond compile support, for indirect branch assignment,
  attribute/generic access functions, `$analog_node_alias`, `$rtoi`,
  `$cds_get_mc_trial_number`, 2D/string `$table_model`, and continuous-time
  `ddt`/`idt`/`laplace_nd`/`zi_nd` rows.
- richer multi-dimensional `$table_model()` behavior certification.
- AC/noise behavior certification beyond compile-level helper coverage.
