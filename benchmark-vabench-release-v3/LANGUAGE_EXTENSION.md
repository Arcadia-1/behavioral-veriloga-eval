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
- `301`-`420`: extension reference solutions are designed to parse and compile
  with current local EVAS, excluding known legacy non-Verilog-A harness/support
  targets outside the single reference-solution scan.
- `421`, `423`, `425`, `427`, `430`, `431`, `432`, and `433`: additional
  gap-fill rows that also compile with current local EVAS.
- `422`, `424`, `426`, `428`, `429`, and `434`: intentionally
  retained as `evas-unsupported-candidate` rows so the benchmark records manual
  syntax gaps even before EVAS supports them.
- `367`, `368`, `369`, `370`, and `372` were adjusted so `transition()` is no
  longer inside conditionally executed `analysis()` branches.

## Remaining Language Gaps Worth Tracking

Tracked upstream in EVAS issue #30.

The newly added rows avoid current-domain KCL and still leave some manual
features as future work:

- `$fscanf()` backend execution.
- `$sformat()` string formatting backend execution.
- `repeat` and `do ... while` loop syntax.
- `$rdist_uniform()` backend execution.
- richer multi-dimensional `$table_model()` behavior certification.
- broader AMS connect-module/connect-rule semantics.
- AC/noise behavior certification beyond compile-level helper coverage.
