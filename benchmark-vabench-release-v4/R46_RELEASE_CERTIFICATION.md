# R46 Release Certification

R46 is the active immutable vaBench V4 package at
`release/benchmarkv4-r46/`. It is a new release tree; the published r44 and
r45 trees and their revision-scoped evidence remain byte-for-byte unchanged.
The R46 audit reports `pass` with no structural or certification problems.

## Certified Scope

- 1,200 tasks: 400 DUT, 400 testbench, and 400 bugfix forms.
- 7,200 prompt records.
- Direct EVAS runtime protocol: DUT and bugfix tasks expose one task-local
  visible test whose bytes are reused for trusted final replay. Testbench tasks
  expose the bound reference-plus-five-mutation suite without publishing the
  gold testbench candidate.
- Runtime identity: EVAS `0.8.3`, engine `evas2`, backend `evas-rust`; the
  certification policy is `rust_evas2_only` and has no compatibility fallback.
- Source denominator registry SHA-256:
  `142ac6a32693c20b450b7f52b7d551e680cc6d7f4da360247fd006632d981aac`.
- Release manifest SHA-256:
  `72d6e5128bf128e39cad2d83148fb98116f97e9a4bda8d2f08177f1d7ee32592`.

R46 includes the source correction for family 232's
`neg_002_no_denominator_guard`: the negative now uses an under-sized 20 mV
guard rather than a machine epsilon at exact zero. This remains behaviorally
wrong against the required 200 mV guard, but its failure no longer depends on
an exact-zero sample landing on a simulator grid. Fresh certification kills it
at a 16 mV observed denominator.

## Evidence

| Artifact | Verified result | SHA-256 |
| --- | --- | --- |
| `evidence/r46/RUST_EVAS2_CERTIFICATION.json` | 400/400 gold pass; 2,000/2,000 mutations killed; 399 insufficient-excitation rejections and 1 not-applicable case; 2,372 trace-axis invariants | `5a9b6180275ec2fae774d8967efbfaf00b984100e11537c777121c814ab39393` |
| `evidence/r46/STIMULUS_METAMORPHIC.json` | 400/400 affine gold pass; 2,000/2,000 affine mutations killed; 0 infrastructure errors; 383 insufficient-excitation rejections and 17 not-applicable cases | `8dc2fb95045535af2f8cff74de4591da96d28dccf7c7e96777de324111632456` |
| `evidence/r46/PROFILE_PARITY.json` | 1,200/1,200 task forms pass; 0 failures across families 001-400 | `bc36fc5812a014045b27b4d6f4be3cb96a51f110aa10ece765f15888d8b43e47` |

Each R46 evidence artifact binds the source denominator registry. Metamorphic
and profile evidence additionally bind the R46 manifest; executable evidence
binds its raw input report. The auditor checks these bindings, revision-scoped
schemas, and the EVAS 0.8.3 Rust runtime markers, so changing labels on an older
artifact cannot satisfy the R46 gate.

Profile parity is a binding and semantic-hash check, not an additional
simulation campaign (`simulation_performed: false`). The
`r45-canonical-test-profile-v1` name is retained as the stable profile-format
schema that introduced this contract; R46 identity is carried independently by
the manifest, task-record, task-index, and public-runtime schemas.

## Release Seal And Rebuild

`release/benchmarkv4-r46/RELEASE_SEAL.json` declares `immutable: true` and
records `r46_immutable_rust_evas2_certified`. Its bound audit contains 1,200
tasks, 400 families, 7,200 prompt records, `problems: []`, and
`certification_problems: []`.

The certification refresh was evidence-only:
`source_certifications_updated` is `false`. R46 materialization binds the
source inputs transitively by SHA-256 and binds the fresh R46 evidence listed
above. A second full rebuild into an independent directory, including runtime
ingestion evidence, audit, and seal generation, matches the tracked R46 tree
under an unfiltered `diff -qr`.

CI permits R46 only as a newly introduced release. Once it exists in the base
revision, both `release/benchmarkv4-r46/` and `evidence/r46/` are protected by
the immutable-tree gate. Any later benchmark content, protocol, evidence, or
input-hash change requires R47 and a new seal.
