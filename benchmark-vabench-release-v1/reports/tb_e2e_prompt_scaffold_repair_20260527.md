# TB/E2E Prompt Scaffold Repair - 2026-05-27

## Summary

Upgraded release public prompts to `public-contract-v3` by adding an explicit Spectre `.scs` scaffold to every TB/E2E prompt. Gold assets and checkers were not changed.

## Scope

- prompt_sync_changed: 158 TB/E2E prompts
- prompt_manifest: 271 prompts, status pass, version public-contract-v3
- gold_changed: False
- checker_changed: False

## Repair Points

- Every TB/E2E prompt now includes a Public Spectre Testbench Scaffold section.
- The scaffold includes literal ahdl_include lines for the generated or supplied Verilog-A files.
- The scaffold includes public fixed supply sources when present in the reference harness, e.g. CDAC VDD=0.9 V.
- The scaffold uses public instance lines from the reference harness when available, preventing node-name case mismatches such as VDD/vdd.
- The scaffold explicitly forbids module-first instance syntax and requires instance-first/module-last Spectre syntax.

## Validation

- py_compile: pass with PYTHONPYCACHEPREFIX
- prompt_manifest_refresh: pass; public-contract-v3; 271 prompts
- scaffold_scan: 158 TB/E2E prompts, missing_scaffold=0
- pytest: 10 passed: score_runnable_assets, prompt_contracts, prompt_contract_manifest

## Examples

- CDAC TB scaffold now states `ahdl_include "cdac_cal.va"`, fixed `0.9 V` supply, `XDUT (...) cdac_cal`, `tran`, and `save` lines.
- Pipeline ADC E2E scaffold now uses the public reference instance line with lowercase testbench nodes `vdd/vss/vin/clk`, instead of guessing from uppercase module port names.
