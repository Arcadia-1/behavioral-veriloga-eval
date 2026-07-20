#!/usr/bin/env python3
"""Audit a tri-form runtime export for public/evaluator isolation."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ALLOWED_DUT_RUNTIME_SCHEMAS = {
    "r45": {"r45-direct-evas-runtime-v1", "r45-direct-evas-runtime-v2"},
    "r47": {"r47-direct-evas-runtime-v2"},
    "r48": {"r48-direct-evas-runtime-v2"},
    "r49": {"r49-direct-evas-runtime-v2"},
}
ALLOWED_TESTBENCH_RUNTIME_SCHEMAS = {
    "r45": {
        "r45-direct-evas-testbench-suite-v1",
        "r45-direct-evas-testbench-suite-v2",
    },
    "r47": {"r47-direct-evas-testbench-suite-v2"},
    "r48": {"r48-direct-evas-testbench-suite-v2"},
    "r49": {"r49-direct-evas-testbench-suite-v2"},
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def tree_sha(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if item.is_file():
            digest.update(item.relative_to(path).as_posix().encode("utf-8"))
            digest.update(b"\0")
            digest.update(item.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def file_map(path: Path) -> dict[str, bytes]:
    return {item.relative_to(path).as_posix(): item.read_bytes() for item in sorted(path.rglob("*")) if item.is_file()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    run = args.run.expanduser().resolve()
    problems: list[str] = []
    policy = read_json(run / "MODEL_ACCESS_POLICY.json")
    attempt = read_json(run / "evidence" / "attempt_record.json")
    mode = str(policy.get("mode") or "")
    mounts = policy.get("mounts") or []
    if policy.get("evaluator_mounted") is not False or any("evaluator" in str(item) for item in mounts):
        problems.append("evaluator assets are model-mounted")
    if policy.get("network") is not False:
        problems.append("network is not disabled")
    if mode in {"G0", "G1"}:
        if mounts:
            problems.append("direct one-shot mode has filesystem mounts")
        if not (run / "direct_prompt.txt").is_file():
            problems.append("direct one-shot prompt is missing")
        else:
            direct_prompt = (run / "direct_prompt.txt").read_text(encoding="utf-8", errors="ignore")
            for marker in (
                "VABENCH_PUBLIC_CONTRACT",
                "Feedback tools",
                "feedback CLI",
                "vabench feedback",
                "private Spectre",
                "public/submission",
                "agentic mode",
                "mounted public task inputs",
            ):
                if marker.lower() in direct_prompt.lower():
                    problems.append(f"direct one-shot prompt leaks {marker!r}")
        if (run / "public" / "evas_manifest.json").exists():
            problems.append("direct one-shot mode exposes an EVAS manifest")
        if (run / "public" / "task" / "public_contract.json").exists():
            problems.append("direct one-shot mode exposes a public contract file")
    else:
        if mounts != ["public/task:ro", "public/submission:rw"]:
            problems.append("agentic model mounts differ from the public contract")
        if policy.get("executables") != ["evas"]:
            problems.append("agentic mode does not expose only the EVAS executable")
        if not (run / "public" / "evas_manifest.json").is_file():
            problems.append("agentic mode lacks the direct EVAS manifest")
        if not (run / "public" / "task" / "evas_runtime.json").is_file():
            problems.append("agentic mode lacks the transparent EVAS runtime contract")
        if not (run / "agent_prompt.txt").is_file():
            problems.append("agentic mode lacks the composed initial prompt")
        else:
            agent_prompt = (run / "agent_prompt.txt").read_text(encoding="utf-8", errors="ignore")
            if "VABENCH_PUBLIC_CONTRACT" in agent_prompt:
                problems.append("agentic prompt redundantly inlines public_contract.json")
        if (run / "public" / "task" / "public_contract.json").exists():
            problems.append("agentic mode exposes public_contract.json in the model task mount")
    submission = run / "public" / "submission"
    if attempt.get("initial_submission_sha256") != tree_sha(submission):
        problems.append("initial submission hash does not match the prepared workspace")
    if attempt.get("form") == "bugfix" and mode not in {"G0", "G1"}:
        buggy = run / "public" / "task" / "buggy_bundle"
        if file_map(buggy) != file_map(submission):
            problems.append("bugfix writable submission is not an exact editable copy of the supplied buggy bundle")
        if attempt.get("submission_seeded_from_buggy_bundle") is not True:
            problems.append("bugfix attempt does not record its seeded editable workspace")
    if attempt.get("state") != "prepared" or attempt.get("private_score_decisions") != 0:
        problems.append("attempt lifecycle was not initialized safely")
    evaluator = run / "evaluator"
    if not evaluator.is_dir():
        problems.append("private evaluator bundle is missing")
    else:
        for name in ("task_record.json", "family_spec.json", "checker_profile.json", "harness_spec.json", "score_policy.json"):
            if not (evaluator / name).is_file():
                problems.append(f"private evaluator bundle missing {name}")
        if not (evaluator / "profiles").is_dir():
            problems.append("private evaluator bundle missing profiles/")
        form = str(attempt.get("form") or "")
        task_record_path = evaluator / "task_record.json"
        task_record = read_json(task_record_path) if task_record_path.is_file() else {}
        release_revision = str(task_record.get("release_revision") or "")
        if release_revision not in ALLOWED_DUT_RUNTIME_SCHEMAS:
            problems.append("private task record has an unsupported release revision")
        if form in {"dut", "bugfix"}:
            if mode not in {"G0", "G1"} and not (
                run / "public" / "task" / "visible_test.scs"
            ).is_file():
                problems.append("agentic DUT/bugfix mode lacks task-local visible_test.scs")
            if not (evaluator / "solution").is_dir():
                problems.append("private evaluator bundle missing solution/")
            if not (evaluator / "canonical_test_profile.json").is_file():
                problems.append("private evaluator bundle missing canonical_test_profile.json")
            if not (evaluator / "trusted_replay_test.scs").is_file():
                problems.append("private evaluator bundle missing trusted replay deck")
            runtime_contract = run / "public" / "task" / "evas_runtime.json"
            if mode not in {"G0", "G1"} and runtime_contract.is_file():
                runtime_data = read_json(runtime_contract)
                command = str(runtime_data.get("command") or "")
                schema_version = runtime_data.get("schema_version")
                if schema_version not in ALLOWED_DUT_RUNTIME_SCHEMAS.get(release_revision, set()):
                    problems.append("public EVAS runtime schema does not match the release")
                if schema_version == f"{release_revision}-direct-evas-runtime-v2":
                    if "/tmp/vabench-visible/evas-output" not in command or "public/submission/evas-output" in command:
                        problems.append("public EVAS output is not isolated from submission")
        if form == "testbench":
            for required in ("trusted_solution", "mutation_bundles"):
                if not (evaluator / required).is_dir():
                    problems.append(f"private testbench evaluator bundle missing {required}/")
            for required in (
                "mutation_catalog.json", "reference_tb.scs", "testbench_security_policy.json",
                "trusted_replay_suite.json",
            ):
                if not (evaluator / required).is_file():
                    problems.append(f"private testbench evaluator bundle missing {required}")
            if not (evaluator / "trusted_replay_fixtures").is_dir():
                problems.append("private testbench evaluator bundle missing trusted_replay_fixtures/")
        visible = run / "public" / "task" / "visible_test.scs"
        trusted = evaluator / "trusted_replay_test.scs"
        if mode not in {"G0", "G1"} and visible.is_file() and trusted.is_file():
            if visible.read_bytes() != trusted.read_bytes():
                problems.append("visible test and trusted replay deck differ")
        if form == "testbench" and mode not in {"G0", "G1"}:
            fixtures = run / "public" / "task" / "visible_fixtures"
            fixture_names = sorted(
                path.name for path in fixtures.iterdir() if path.is_dir()
            ) if fixtures.is_dir() else []
            if fixture_names != [
                "mutation_01", "mutation_02", "mutation_03", "mutation_04", "mutation_05", "reference",
            ]:
                problems.append("public testbench runtime does not expose one reference and five mutation fixtures")
            public_suite = run / "public" / "task" / "evas_runtime.json"
            trusted_suite = evaluator / "trusted_replay_suite.json"
            trusted_fixtures = evaluator / "trusted_replay_fixtures"
            if public_suite.is_file() and trusted_suite.is_file() and public_suite.read_bytes() != trusted_suite.read_bytes():
                problems.append("public and trusted testbench suite manifests differ")
            if public_suite.is_file():
                suite_data = read_json(public_suite)
                command = str(suite_data.get("candidate_command_template") or "")
                schema_version = suite_data.get("schema_version")
                if schema_version not in ALLOWED_TESTBENCH_RUNTIME_SCHEMAS.get(release_revision, set()):
                    problems.append("public testbench suite schema does not match the release")
                if schema_version == f"{release_revision}-direct-evas-testbench-suite-v2":
                    if "/tmp/vabench-visible/runs/{case}" not in command:
                        problems.append("public testbench runs are not scratch-isolated")
                    if "public/submission/runs" in command or "public/submission/evas-output" in command:
                        problems.append("public testbench scratch pollutes submission")
            if fixtures.is_dir() and trusted_fixtures.is_dir() and tree_sha(fixtures) != tree_sha(trusted_fixtures):
                problems.append("public and trusted testbench fixture trees differ")
            if (run / "public" / "task" / "visible_test.scs").exists():
                problems.append("testbench runtime exposes a gold-derived visible_test.scs")
        if attempt.get("evaluator_bundle_sha256") != tree_sha(evaluator):
            problems.append("evaluator bundle hash does not match the prepared workspace")
    for path in (run / "public").rglob("*"):
        if path.is_symlink():
            problems.append(f"public bundle contains symlink: {path}")
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "negative_variants/" in text or "/evaluator/" in text or "vabench feedback" in text.lower():
                problems.append(f"public file leaks authoring evaluator path: {path}")
    report = {"schema_version": "v4-runtime-export-audit-v1", "status": "pass" if not problems else "fail", "problems": problems}
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
