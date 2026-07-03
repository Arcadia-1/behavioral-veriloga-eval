# Honest SOP Audit: Task 005 Debounce Latch

## Scope

Task boundary is one Verilog-A DUT, `debounce_latch.va`, plus EVAS/Spectre-compatible `.scs` testbenches.

## Four Standards

- Useful scenario: comparator debounce qualification is a common mixed-signal decision-filter primitive.
- Reasonable task: the public prompt states the exact port order, active-low reset behavior, 12 ns qualification delay, and voltage-coded logic levels.
- Complete tests: visible smoke plus private validation decks save `sig`, `rst_n`, and `out`; private stimulus covers reset-held high input, short glitches, reset cancellation, a stable-high qualified interval, and falling-input clear.
- Fair evaluation: trace checker should sample `out` low at 20 ns, 40 ns, 60 ns, 82 ns, and 138 ns, and high at 100 ns and 130 ns. Threshold is 0.45 V.

Certification status: certified as an EVAS formal candidate on 2026-06-24. Gold PASS; 5/5 concrete negatives compile and fail with `FAIL_SIM_CORRECTNESS` under `v3_005_debounce_latch`.

## Digital/Control/Logic Closeout Review

- Gate 1 status: `independent_l1_ready`.
- Rationale: comparator decision debounce is an AMS decision-filter primitive with reset, qualification timer, glitch rejection, and held output state.
- Counting recommendation: retain as comparator/control L1; it is not a generic gate.
