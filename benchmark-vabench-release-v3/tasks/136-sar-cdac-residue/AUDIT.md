# Two-Gate SOP Audit: Task 136 SAR CDAC Residue

## Scope

Task 136 is a sampled SAR CDAC residue update primitive. It is data-converter support, but it has a standalone AMS function boundary through clocked sampling and weighted capacitor-switch residue updates.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: retain as a data-converter support L1 row.
- Function boundary: sample `VIN`, then update residue through public SAR switch events and binary reference-span weights.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after targeted EVAS, Spectre visible/hidden gold validation, and AHDL warning triage.
- Prompt hygiene: public instruction now exposes clock edge, switch edge directions, reference parameters, explicit output transition time, and the binary residue weights.
- Checker alignment: checker now derives expected residue from input/switch events and uses an LSB-sensitive tolerance.
- Negative strength: `neg_004_missing_lsb_step` was previously accepted because the checker tolerance was too wide; the checker now rejects the omitted-S1 behavior.
- Hidden coverage: private deck now uses a different sample value and switching schedule from the visible smoke deck.
- AHDL triage: the gold now provides explicit `transition(..., tr, tr)` timing to avoid ideal-transition ambiguity.

## Evidence

- Fresh EVAS gold after checker/hidden repair: PASS.
- Fresh EVAS negatives after checker repair: 5/5 behavioral rejections.
- Spectre gold validation: visible and hidden PASS with zero measured residue error after the explicit transition-time repair.
- AHDL triage: the prior task-specific ideal-transition warning is gone; remaining warnings are shared bridge/environment warnings.
