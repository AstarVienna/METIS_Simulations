#!/usr/bin/env python
"""
Validate that every YAML file under the YAML/ tree

    1. Can be parsed by PyYAML (``yaml.safe_load``).
    2. Passes static/schema validation via
       ``metis_simulations.runRecipes.validate_recipes``.
    3. Is accepted by ``metis_simulations.runSimulationBlock.runSimulationBlock``.

Results are written as a markdown report. For each failing file the report
lists the underlying error and, where possible, identifies the top-level YAML
entry (template recipe) that caused the failure.

The real ScopeSim ``simulate`` call is monkey-patched to a no-op so the
validation performs only structural/signature checks and does not actually
execute simulations or write FITS files.

Usage
-----
    python validate_yamls.py [--yaml-dir PATH] [--output PATH]

Defaults assume this script lives in ``YAML/`` and writes
``yaml_validation_report.md`` next to itself.
"""

from __future__ import annotations

import argparse
import copy
import os
import sys
import tempfile
import traceback
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# simulationDefinitions.py reads DEFAULT_IRDB_LOCATION at import time. We
# mock simulate() so the value is never used, but it still has to be present.
os.environ.setdefault("DEFAULT_IRDB_LOCATION", str(REPO_ROOT))


def _install_stubs() -> None:
    """Inject fake ScopeSim-backed modules before anything else imports them.

    Two siblings of ``setupSimulations`` / ``runRecipes`` pull in ``scopesim``
    and ``metis_simulations.sources`` at import time, and the latter builds
    full ScopeSim OpticalTrain objects at module load. That is far too heavy
    (and too fragile — it needs an IRDB install) for a YAML validation pass.
    Both modules are only used here for their ``simulate`` symbol, so fakes
    exposing a no-op ``simulate`` are sufficient.

    runSimulationBlock calls ``simulate`` unconditionally from inside the
    recipe loop (testRun only gates the parallel Pool dispatch and the
    header-update step), so it must be stubbed regardless of testRun.
    """
    import types

    def _noop_simulate(*args, **kwargs):
        return None

    for mod_name in (
        "metis_simulations.scopesimWrapper",  # used by setupSimulations
        "metis_simulations.raw_script",        # used by runRecipes
    ):
        fake = types.ModuleType(mod_name)
        fake.simulate = _noop_simulate
        sys.modules[mod_name] = fake


def _base_params(out_dir: str, do_calib: int = 1) -> dict:
    return {
        "outputDir": out_dir,
        "small": True,
        "doStatic": False,
        "doCalib": do_calib,
        "sequence": True,
        "startMJD": "2027-01-25 00:00:00",
        "calibFile": None,
        "nCores": 1,
        "testRun": True,
    }


def _try_run(yaml_path: Path) -> tuple[bool, str | None]:
    """Try to feed a single YAML file to runSimulationBlock.

    Returns (ok, error_message). ``error_message`` is None on success.
    """
    from metis_simulations import runSimulationBlock as rs

    with tempfile.TemporaryDirectory() as tmp:
        params = _base_params(tmp)
        try:
            # Pass -t so parseCommandLine's argparse result also carries
            # testRun=True and doesn't overwrite our params dict.
            rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
        except SystemExit as exc:
            return False, f"SystemExit: {exc}"
        except BaseException as exc:
            return False, f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}"
    return True, None


def _try_run_single_entry(entry_name: str, entry_value, tmp_dir: Path) -> tuple[bool, str | None]:
    """Write a one-entry YAML to ``tmp_dir`` and test it."""
    from metis_simulations import runSimulationBlock as rs

    # Deep-copy so we don't mutate the caller's dict through runSimulationBlock.
    single = {entry_name: copy.deepcopy(entry_value)}
    tmp_yaml = tmp_dir / f"__single_{entry_name}.yaml"
    with tmp_yaml.open("w", encoding="utf-8") as f:
        yaml.safe_dump(single, f, sort_keys=False)

    params = _base_params(str(tmp_dir))
    try:
        rs.runSimulationBlock([str(tmp_yaml)], params, ["-t"])
    except SystemExit as exc:
        return False, f"SystemExit: {exc}"
    except BaseException as exc:
        return False, f"{type(exc).__name__}: {exc}"
    finally:
        try:
            tmp_yaml.unlink()
        except OSError:
            pass
    return True, None


def _identify_failing_entries(parsed, outer_error: str) -> list[tuple[str, str]]:
    """If the whole-file run failed, try each top-level entry in isolation.

    Returns a list of (entry_name, error_message) for every entry that fails
    on its own. Non-dict YAMLs or empty YAMLs short-circuit with a single
    synthetic entry describing the structural problem.
    """
    if not isinstance(parsed, dict):
        return [("<file>", f"Top-level YAML is not a mapping (got {type(parsed).__name__}); "
                            f"runSimulationBlock expects a dict of named recipes. "
                            f"Outer error: {outer_error}")]
    if not parsed:
        return [("<file>", "YAML contains no recipes. Outer error: " + outer_error)]

    failing: list[tuple[str, str]] = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for name, value in parsed.items():
            ok, err = _try_run_single_entry(str(name), value, tmp_path)
            if not ok:
                failing.append((str(name), err or "unknown error"))
    return failing


def validate_file(yaml_path: Path) -> dict:
    """Return a result dict describing the validation outcome for one file."""
    from metis_simulations.runRecipes import validate_recipes

    result: dict = {
        "path": yaml_path,
        "yaml_ok": False,
        "yaml_error": None,
        "static_errors": [],
        "run_ok": False,
        "run_error": None,
        "failing_entries": [],
    }

    # Step 1: PyYAML parse.
    try:
        with yaml_path.open(encoding="utf-8") as f:
            parsed = yaml.safe_load(f)
        result["yaml_ok"] = True
    except yaml.YAMLError as exc:
        result["yaml_error"] = f"{type(exc).__name__}: {exc}"
        return result
    except OSError as exc:
        result["yaml_error"] = f"OSError: {exc}"
        return result

    # Step 2: static/schema validation via runRecipes.validate_recipes.
    # validate_recipes requires a dict of named recipes; anything else is
    # reported as a single structural message (the dynamic pass below
    # reports the same problem more specifically).
    if isinstance(parsed, dict) and parsed:
        try:
            result["static_errors"] = list(validate_recipes(parsed))
        except Exception as exc:
            # validate_recipes shouldn't raise on normal recipe dicts, but
            # if it does, surface it rather than letting it abort the run.
            result["static_errors"] = [f"validate_recipes raised {type(exc).__name__}: {exc}"]
    elif not isinstance(parsed, dict):
        result["static_errors"] = [
            f"Top-level YAML is not a mapping (got {type(parsed).__name__}); "
            f"expected a dict of named recipes."
        ]
    else:
        result["static_errors"] = ["YAML contains no recipes."]

    # Step 3: runSimulationBlock acceptance (whole file).
    ok, err = _try_run(yaml_path)
    if ok:
        result["run_ok"] = True
        return result

    result["run_error"] = err
    result["failing_entries"] = _identify_failing_entries(parsed, err or "")
    return result


def find_yaml_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for ext in ("*.yaml", "*.yml"):
        files.extend(root.rglob(ext))
    # Keep output deterministic and skip this script's own output file.
    return sorted(p for p in files if p.is_file())


def _fmt_err(err: str | None, *, indent: int = 0) -> str:
    if err is None:
        return ""
    lead = " " * indent
    return "\n".join(lead + line for line in err.rstrip().splitlines())


def _is_passing(r: dict) -> bool:
    return r["yaml_ok"] and not r["static_errors"] and r["run_ok"]


def _rel(path: Path, root: Path) -> Path:
    return path.relative_to(root) if path.is_relative_to(root) else path


def write_report(results: list[dict], out_path: Path, yaml_root: Path) -> None:
    total = len(results)
    yaml_fail = [r for r in results if not r["yaml_ok"]]
    static_fail = [r for r in results if r["yaml_ok"] and r["static_errors"]]
    run_fail = [r for r in results if r["yaml_ok"] and not r["run_ok"]]
    passed = [r for r in results if _is_passing(r)]

    lines: list[str] = []
    lines.append("# YAML validation report")
    lines.append("")
    lines.append(f"- YAML root: `{yaml_root}`")
    lines.append(f"- Files scanned: **{total}**")
    lines.append(f"- PyYAML parse failures: **{len(yaml_fail)}**")
    lines.append(f"- Static validation failures: **{len(static_fail)}**")
    lines.append(f"- runSimulationBlock acceptance failures: **{len(run_fail)}**")
    lines.append(f"- Passed: **{len(passed)}**")
    lines.append("")
    lines.append("A file counts as passing only when it clears all three checks.")
    lines.append("")

    if yaml_fail:
        lines.append("## PyYAML parse failures")
        lines.append("")
        for r in yaml_fail:
            lines.append(f"### `{_rel(r['path'], yaml_root)}`")
            lines.append("")
            lines.append("```text")
            lines.append(_fmt_err(r["yaml_error"]))
            lines.append("```")
            lines.append("")

    if static_fail:
        lines.append("## Static validation issues")
        lines.append("")
        lines.append(
            "From `metis_simulations.runRecipes.validate_recipes` — checks "
            "required keys, filter/ND/catg/tech/type/mode allow-lists, and "
            "positive `nObs`/`ndit`/`dit`."
        )
        lines.append("")
        for r in static_fail:
            lines.append(f"### `{_rel(r['path'], yaml_root)}`")
            lines.append("")
            for msg in r["static_errors"]:
                lines.append(f"- {msg}")
            lines.append("")

    if run_fail:
        lines.append("## runSimulationBlock acceptance failures")
        lines.append("")
        for r in run_fail:
            lines.append(f"### `{_rel(r['path'], yaml_root)}`")
            lines.append("")
            lines.append("**Top-level error:**")
            lines.append("")
            lines.append("```text")
            lines.append(_fmt_err(r["run_error"]))
            lines.append("```")
            lines.append("")
            if r["failing_entries"]:
                lines.append("**Failing YAML entries:**")
                lines.append("")
                for name, err in r["failing_entries"]:
                    lines.append(f"- `{name}`")
                    lines.append("")
                    lines.append("  ```text")
                    for line in err.rstrip().splitlines():
                        lines.append(f"  {line}")
                    lines.append("  ```")
                    lines.append("")
            else:
                lines.append("_Could not isolate failure to a single entry — see top-level error above._")
                lines.append("")

    if passed:
        lines.append("## Passing files")
        lines.append("")
        for r in passed:
            lines.append(f"- `{_rel(r['path'], yaml_root)}`")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--yaml-dir",
        type=Path,
        default=HERE,
        help="Root directory to scan for YAML files (default: this script's directory).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=HERE / "yaml_validation_report.md",
        help="Path to the markdown report to write.",
    )
    args = parser.parse_args()

    _install_stubs()

    # Silence the chatter from runSimulationBlock / setupSimulations.
    devnull = open(os.devnull, "w")
    saved_stdout = sys.stdout
    sys.stdout = devnull
    try:
        files = find_yaml_files(args.yaml_dir)
        # Exclude the report file itself if it happens to match *.yaml — it
        # won't, but be defensive against stray outputs.
        files = [p for p in files if p.resolve() != args.output.resolve()]

        results: list[dict] = []
        for path in files:
            results.append(validate_file(path))
    finally:
        sys.stdout = saved_stdout
        devnull.close()

    write_report(results, args.output, args.yaml_dir.resolve())

    n_fail = sum(1 for r in results if not _is_passing(r))
    print(f"Scanned {len(results)} YAML file(s); {n_fail} failure(s).")
    print(f"Report written to: {args.output}")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
