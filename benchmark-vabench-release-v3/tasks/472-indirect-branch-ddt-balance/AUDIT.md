# Audit: Indirect Branch Ddt Balance

- Task id: `v3_472_indirect_branch_ddt_balance`
- Category: `veriloga_indirect_branch_semantics`
- Required syntax focus: `Use indirect branch assignment with a ddt() equation term.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `behavioral-continuous-time-candidate`
- EVAS status: `compile-supported continuous-time/constraint candidate; behavior requires ddt and indirect-branch equation certification`
- Blocking issue: `ddt()` indirect branch behavior requires continuous-time dynamic support in EVAS; see https://github.com/Arcadia-1/EVAS/issues/44.
