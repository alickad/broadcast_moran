# Installation guide

## Requirements

- Python 3.10 or newer (the source uses Python 3.10 `match` syntax).
- `pip`.
- A terminal in which Python can be run.
- A graphical desktop and a working Matplotlib GUI backend only when using
  `--visualize`.

The project has been verified in this repository environment on Linux with
Python 3.14.8. Windows, macOS, and other Python versions have not yet been
verified.

## Install

Open a terminal in the repository root and create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
# Linux or macOS
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install the runtime dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The dependencies are NetworkX (graph data structures), NumPy and SciPy (the
exact solver), and Matplotlib (visualization).

## Verify the installation

From the repository root, run the test suite:

```bash
python -m unittest discover -s tests -v
```

Then run the simulation and exact solver using the included small example:

```bash
python -m scripts.simulate \
  --edges examples/demo/edges.in \
  --mutants examples/demo/mutants.in \
  --simulations 1000

python -m scripts.solve_exact \
  --edges examples/demo/edges.in \
  --mutants examples/demo/mutants.in
```

Run scripts as modules from the repository root. Both `--edges` and `--mutants`
are required; the programs do not assume paths based on the current directory.

## Configuration and troubleshooting

No separate configuration file is required. Input paths, mutant fitness, and
simulation count are provided as command-line options. Fitness must be a
positive finite number, and the simulation count must be at least one.

If Python reports `No module named ...`, confirm that the virtual environment
is active and rerun `python -m pip install -r requirements.txt`. If
visualization fails to open a window, check that the machine has a graphical
session and that Matplotlib has a compatible GUI backend; simulation and exact
solving do not require visualization.
