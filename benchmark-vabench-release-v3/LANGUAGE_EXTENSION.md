# Verilog-A Language-Semantics Extension Tasks

Tasks `001` through `300` remain the original certified full-300 vaBench
surface. Tasks `301` through `340` are extension candidates added to cover
behavioral Verilog-A language features called out by the Cadence Verilog-A
Language Reference and the local training material.

These extension tasks keep the same pure voltage-domain behavioral boundary as
the original benchmark. They intentionally avoid current-domain `I(...)`
behavior, transistor-level devices, custom conservative branch equations, and
AMS connect-module or `wreal` glue.

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

Each extension task contains:

- `instruction.md`
- `solution/`
- `starter/`
- `test_visible/`
- `test_hidden/`
- `test_harness/visible_hidden_manifest.json`
- five concrete negative variants under `negative_variants/`

## Certification Boundary

The extension tasks are marked `syntax-extension-candidate` in `TASKS.json` and
`CHECKS.yaml`. They are not part of the original full-300 certification claim.

Current EVAS compile scan:

- 35 / 40 extension reference solutions compile with the current EVAS backend.
- 5 / 40 user-defined-function tasks parse but require EVAS support for
  user-defined function calls, or Spectre-based certification.

Before these tasks are included in any paper-facing full-suite claim, run
dedicated EVAS/Spectre behavior certification and promote only the rows whose
gold solutions, hidden checks, and five negative variants are all certified.

## AMS Mixed-Signal Extension

Tasks `341` through `360` add Verilog-AMS digital/mixed-signal constructs that
are outside pure Verilog-A but are important for practical behavioral modeling:

- `341`-`345`: `wreal` nets with continuous `assign`.
- `346`-`350`: `logic` nets with combinational continuous `assign`.
- `351`-`355`: edge-triggered `always` blocks for digital sequential behavior.
- `356`-`360`: mixed `logic`/`wreal`/`electrical` bridge-style behavioral tasks.

These rows are marked `ams-mixed-signal-candidate`. EVAS currently parses and
compiles some old-style `wreal`/`logic` declaration plus `assign` forms, but does
not support `always` blocks and does not accept ANSI-style typed digital ports.
Track EVAS support before promoting these rows into any certified suite.

## Noise And Analysis Extension

Tasks `361` through `372` add Verilog-A noise and analysis-dependent source
functions from the Cadence language reference:

- `white_noise()`
- `flicker_noise()`
- `noise_table()`
- `analysis()`
- `ac_stim()`

These rows are marked `noise-analysis-candidate`. They are behavioral and
voltage-domain, but they may require AC/noise-capable simulator certification.
EVAS currently parses these functions but rejects them during backend compile;
track EVAS issue #23 before EVAS promotion.
