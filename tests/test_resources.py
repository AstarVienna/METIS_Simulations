"""Bundled blocks can find their inputs without a repository checkout."""

from importlib.resources import as_file, files
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
from types import ModuleType
from unittest.mock import Mock

import pytest

from metis_simulations.__main__ import main


def test_bundled_eso_resources():
    root = files("metis_simulations")
    assert root.joinpath("simulationBlocks/ESO/imgLM.py").is_file()
    for name in ("scienceLM.yaml", "stdLM.yaml"):
        assert "IMAGE,LM" in root.joinpath("YAML", "ESO", name).read_text()
    assert root.joinpath("templates.yaml").is_file()


@pytest.fixture
def simulation_runner(monkeypatch):
    # Execute the real block, replacing only the costly ScopeSim entry point.
    module = ModuleType("metis_simulations.runSimulationBlock")
    module.runSimulationBlock = Mock()
    monkeypatch.setitem(sys.modules, module.__name__, module)
    return module.runSimulationBlock


def test_runner_uses_bundled_inputs_outside_checkout(monkeypatch, tmp_path, simulation_runner):
    monkeypatch.chdir(tmp_path)
    for name in ("MSIM_YAML_DIR", "MSIM_NCORES", "MSIM_OUTDIR"):
        monkeypatch.delenv(name, raising=False)
    original_argv = sys.argv

    main(["ESO/imgLM", "--small", "--nCores", "2"])

    simulation_runner.assert_called_once()
    yamls, params, args = simulation_runner.call_args.args
    assert [Path(name).name for name in yamls] == ["scienceLM.yaml", "stdLM.yaml"]
    assert all(Path(name).is_file() for name in yamls)
    assert Path(params["outputDir"]).is_relative_to(tmp_path / "output")
    assert params["nCores"] == "1"
    assert args == ["--small", "--nCores", "2"]
    assert sys.argv is original_argv


def test_runner_preserves_environment_overrides(monkeypatch, tmp_path, simulation_runner):
    monkeypatch.setenv("MSIM_YAML_DIR", str(tmp_path / "custom-yaml"))
    monkeypatch.setenv("MSIM_OUTDIR", str(tmp_path / "custom-output"))
    monkeypatch.setenv("MSIM_NCORES", "3")

    main(["ESO/imgLM"])

    yamls, params, _ = simulation_runner.call_args.args
    assert all(Path(name).parent == tmp_path / "custom-yaml" for name in yamls)
    assert Path(params["outputDir"]).is_relative_to(tmp_path / "custom-output")
    assert params["nCores"] == "3"


def test_runner_rejects_unknown_block():
    with pytest.raises(SystemExit) as error:
        main(["ESO/not-a-block"])
    assert error.value.code == 2
