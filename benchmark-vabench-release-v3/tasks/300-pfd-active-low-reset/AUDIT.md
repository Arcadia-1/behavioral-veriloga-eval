# PFD External Active-Low Reset Audit

- Gate 1: `independent_l1_ready`.
- Duplicate resolution: this row is distinct from `282-pfd-timer-reset` because it adds an explicit asynchronous active-low reset input that clears pending one-sided PFD state.
- Cadence/VA modeling rationale: Cadence PFD examples use `cross` events for REF/FB edge capture, state-machine storage, `timer` for delayed reset, and `transition` for smooth rail-coded outputs. This row extends that pattern with an external reset pin.
- Public contract: `pfd_active_low_reset(ref, fb, rstb, up, down)` with active-high `up/down`; `rstb` low clears and holds both outputs low, and normal REF/FB operation resumes when `rstb` is high.
- Checker alignment: checker evaluates reset-low hold, one-sided state clearing by external reset, normal UP/DOWN assertions, and delayed mutual reset.
- Validation status: fresh local EVAS2 gold/negative, Spectre visible/hidden gold, Spectre hidden negative, and EVAS AHDL-like preflight validation completed after this rewrite. Generated evidence reports are intentionally not committed.
