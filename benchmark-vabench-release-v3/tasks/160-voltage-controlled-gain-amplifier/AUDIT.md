# Voltage Controlled Gain Amplifier Audit

- Gate 1 counting status: duplicate-risk L1 candidate. It is a valid unipolar voltage-controlled gain block, but functionally overlaps strongly with `159-variable-gain-differential-amplifier` and `280-vargain-diffamp-clip`.
- Recommended counting treatment: retain only if the benchmark set wants a unipolar output-range VCA variant; otherwise prefer `280` as the more parameterized canonical variable-gain differential clip task.
- Gate 2 modeling status: prompt now exposes differential input/control roles, input offset, output midpoint, unipolar clamp range, and voltage-domain boundary.
- Checker status: stable sampled waveform checks cover input offset, differential control, midpoint, and clamp behavior.
- Cadence reference anchor: voltage-domain gain/control macromodels with explicit limiting.
- Current validation status: 2026-07-03 rerun passed EVAS hidden gold, EVAS negative rejection, visible smoke, EVAS AHDL-like lint, and Spectre hidden gold.
