# Audit: Indirect Branch Null Balance

- Task id: `v3_471_indirect_branch_null_balance`
- Category: `veriloga_indirect_branch_semantics`
- Required syntax focus: `Use an indirect branch assignment target/equation form.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `behavioral-continuous-time-candidate`
- EVAS status: `compile-supported continuous-time/constraint candidate; behavior requires indirect-branch equation certification`
- Blocking issue: indirect branch equation behavior requires continuous-time dynamic support in EVAS; see https://github.com/Arcadia-1/EVAS/issues/44.
