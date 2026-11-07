"""Run a bundled simulation block with its bundled YAML inputs."""

import argparse
from importlib.resources import as_file, files
import os
from pathlib import Path
import runpy
import sys


def main(argv=None):
    # Keep extracted resources alive throughout the simulation, including workers.
    with as_file(files("metis_simulations")) as root:
        blocks = {
            f"{path.parent.name}/{path.stem}": path
            for path in (root / "simulationBlocks").glob("*/*.py")
        }
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("block", choices=sorted(blocks), help="simulation block to run")
        args, block_args = parser.parse_known_args(argv)
        block = blocks[args.block]

        os.environ.setdefault("MSIM_YAML_DIR", str(root / "YAML" / block.parent.name))
        os.environ.setdefault("MSIM_NCORES", "1")
        os.environ.setdefault("MSIM_OUTDIR", str(Path.cwd() / "output"))
        original_argv = sys.argv
        try:
            sys.argv = [str(block), *block_args]
            runpy.run_path(str(block), run_name="__main__")
        finally:
            sys.argv = original_argv


if __name__ == "__main__":
    main()
