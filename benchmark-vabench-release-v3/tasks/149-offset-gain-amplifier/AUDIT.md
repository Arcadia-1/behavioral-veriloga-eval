# Offset Gain Amplifier Audit

- Gate 1 counting status: retain as a small L1 analog primitive, with low complexity noted. It covers a single-ended offset-correcting gain stage.
- Gate 2 modeling status: prompt now states the fixed input offset and voltage gain as the public circuit contract, without checker or testbench leakage.
- Checker status: stable sampled waveform checks cover offset subtraction and gain.
- Cadence reference anchor: voltage-domain macromodel guidance for simple gain stages.
- Current validation status: 2026-07-03 rerun passed EVAS hidden gold, EVAS negative rejection, visible smoke, EVAS AHDL-like lint, and Spectre hidden gold.
