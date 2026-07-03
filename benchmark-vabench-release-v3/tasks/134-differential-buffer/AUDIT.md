# Differential Buffer Audit

- Gate 1: `l2_support_component` / low-complexity primitive. The row is valid
  as a differential voltage-domain support block, but a strict core benchmark
  count should not overclaim it as a rich independent circuit function.
- Duplicate review: distinct from `161-ideal-differential-opamp` only by being
  unity pass-through with no gain or common-mode generation. Prefer 161 when a
  stronger amplifier primitive is needed.
- Gate 2: public prompt now uses the mandatory v3 instruction shape and exposes
  exact unity mapping, common-mode preservation, and no gain/offset/delay.
- Validation focus: stable samples compare both input-output pairs and reject
  swapped outputs, half gain, common-mode-only, and zero implementations.
