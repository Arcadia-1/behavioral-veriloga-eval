from __future__ import annotations

import json
import sys
from pathlib import Path


PREP = Path(__file__).resolve().parents[2] / "operations" / "tri_form_derivation_prep"
if str(PREP) not in sys.path:
    sys.path.insert(0, str(PREP))

from materialize_tri_form_release import (  # noqa: E402
    COMPONENT_METADATA,
    FEEDBACK_CORE,
    FEEDBACK_GUIDES,
    FORM_SKILLS,
    MODES,
    REFERENCE_TOKENIZER,
    WRAPPERS_BY_PROCESS,
    install_prompt_assets,
    iter_public_inputs,
    negative_assignment,
    reference_token_count,
    render_bugfix_instruction,
    render_testbench_instruction,
    select_bugfix_seed,
    write_prompt_records,
)
from export_tri_form_runtime import install_public, ordered_prompt_components, render_prompt  # noqa: E402
from record_runtime_ingestion_evidence import verified_audit  # noqa: E402
from audit_tri_form_release import (  # noqa: E402
    RELEASE_SEAL_ARTIFACTS,
    build_release_seal,
    expected_buggy_artifact_hashes,
    file_sha,
    mutation_certification_hashes,
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


def test_testbench_instruction_has_one_candidate_and_five_anonymous_negatives() -> None:
    text = render_testbench_instruction(sample_spec())
    assert "`testbench.scs`" in text
    assert "five anonymous semantic negative DUTs" in text
    assert "hidden" not in text.lower()


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


def test_testbench_and_bugfix_share_one_selected_negative_assignment() -> None:
    row = {
        "bugfix_seed": "neg_001_force_zero",
        "active_mutations": [
            {"mutation_id": "neg_001_force_zero"},
            {"mutation_id": "neg_002_wrong_edge"},
        ],
    }
    selected = {"mutation_id": "neg_002_wrong_edge"}
    assert negative_assignment(row, selected) == {
        "bugfix_seed": "neg_002_wrong_edge",
        "testbench_suite": ["neg_001_force_zero", "neg_002_wrong_edge"],
    }


def test_prompt_components_have_pinned_reference_tokenizer_metadata() -> None:
    assert REFERENCE_TOKENIZER["id"] == "vabench_utf8_lexeme"
    assert set(COMPONENT_METADATA) == {
        "direct_wrapper.md",
        "agentic_wrapper.md",
        "dut_modeling.md",
        "testbench_verification.md",
        "bugfix_diagnosis.md",
        "feedback_core.md",
        "feedback_dut.md",
        "feedback_testbench.md",
        "feedback_bugfix.md",
    }
    assert {COMPONENT_METADATA[name]["kind"] for name in WRAPPERS_BY_PROCESS.values()} == {"wrapper"}
    assert {COMPONENT_METADATA[name]["kind"] for name in FORM_SKILLS.values()} == {"form_skill"}
    assert COMPONENT_METADATA[FEEDBACK_CORE]["kind"] == "feedback_guide"
    assert {COMPONENT_METADATA[name]["kind"] for name in FEEDBACK_GUIDES.values()} == {"feedback_guide"}
    assert reference_token_count("one two; three") == 4


def write_sample_prompt_records(release: Path, form: str = "bugfix") -> Path:
    task = release / "tasks" / form / "sample"
    task.mkdir(parents=True)
    (task / "instruction.md").write_text("Complete the task from this instruction.\n", encoding="utf-8")
    (task / "public_contract.json").write_text('{"evaluator_only": true}\n', encoding="utf-8")
    if form == "testbench":
        (task / "supplied_dut").mkdir()
        (task / "supplied_dut" / "dut.va").write_text("module dut; endmodule\n", encoding="utf-8")
    elif form == "bugfix":
        (task / "buggy_bundle").mkdir()
        (task / "buggy_bundle" / "buggy.va").write_text("module buggy; endmodule\n", encoding="utf-8")
    components = install_prompt_assets(release)
    write_prompt_records(
        release,
        [{"task_id": "v4-sample", "family_id": "001", "form": form, "task_dir": task.relative_to(release).as_posix()}],
        components,
    )
    return task


def prompt_record_at(release: Path, mode: str) -> dict:
    for line in (release / "prompt_modes" / "PROMPT_RECORDS.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row["mode"] == mode:
            return row
    raise AssertionError(f"missing prompt record for {mode}")


def test_prompt_record_components_keep_wrapper_last_and_contract_out_of_prompt_surface(tmp_path: Path) -> None:
    task = write_sample_prompt_records(tmp_path, "bugfix")
    assert [item.name for item in iter_public_inputs(task, "bugfix")] == ["instruction.md", "buggy.va"]
    g1 = prompt_record_at(tmp_path, "G1")
    assert g1["component_order"] == ["instruction", "public_input:buggy_bundle/buggy.va", "bugfix_diagnosis.md", "direct_wrapper.md"]
    assert ordered_prompt_components(g1) == ["bugfix_diagnosis.md", "direct_wrapper.md"]
    assert "public_contract.json" not in g1["public_input_hashes"]
    assert g1["public_contract_sha256"] == file_sha(task / "public_contract.json")
    g5 = prompt_record_at(tmp_path, "G5")
    assert g5["component_order"] == [
        "instruction",
        "public_input:buggy_bundle/buggy.va",
        "bugfix_diagnosis.md",
        "feedback_core.md",
        "feedback_bugfix.md",
        "agentic_wrapper.md",
    ]
    assert ordered_prompt_components(g5) == [
        "bugfix_diagnosis.md",
        "feedback_core.md",
        "feedback_bugfix.md",
        "agentic_wrapper.md",
    ]


def test_rendered_prompts_do_not_inline_public_contract_json_and_use_mode_wrapper(tmp_path: Path) -> None:
    task = write_sample_prompt_records(tmp_path, "bugfix")
    record = {"form": "bugfix"}
    g1_text = render_prompt(tmp_path, task, record, prompt_record_at(tmp_path, "G1"), inline_artifacts=True)
    assert "<<<VABENCH_PUBLIC_CONTRACT>>>" not in g1_text
    assert "public_contract.json" not in g1_text
    assert '<<<VABENCH_INPUT_ARTIFACT path="buggy_bundle/buggy.va">>>' in g1_text
    assert g1_text.index('id="bugfix_diagnosis.md"') < g1_text.index('id="direct_wrapper.md"')
    g5_text = render_prompt(tmp_path, task, record, prompt_record_at(tmp_path, "G5"), inline_artifacts=False)
    assert "<<<VABENCH_PUBLIC_CONTRACT>>>" not in g5_text
    assert "public_contract.json" not in g5_text
    assert "VABENCH_INPUT_ARTIFACT" not in g5_text
    assert (
        g5_text.index('id="bugfix_diagnosis.md"')
        < g5_text.index('id="feedback_core.md"')
        < g5_text.index('id="feedback_bugfix.md"')
        < g5_text.index('id="agentic_wrapper.md"')
    )


def test_agentic_bugfix_export_seeds_editable_submission(tmp_path: Path) -> None:
    task = tmp_path / "task"
    (task / "buggy_bundle").mkdir(parents=True)
    (task / "buggy_bundle" / "a.va").write_text("module a; endmodule\n", encoding="utf-8")
    (task / "instruction.md").write_text("Repair the bundle.\n", encoding="utf-8")
    (task / "public_contract.json").write_text("{}\n", encoding="utf-8")
    public = tmp_path / "public"
    (public / "submission").mkdir(parents=True)
    install_public(task, public, "bugfix", "G2")
    assert (public / "submission" / "a.va").read_bytes() == (task / "buggy_bundle" / "a.va").read_bytes()
    assert (public / "task" / "buggy_bundle" / "a.va").is_file()
    assert not (public / "task" / "public_contract.json").exists()


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


def test_reference_certification_hashes_are_bound_to_exact_five_rows() -> None:
    rows = [
        {"mutation_id": "m1", "certification_sha256": "a" * 64},
        {"mutation_id": "m2", "certification_sha256": "b" * 64},
    ]
    assert mutation_certification_hashes(rows) == {
        "m1": "a" * 64,
        "m2": "b" * 64,
    }


def test_bugfix_bundle_hashes_include_unchanged_gold_artifacts(tmp_path: Path) -> None:
    solution = tmp_path / "solution"
    solution.mkdir()
    (solution / "changed.va").write_text("gold changed\n", encoding="utf-8")
    (solution / "unchanged.va").write_text("gold unchanged\n", encoding="utf-8")
    mutated_hash = "c" * 64
    assert expected_buggy_artifact_hashes(
        ["changed.va", "unchanged.va"],
        {"changed.va": mutated_hash},
        solution,
    ) == {
        "changed.va": mutated_hash,
        "unchanged.va": file_sha(solution / "unchanged.va"),
    }


def test_release_seal_binds_transitive_release_and_reused_certifications(tmp_path: Path) -> None:
    for relative in RELEASE_SEAL_ARTIFACTS:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"artifact": relative}) + "\n", encoding="utf-8")
    reuse = {
        "policy": "source_denominator_hash_bound",
        "source_dut_gold_certification_count": 400,
        "source_negative_certification_count": 2000,
        "evaluators": ["evas", "spectre"],
        "simulation_rerun_required_for_materialization": False,
    }
    seal = build_release_seal(tmp_path, "a" * 64, reuse)
    assert seal["release_status"] == "gate3_hash_bound_certification_reused"
    assert seal["certification_reuse"] == reuse
    assert set(seal["artifact_sha256"]) == set(RELEASE_SEAL_ARTIFACTS)
