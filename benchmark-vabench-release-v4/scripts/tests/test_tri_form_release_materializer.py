from __future__ import annotations

import json
import hashlib
import sys
from pathlib import Path


PREP = Path(__file__).resolve().parents[2] / "operations" / "tri_form_derivation_prep"
if str(PREP) not in sys.path:
    sys.path.insert(0, str(PREP))

import materialize_tri_form_release as materializer  # noqa: E402
from materialize_tri_form_release import (  # noqa: E402
    COMPONENT_METADATA,
    MODES,
    REFERENCE_TOKENIZER,
    aggregate_artifact_sha,
    build_dut_public_contract,
    build_solver_contract,
    compact_reference_replay_record,
    current_source_evidence_identity,
    public_semantics,
    reference_token_count,
    reference_replay_mismatches,
    render_bugfix_instruction,
    render_dut_instruction,
    render_testbench_instruction,
    replay_record_sha,
    sanitize_public_buggy_source,
    select_bugfix_seed,
    source_record_mismatches,
)
from export_tri_form_runtime import install_public, render_prompt  # noqa: E402
from audit_tri_form_release import (  # noqa: E402
    audit_task,
    buggy_source_leak_markers,
    expected_reference_replay_plan,
)
from record_runtime_ingestion_evidence import verified_audit  # noqa: E402


PACKAGE = Path(__file__).resolve().parents[2]
MATERIALIZED_RELEASE = PACKAGE / "release" / "tri-form-v4-1200-final"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_external_source_reference_stays_package_relative() -> None:
    from materialize_tri_form_release import resolve_source_reference, source_rel

    source = Path("/tmp/exact-five")
    reference = resolve_source_reference(
        source,
        "release/dut-base-v3-exact-five-hash-bound-v2",
    )

    assert reference == "release/dut-base-v3-exact-five-hash-bound-v2"
    assert source_rel(
        source / "001-demo" / "evaluator" / "checker_profile.json",
        source,
        reference,
    ) == (
        "release/dut-base-v3-exact-five-hash-bound-v2/001-demo/"
        "evaluator/checker_profile.json"
    )


def sample_spec() -> dict:
    return {
        "family_id": "001",
        "identity": {"title": "Sample Hold", "category": "sampling", "level": "L1", "difficulty": "D2"},
        "artifact_contract": {"mode": "single_file", "files": [{"path": "dut.va", "modules": [{
            "name": "dut", "role": "entry", "depends_on": [],
            "ports": [{"name": "vin", "direction": "input", "discipline": "electrical", "position": 0}],
            "parameters": [],
        }]}]},
        "testbench_binding": {"source_path_template": "./dut/{artifact_path}", "instances": [{
            "name": "XDUT", "module_ref": "dut", "connections": [{"port_ref": "vin", "net": "vin", "position": 0}],
        }]},
        "properties": [{"id": "P_HOLD", "observable_contract": "hold the sampled value", "required_signals": ["time", "vin"]}],
        "trace_contract": {"required_signals": ["time", "vin"]},
        "modeling_constraints": ["Remain deterministic."],
    }


def test_mode_matrix_is_two_direct_plus_four_agentic() -> None:
    assert [name for name, row in MODES.items() if row["process"] == "direct_one_shot"] == ["G0", "G1"]
    assert [name for name, row in MODES.items() if row["feedback_cli"]] == ["G2", "G3", "G4", "G5"]


def test_bugfix_instruction_does_not_localize_fault() -> None:
    text = render_bugfix_instruction(sample_spec()).lower()
    for forbidden in ("mutation", "faulty file", "root cause", "changed line", "baseline result"):
        assert forbidden not in text


def test_buggy_source_leak_scan_targets_evaluator_metadata_only(tmp_path: Path) -> None:
    bundle = tmp_path / "buggy_bundle"
    bundle.mkdir()
    source = bundle / "dut.va"
    source.write_text(
        "// A circuit fault may be represented by this ordinary signal name.\n"
        "module dut; real fault_voltage; endmodule\n",
        encoding="utf-8",
    )
    assert buggy_source_leak_markers(bundle) == []

    source.write_text(
        "// mutation_id: neg_003_wrong_edge\nmodule dut; endmodule\n",
        encoding="utf-8",
    )
    assert buggy_source_leak_markers(bundle) == ["mutation_id", "negative_id"]


def test_public_buggy_source_strips_only_leading_evaluator_annotation() -> None:
    source = (
        "// Copyright remains public.\n"
        "// neg_004_wrong_edge: changes the sampled edge.\n"
        "// This continuation also localizes the defect.\n"
        "\n"
        "module dut;\n"
        "  // Ordinary in-code fault terminology is allowed.\n"
        "endmodule\n"
    )

    sanitized, changed = sanitize_public_buggy_source(source)

    assert changed is True
    assert sanitized.startswith("// Copyright remains public.\nmodule dut;")
    assert "neg_004" not in sanitized
    assert "localizes the defect" not in sanitized
    assert "Ordinary in-code fault terminology" in sanitized


def test_dut_instruction_is_generated_from_family_spec() -> None:
    text = render_dut_instruction(sample_spec())
    assert "# Sample Hold" in text
    assert "`dut.va`" in text
    assert "`P_HOLD`" in text
    assert "solver_contract.json" in text


def test_testbench_instruction_has_one_candidate_and_five_anonymous_negatives() -> None:
    text = render_testbench_instruction(sample_spec())
    assert "`testbench.scs`" in text
    assert "five anonymous semantic negative DUTs" in text
    assert "solver_contract.json" in text
    assert "source_path_template" not in text
    assert "hidden" not in text.lower()


def test_public_semantics_excludes_private_evaluator_binding() -> None:
    contract = public_semantics(sample_spec())
    assert "testbench_binding" not in contract
    assert "dut_source_root" not in json.dumps(contract)
    assert "source_path_template" not in json.dumps(contract)


def test_solver_contract_is_compact_public_projection() -> None:
    public = build_dut_public_contract(sample_spec(), "v4-001")
    solver = build_solver_contract(public)
    assert solver["task_id"] == "v4-001"
    assert solver["properties"] == [
        {"id": "P_HOLD", "observable_contract": "hold the sampled value"}
    ]
    assert solver["trace_contract"] == {"required_signals": ["time", "vin"]}
    assert "feedback" not in solver
    assert "identity" not in solver


def test_dut_solver_contract_does_not_expose_evaluator_trace_aliases() -> None:
    spec = sample_spec()
    spec["properties"][0]["required_signals"] = ["time", "vin_case_42", "vout_sample_9ns"]
    spec["trace_contract"] = {"required_signals": ["time", "vin_case_42", "vout_sample_9ns"]}

    solver = build_solver_contract(build_dut_public_contract(spec, "v4-001"))

    rendered = json.dumps(solver, sort_keys=True)
    assert "vin_case_42" not in rendered
    assert "vout_sample_9ns" not in rendered
    assert solver["trace_contract"] == {"required_signals": ["time", "vin"]}


def test_release_audit_reports_missing_solver_contract_without_crashing(tmp_path: Path) -> None:
    release = tmp_path / "release"
    task = release / "tasks" / "dut" / "001-sample"
    task.mkdir(parents=True)
    (task / "TASK_RECORD.json").write_text("{}\n", encoding="utf-8")
    (task / "instruction.md").write_text("Implement the DUT.\n", encoding="utf-8")
    (task / "public_contract.json").write_text("{}\n", encoding="utf-8")
    problems: list[str] = []

    audit_task(
        release,
        tmp_path / "source",
        {
            "task_dir": "tasks/dut/001-sample",
            "task_id": "v4-001",
            "form": "dut",
            "family_id": "001",
        },
        problems,
    )

    assert problems == ["v4-001: missing solver_contract.json"]


def test_seed_policy_prefers_temporal_semantic_fault_over_force_zero() -> None:
    row = {
        "bugfix_seed": "neg_001_force_zero",
        "active_mutations": [
            {"mutation_id": "neg_001_force_zero", "fault_class": "stuck_zero", "trigger_condition": "all time", "violated_property_ids": ["P_OUT"]},
            {"mutation_id": "neg_002_wrong_edge", "fault_class": "wrong_sampling_edge", "trigger_condition": "falling edge after reset", "violated_property_ids": ["P_EDGE", "P_HOLD"]},
        ],
    }
    selected = select_bugfix_seed(row)
    assert selected["mutation_id"] == "neg_002_wrong_edge"
    assert not selected["triviality_markers"]


def test_current_source_identity_rejects_stale_342_certification() -> None:
    source = (
        PACKAGE
        / "release"
        / "dut-base-v3-exact-five-hash-bound-v2"
        / "342-sar-adc-system-4b"
    )
    current_source_evidence_identity.cache_clear()
    current = current_source_evidence_identity(source)
    recorded = read_json(source / "evaluator" / "certification.json")

    mismatches = source_record_mismatches(
        recorded,
        current,
        task_input_keys=(
            "family_spec_sha256",
            "checker_profile_sha256",
            "harness_spec_sha256",
            "gold_bundle_sha256",
            "feedback_profile_sha256",
            "score_profile_sha256",
        ),
    )

    assert "task_inputs.family_spec_sha256" in mismatches
    assert "task_inputs.harness_spec_sha256" in mismatches
    assert "oracle.checker_implementation_sha256" in mismatches


def test_partial_mutation_bundle_hash_overlays_unchanged_gold_artifacts(
    tmp_path: Path,
) -> None:
    gold = tmp_path / "gold"
    mutation = tmp_path / "mutation"
    gold.mkdir()
    mutation.mkdir()
    (gold / "top.va").write_text("gold top\n", encoding="utf-8")
    (gold / "leaf.va").write_text("gold leaf\n", encoding="utf-8")
    (mutation / "top.va").write_text("mutated top\n", encoding="utf-8")

    gold_hash = aggregate_artifact_sha(
        {"top.va": gold / "top.va", "leaf.va": gold / "leaf.va"}
    )
    candidate_hash = aggregate_artifact_sha(
        {"top.va": mutation / "top.va", "leaf.va": gold / "leaf.va"}
    )
    mutation_only_hash = aggregate_artifact_sha({"top.va": mutation / "top.va"})

    assert candidate_hash != gold_hash
    assert candidate_hash != mutation_only_hash


def test_reference_replay_record_is_compact_hash_bound_and_path_free() -> None:
    row = {
        "canonical_id": "7",
        "mutation_id": "neg_002_wrong_edge",
        "profile": "score",
        "status": "PASS",
        "case_dir": "/private/tmp/host-specific/case",
        "component_fingerprints": {"task_inputs": {"deck_sha256": "a" * 64}},
        "evaluators": {"spectre": {
            "compile_status": "pass",
            "simulation_status": "pass",
            "behavior_status": "behavior_fail",
        }},
        "checkers": {"spectre_behavior": {"status": "behavior_fail"}},
        "property_activation_status": "verified",
        "property_activation": {"status": "verified", "log_path": "/tmp/private.log"},
        "side_effect": {"required": False},
        "spectre": {
            "ran": True,
            "ok": True,
            "rows": 12,
            "untriaged_warnings": [],
            "raw_log": "/private/tmp/raw.log",
        },
        "spectre_identity": {"backend": "spectre", "host": "thu-wei"},
    }

    record = compact_reference_replay_record(row, source_evidence_sha256="b" * 64)
    rendered = json.dumps(record, sort_keys=True)

    assert record["canonical_id"] == "007"
    assert record["record_sha256"] == replay_record_sha(record)
    assert "/private/tmp" not in rendered
    assert "log_path" not in rendered
    assert "raw_log" not in rendered


def test_reference_replay_binding_rejects_rehashed_stale_fingerprint(tmp_path: Path) -> None:
    source_task = tmp_path / "source-task"
    evaluator = source_task / "evaluator"
    evaluator.mkdir(parents=True)
    lock = evaluator / "toolchain_lock.json"
    lock.write_text('{"lock":"test"}\n', encoding="utf-8")
    task_inputs = {
        key: "a" * 64
        for key in (
            "deck_sha256",
            "profile_sha256",
            "harness_spec_sha256",
            "gold_bundle_sha256",
            "candidate_bundle_sha256",
            "property_contract_sha256",
            "trace_contract_sha256",
        )
    }
    oracle = {
        key: "b" * 64
        for key in (
            "checker_profile_sha256",
            "checker_binding_sha256",
            "checker_implementation_sha256",
            "diagnostic_policy_sha256",
        )
    }
    record = {
        "status": "FAIL_PROPERTY_ACTIVATION",
        "component_fingerprints": {
            "task_inputs": dict(task_inputs),
            "oracle": dict(oracle),
            "assembly": {"release_snapshot_sha256": materializer.file_sha(lock)},
        },
        "evaluators": {
            "ahdl_like": {"compile_status": "pass"},
            "evas": {"compile_status": "pass", "simulation_status": "pass", "behavior_status": "behavior_fail"},
            "spectre": {"compile_status": "pass", "simulation_status": "pass", "behavior_status": "behavior_fail"},
        },
        "checkers": {
            "evas_behavior": {"status": "behavior_fail"},
            "spectre_behavior": {"status": "behavior_fail"},
        },
        "property_activation_status": "unverified",
        "side_effect": {"required": False},
        "evas": {"ran": True, "ok": True, "returncode": 0},
        "spectre": {"ran": True, "ok": True, "rows": 5, "untriaged_warnings": []},
    }
    record["record_sha256"] = replay_record_sha(record)
    current = {"task_inputs": dict(task_inputs), "oracle": dict(oracle)}

    assert reference_replay_mismatches(record, current, source_task) == []

    record["component_fingerprints"]["task_inputs"]["deck_sha256"] = "c" * 64
    record["record_sha256"] = replay_record_sha(record)
    assert "task_inputs.deck_sha256" in reference_replay_mismatches(
        record,
        current,
        source_task,
    )


def test_reference_replay_selection_rejects_multiple_valid_rows(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(materializer, "reference_replay_mismatches", lambda *_args: [])
    candidates = [{"record_sha256": "a" * 64}, {"record_sha256": "b" * 64}]

    selected, mismatches = materializer.select_reference_replay_candidate(
        candidates,
        {},
        tmp_path,
    )

    assert selected is None
    assert mismatches == ["supplemental.ambiguous_valid_records"]


def test_expected_reference_replay_plan_preserves_family_binding() -> None:
    certificates = [
        ("342", {"negative_cases": {
            "neg_002_wrong_edge": {
                "source_hash_reusable": False,
                "replay_profile": "score",
                "reference_deck_sha256": "c" * 64,
            },
            "neg_003_reusable": {"source_hash_reusable": True},
        }}),
    ]

    assert expected_reference_replay_plan(certificates) == {
        ("342", "neg_002_wrong_edge", "score", "c" * 64)
    }


def test_release_audit_rejects_absolute_canonical_source_path(tmp_path: Path) -> None:
    release = tmp_path / "release"
    task = release / "tasks" / "dut" / "001-sample"
    task.mkdir(parents=True)
    contract = build_dut_public_contract(sample_spec(), "v4-001")
    (task / "instruction.md").write_text("Implement the DUT.\n", encoding="utf-8")
    (task / "public_contract.json").write_text(
        json.dumps(contract) + "\n",
        encoding="utf-8",
    )
    (task / "solver_contract.json").write_text(
        json.dumps(build_solver_contract(contract)) + "\n",
        encoding="utf-8",
    )
    (task / "TASK_RECORD.json").write_text(json.dumps({
        "task_id": "v4-001",
        "form": "dut",
        "family_id": "001",
        "canonical_dut_source": "/private/tmp/leaked/001-sample",
        "public_bundle_sha256": "invalid",
    }) + "\n", encoding="utf-8")
    problems: list[str] = []

    audit_task(
        release,
        tmp_path / "source",
        {
            "task_dir": "tasks/dut/001-sample",
            "task_id": "v4-001",
            "form": "dut",
            "family_id": "001",
        },
        problems,
        source_reference="release/source",
    )

    assert "v4-001: canonical DUT source path is unsafe" in problems


def test_materialized_release_uses_one_bugfix_seed_per_family() -> None:
    tasks = read_json(MATERIALIZED_RELEASE / "TASK_INDEX.json")["tasks"]
    by_family = {
        (str(row["family_id"]), str(row["form"])): MATERIALIZED_RELEASE / row["task_dir"]
        for row in tasks
    }
    mismatches = []
    for family in (f"{value:03d}" for value in range(1, 401)):
        testbench = read_json(
            by_family[(family, "testbench")] / "evaluator" / "derivation_manifest.json"
        )
        bugfix = read_json(
            by_family[(family, "bugfix")] / "evaluator" / "derivation_manifest.json"
        )
        testbench_seed = testbench["negative_assignment"]["bugfix_seed"]
        bugfix_seed = bugfix["negative_assignment"]["bugfix_seed"]
        if testbench_seed != bugfix_seed:
            mismatches.append((family, testbench_seed, bugfix_seed))
    assert not mismatches, mismatches[:10]


def test_release_seal_hashes_all_transitive_artifacts(tmp_path: Path) -> None:
    from audit_tri_form_release import RELEASE_SEAL_ARTIFACTS, build_release_seal

    release = tmp_path / "release"
    for index, relative in enumerate(RELEASE_SEAL_ARTIFACTS):
        path = release / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"artifact-{index}\n", encoding="utf-8")
    seal = build_release_seal(release, "a" * 64)
    assert seal["schema_version"] == "v4-tri-form-release-seal-v1"
    assert seal["source_score_denominator_manifest_sha256"] == "a" * 64
    assert set(seal["artifact_sha256"]) == set(RELEASE_SEAL_ARTIFACTS)
    assert "RELEASE_SEAL.json" not in seal["artifact_sha256"]


def test_materialized_release_seal_replays_current_hashes() -> None:
    seal = read_json(MATERIALIZED_RELEASE / "RELEASE_SEAL.json")
    assert seal["schema_version"] == "v4-tri-form-release-seal-v2"
    assert seal["release_status"] == "final_static_tb_security_v2_fixed"
    for relative, recorded_sha in seal["artifact_sha256"].items():
        assert hashlib.sha256((MATERIALIZED_RELEASE / relative).read_bytes()).hexdigest() == recorded_sha
    digest = hashlib.sha256()
    for path in sorted(p for p in MATERIALIZED_RELEASE.rglob("*") if p.is_file()):
        relative = path.relative_to(MATERIALIZED_RELEASE).as_posix()
        if relative == "RELEASE_SEAL.json":
            continue
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    assert seal["tree_sha256"] == digest.hexdigest()


def test_prompt_components_have_pinned_reference_tokenizer_metadata() -> None:
    assert REFERENCE_TOKENIZER["id"] == "vabench_utf8_lexeme"
    assert set(COMPONENT_METADATA) == {
        "neutral_wrapper.md",
        "dut_modeling.md",
        "testbench_verification.md",
        "bugfix_diagnosis.md",
        "feedback_core.md",
        "feedback_dut.md",
        "feedback_testbench.md",
        "feedback_bugfix.md",
    }
    assert reference_token_count("one two; three") == 4


def test_runtime_prompt_always_places_submission_wrapper_last(tmp_path: Path) -> None:
    release = tmp_path / "release"
    skills = release / "prompt_modes" / "skills"
    skills.mkdir(parents=True)
    (skills / "dut_modeling.md").write_text("FORM SKILL\n", encoding="utf-8")
    (skills / "feedback_core.md").write_text("FEEDBACK CORE\n", encoding="utf-8")
    (skills / "feedback_dut.md").write_text("FEEDBACK DUT\n", encoding="utf-8")
    (skills / "neutral_wrapper.md").write_text("SUBMISSION CONTRACT\n", encoding="utf-8")
    task = tmp_path / "task"
    task.mkdir()
    (task / "instruction.md").write_text("TASK\n", encoding="utf-8")
    (task / "public_contract.json").write_text("{}\n", encoding="utf-8")
    (task / "solver_contract.json").write_text("{}\n", encoding="utf-8")
    prompt = render_prompt(
        release,
        task,
        {"canonical_dut_source": "unused", "form": "dut"},
        {"skill_hashes": {
            "dut_modeling.md": "x",
            "feedback_core.md": "y",
            "feedback_dut.md": "z",
        }},
        inline_artifacts=False,
    )
    assert prompt.index('<<<VABENCH_SKILL id="dut_modeling.md">>>') < prompt.index(
        '<<<VABENCH_COMPONENT id="neutral_wrapper.md">>>'
    )
    assert prompt.rstrip().endswith("<<<END_VABENCH_COMPONENT>>>")


def test_agentic_bugfix_export_seeds_editable_submission(tmp_path: Path) -> None:
    task = tmp_path / "task"
    (task / "buggy_bundle").mkdir(parents=True)
    (task / "buggy_bundle" / "a.va").write_text("module a; endmodule\n", encoding="utf-8")
    (task / "instruction.md").write_text("Repair the bundle.\n", encoding="utf-8")
    (task / "public_contract.json").write_text("{}\n", encoding="utf-8")
    (task / "solver_contract.json").write_text("{}\n", encoding="utf-8")
    public = tmp_path / "public"
    (public / "submission").mkdir(parents=True)
    install_public(task, public, "bugfix", "G2")
    assert (public / "submission" / "a.va").read_bytes() == (task / "buggy_bundle" / "a.va").read_bytes()
    assert (public / "task" / "buggy_bundle" / "a.va").is_file()


def test_runtime_export_includes_declared_public_support(tmp_path: Path) -> None:
    task = tmp_path / "task"
    task.mkdir()
    (task / "instruction.md").write_text("Implement the DUT.\n", encoding="utf-8")
    (task / "public_contract.json").write_text("{}\n", encoding="utf-8")
    (task / "solver_contract.json").write_text("{}\n", encoding="utf-8")
    support = task / "public_support"
    support.mkdir(parents=True)
    (support / "helper.va").write_text("module helper; endmodule\n", encoding="utf-8")
    public = tmp_path / "public"
    (public / "submission").mkdir(parents=True)
    install_public(task, public, "dut", "G2")
    assert (public / "task" / "public_support" / "helper.va").is_file()


def test_runtime_evidence_rejects_handwritten_pass_report(tmp_path: Path) -> None:
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    (evidence / "runtime_export_audit.json").write_text(
        '{"schema_version":"wrong","status":"pass","problems":[]}\n',
        encoding="utf-8",
    )
    try:
        verified_audit(tmp_path)
    except SystemExit as exc:
        assert "not a valid pass" in str(exc)
    else:
        raise AssertionError("handwritten pass report was accepted")
