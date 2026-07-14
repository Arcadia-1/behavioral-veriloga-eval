from __future__ import annotations

import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any


class CaseOutcome(str, Enum):
    REFERENCE_PASS = "reference_pass"
    REFERENCE_FAIL = "reference_fail"
    KILLED_BEHAVIORALLY = "killed_behaviorally"
    SURVIVED = "survived"
    INVALID_RUN = "invalid_run"


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    role: str
    outcome: CaseOutcome
    notes: tuple[str, ...]

    @property
    def counts_as_kill(self) -> bool:
        return self.role == "negative" and self.outcome is CaseOutcome.KILLED_BEHAVIORALLY


@dataclass(frozen=True)
class TestbenchResult:
    reference: CaseResult
    negatives: tuple[CaseResult, ...]
    expected_negative_count: int = 5

    @property
    def killed_count(self) -> int:
        return sum(result.counts_as_kill for result in self.negatives)

    @property
    def invalid_count(self) -> int:
        return sum(result.outcome is CaseOutcome.INVALID_RUN for result in self.negatives)

    @property
    def survived_count(self) -> int:
        return sum(result.outcome is CaseOutcome.SURVIVED for result in self.negatives)

    @property
    def passed(self) -> bool:
        return (
            self.reference.outcome is CaseOutcome.REFERENCE_PASS
            and len(self.negatives) == self.expected_negative_count
            and self.killed_count == self.expected_negative_count
        )


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _candidate_tb_dir(env_name: str) -> Path:
    override = os.environ.get(env_name)
    if not override:
        raise SystemExit(f"missing candidate testbench directory; set {env_name}=<candidate-dir>")
    return Path(override).expanduser().resolve()


def _find_package_root(path: Path) -> Path:
    for parent in [path, *path.parents]:
        if (parent / "formal_tasks").is_dir() and (parent / "runners").is_dir():
            return parent
    raise SystemExit("cannot find benchmark-vabench-release-v4 package root")


def _find_repo_root(package_root: Path) -> Path:
    for parent in [package_root, *package_root.parents]:
        if (parent / "runners" / "simulate_evas.py").exists():
            return parent
    raise SystemExit("cannot find behavioral-veriloga-eval repo root")


def _copy_single_tb(candidate_dir: Path, run_dir: Path, expected_name: str) -> Path:
    source = candidate_dir / expected_name
    if not source.exists():
        raise SystemExit(f"candidate testbench directory is missing target artifact: {expected_name}")
    target = run_dir / expected_name
    shutil.copy2(source, target)
    return target


def _module_names(source: Path) -> list[str]:
    text = source.read_text(encoding="utf-8", errors="ignore")
    return re.findall(r"\bmodule\s+([A-Za-z_][A-Za-z0-9_$]*)", text)


def _target_name_for_negative(negative_source: Path, target_artifacts: list[str]) -> str:
    if len(target_artifacts) == 1:
        return target_artifacts[0]
    module_names = set(_module_names(negative_source))
    for artifact in target_artifacts:
        if Path(artifact).stem in module_names:
            return artifact
    raise SystemExit(
        f"cannot map negative {negative_source} to one of target artifacts: {', '.join(target_artifacts)}"
    )


def _negative_bundle_sources(negative_bundle: Path, target_artifacts: list[str]) -> dict[str, Path]:
    if negative_bundle.is_file():
        return {_target_name_for_negative(negative_bundle, target_artifacts): negative_bundle}
    if not negative_bundle.is_dir():
        raise ValueError(f"negative bundle is missing: {negative_bundle}")
    candidates = sorted(negative_bundle.rglob("*.va"))
    if not candidates:
        raise ValueError(f"negative bundle has no Verilog-A source: {negative_bundle}")
    by_basename: dict[str, list[str]] = {}
    for artifact in target_artifacts:
        by_basename.setdefault(Path(artifact).name, []).append(artifact)
    mapped: dict[str, Path] = {}
    for source in candidates:
        relative = source.relative_to(negative_bundle).as_posix()
        if relative in target_artifacts:
            target = relative
        else:
            matches = by_basename.get(source.name) or []
            if len(matches) == 1:
                target = matches[0]
            elif len(target_artifacts) == 1 and len(candidates) == 1:
                target = target_artifacts[0]
            else:
                raise ValueError(f"cannot map negative artifact {relative} into declared DUT bundle")
        if target in mapped:
            raise ValueError(f"negative bundle maps multiple files to {target}")
        mapped[target] = source
    return mapped


def _prepare_dut_sources(
    *,
    package_root: Path,
    source_formal: Path,
    run_dir: Path,
    target_artifacts: list[str],
    negative_bundle: Path | None = None,
    dut_subdir: str | None = None,
    public_contract: dict[str, Any] | None = None,
) -> None:
    supplied = (public_contract or {}).get("supplied_inputs") or {}
    include_by_artifact = {
        str(item.get("public_input_path") or "").removeprefix("supplied_dut/"): str(
            item.get("testbench_include_path") or ""
        )
        for item in supplied.get("read_only_dut_artifacts") or []
    }

    def include_target(include_path: str) -> Path:
        logical = PurePosixPath(include_path)
        if logical.is_absolute() or ".." in logical.parts:
            raise ValueError(f"invalid logical include path: {include_path}")
        return run_dir.joinpath(*[part for part in logical.parts if part != "."])

    target_root = run_dir / dut_subdir if dut_subdir else run_dir
    for artifact in target_artifacts:
        source = source_formal / "solution" / artifact
        if not source.is_file():
            source = source_formal / "trusted_solution" / artifact
        if not source.exists():
            raise SystemExit(f"missing gold DUT artifact: {source}")
        include_path = include_by_artifact.get(artifact)
        target = include_target(include_path) if include_path else target_root / artifact
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    if negative_bundle is not None:
        for target_name, source in _negative_bundle_sources(negative_bundle, target_artifacts).items():
            include_path = include_by_artifact.get(target_name)
            target = include_target(include_path) if include_path else target_root / target_name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    support_root = source_formal / "public_support"
    for item in supplied.get("read_only_support_artifacts") or []:
        public_path = str(item.get("public_input_path") or "")
        relative = public_path.removeprefix("public_support/")
        source = support_root / relative
        if not source.is_file():
            raise SystemExit(f"missing public support artifact: {source}")
        target = include_target(str(item.get("testbench_include_path") or ""))
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _trace_is_valid(csv_path: Path, required_signals: set[str]) -> tuple[bool, list[str]]:
    try:
        with csv_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            header = next(reader, [])
            first_row = next(reader, None)
    except (OSError, csv.Error, UnicodeError) as exc:
        return False, [f"trace read failed: {type(exc).__name__}"]
    def expand(name: str) -> set[str]:
        match = re.fullmatch(r"(.+)\[(\d+):(\d+)\]", name)
        if match is None:
            return {name.lower()}
        base, first, last = match.groups()
        start = int(first)
        stop = int(last)
        step = -1 if start > stop else 1
        return {f"{base}{index}".lower() for index in range(start, stop + step, step)}

    required = {value for item in required_signals for value in expand(str(item))}
    present = {value for item in header for value in expand(str(item))}
    missing = sorted(required - present)
    if missing:
        return False, ["missing required trace signals: " + ", ".join(missing)]
    if first_row is None:
        return False, ["transient trace contains no data rows"]
    return True, []


def _case_result(
    *,
    label: str,
    role: str,
    valid: bool,
    behavior_pass: bool | None,
    notes: list[str],
) -> CaseResult:
    if not valid:
        outcome = CaseOutcome.INVALID_RUN
    elif role == "reference":
        outcome = CaseOutcome.REFERENCE_PASS if behavior_pass else CaseOutcome.REFERENCE_FAIL
    else:
        outcome = CaseOutcome.SURVIVED if behavior_pass else CaseOutcome.KILLED_BEHAVIORALLY
    return CaseResult(label, role, outcome, tuple(notes))


def _run_case(
    *,
    package_root: Path,
    tb_source: Path,
    source_formal: Path,
    target_artifacts: list[str],
    negative_bundle: Path | None,
    checker_task_id: str,
    required_signals: set[str],
    label: str,
    dut_subdir: str | None = None,
    public_contract: dict[str, Any] | None = None,
) -> CaseResult:
    repo_root = _find_repo_root(package_root)
    runners_dir = str(repo_root / "runners")
    if runners_dir not in sys.path:
        sys.path.insert(0, runners_dir)
    from simulate_evas import evaluate_behavior, run_evas

    role = "reference" if negative_bundle is None else "negative"
    with tempfile.TemporaryDirectory(prefix=f"v4_tb_feedback_{label}_") as td:
        run_dir = Path(td)
        tb_dst = run_dir / "tb_candidate.scs"
        shutil.copy2(tb_source, tb_dst)
        try:
            _prepare_dut_sources(
                package_root=package_root,
                source_formal=source_formal,
                run_dir=run_dir,
                target_artifacts=target_artifacts,
                negative_bundle=negative_bundle,
                dut_subdir=dut_subdir,
                public_contract=public_contract,
            )
        except (OSError, SystemExit, ValueError) as exc:
            return _case_result(
                label=label,
                role=role,
                valid=False,
                behavior_pass=None,
                notes=[f"{label}: DUT staging failed: {str(exc)[:300]}"],
            )
        output_dir = run_dir / "out"
        try:
            result = run_evas(
                run_dir,
                tb_dst,
                output_dir,
                timeout_s=60,
                required_trace_signals=required_signals,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return _case_result(
                label=label,
                role=role,
                valid=False,
                behavior_pass=None,
                notes=[f"{label}: simulation invocation failed: {type(exc).__name__}"],
            )
        combined = (result.stdout or "") + "\n" + (result.stderr or "")
        if result.returncode != 0:
            return _case_result(
                label=label,
                role=role,
                valid=False,
                behavior_pass=None,
                notes=[f"{label}: simulation failed", combined[-2000:]],
            )
        csv_path = output_dir / "tran.csv"
        if not csv_path.exists():
            return _case_result(
                label=label,
                role=role,
                valid=False,
                behavior_pass=None,
                notes=[f"{label}: no transient trace produced"],
            )
        trace_valid, trace_notes = _trace_is_valid(csv_path, required_signals)
        if not trace_valid:
            return _case_result(
                label=label,
                role=role,
                valid=False,
                behavior_pass=None,
                notes=[f"{label}: {note}" for note in trace_notes],
            )
        try:
            score, notes = evaluate_behavior(checker_task_id, csv_path)
        except Exception as exc:  # Checker exceptions are evaluator-invalid, not behavioral kills.
            return _case_result(
                label=label,
                role=role,
                valid=False,
                behavior_pass=None,
                notes=[f"{label}: checker failed: {type(exc).__name__}: {str(exc)[:300]}"],
            )
        return _case_result(
            label=label,
            role=role,
            valid=True,
            behavior_pass=score >= 1.0,
            notes=[f"{label}: " + note for note in notes],
        )


def _run_testbench_oracle(
    script_file: str | Path,
    *,
    source_env: str,
    result_prefix: str,
    public_subset_only: bool,
) -> int:
    script_path = Path(script_file).resolve()
    task_dir = script_path.parents[1]
    package_root = _find_package_root(task_dir)
    record = _read_json(task_dir / "TASK_RECORD.json")
    policy = _read_json(task_dir / "evaluator" / "score_policy.json")
    contract = _read_json(task_dir / "public_contract.json")
    source_formal = package_root / str(record["source_formal_dir"])
    target_artifacts = [str(item) for item in policy.get("target_artifacts") or record.get("source_target_artifacts") or []]
    if not target_artifacts:
        raise SystemExit("missing source target artifacts in score policy")
    checker_profile = _read_json(package_root / str(policy["source_checker_profile"]))
    checker_task_id = str(policy["source_checker_task_id"])
    required_signals = set(str(item) for item in contract.get("required_trace_signals") or [])
    trace_contract = checker_profile.get("trace_contract") or {}
    required_signals.update(str(item) for item in trace_contract.get("extra_trace_signals") or [])
    repo_root = _find_repo_root(package_root)
    runners_dir = str(repo_root / "runners")
    if runners_dir not in sys.path:
        sys.path.insert(0, runners_dir)
    from simulate_evas import required_trace_signals_for_checker

    required_signals.update(required_trace_signals_for_checker(checker_task_id))

    candidate_dir = _candidate_tb_dir(source_env)
    with tempfile.TemporaryDirectory(prefix="v4_tb_feedback_candidate_") as td:
        candidate_copy_dir = Path(td)
        candidate_tb = _copy_single_tb(candidate_dir, candidate_copy_dir, str(record["target"][0]))

        security_path = task_dir / "evaluator" / "testbench_security_policy.json"
        if security_path.is_file():
            from testbench_security import validate_testbench

            security = validate_testbench(candidate_tb, contract, _read_json(security_path))
            if not security.valid:
                for note in security.diagnostics:
                    print(f"security: {note}")
                print(f"{result_prefix}_TB_INVALID_RUN")
                return 1

        gold = _run_case(
            package_root=package_root,
            tb_source=candidate_tb,
            source_formal=source_formal,
            target_artifacts=target_artifacts,
            negative_bundle=None,
            checker_task_id=checker_task_id,
            required_signals=required_signals,
            label="gold",
            public_contract=contract,
        )
        for note in gold.notes:
            print(note)
        if gold.outcome is not CaseOutcome.REFERENCE_PASS:
            print(f"{result_prefix}_TB_REFERENCE_{gold.outcome.value.upper()}")
            return 1

        negative_manifest_path = package_root / str(policy["negative_manifest"])
        negative_manifest = _read_json(negative_manifest_path)
        negative_cases = [
            case for case in negative_manifest.get("cases", []) or negative_manifest.get("negatives", [])
        ]
        if len(negative_cases) != 5:
            print(f"{result_prefix}_TB_NEGATIVE_SUITE_INVALID count={len(negative_cases)} expected=5")
            return 1
        negative_results: list[CaseResult] = []
        for case in negative_cases:
            negative_ref = str(case.get("source") or case.get("artifact") or "")
            negative_bundle = source_formal / negative_ref
            if not negative_bundle.exists():
                negative_bundle = negative_manifest_path.parent / negative_ref
            result = _run_case(
                package_root=package_root,
                tb_source=candidate_tb,
                source_formal=source_formal,
                target_artifacts=target_artifacts,
                negative_bundle=negative_bundle,
                checker_task_id=checker_task_id,
                required_signals=required_signals,
                label=str(case["id"]),
                public_contract=contract,
            )
            negative_results.append(result)
            for note in result.notes:
                print(note)
        aggregate = TestbenchResult(gold, tuple(negative_results))
        if not aggregate.passed:
            print(
                f"{result_prefix}_TB_NEGATIVE_COVERAGE_FAIL "
                f"killed={aggregate.killed_count}/5 survived={aggregate.survived_count} "
                f"invalid={aggregate.invalid_count}"
            )
            return 1

    print(f"{result_prefix}_TB_PASS killed={aggregate.killed_count}/5")
    return 0


def run_testbench_feedback(script_file: str | Path) -> int:
    return _run_testbench_oracle(
        script_file,
        source_env="VABENCH_FEEDBACK_TB_DIR",
        result_prefix="FEEDBACK",
        public_subset_only=True,
    )


def run_testbench_score(script_file: str | Path) -> int:
    return _run_testbench_oracle(
        script_file,
        source_env="VABENCH_SCORE_TB_DIR",
        result_prefix="SCORE",
        public_subset_only=False,
    )
