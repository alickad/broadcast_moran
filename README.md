# Broadcasting Moran process

This project simulates the broadcast Moran process on an undirected graph and
computes exact results for small graphs. It reports the probability that mutants
take over, the expected time to absorption, and the expected fixation time
conditional on fixation.

## Quick start

Use Python 3.10 or newer. From the repository root, create a virtual environment
and install the dependencies:

```bash
python -m venv .venv
```

Activate it (`source .venv/bin/activate` on Linux/macOS, or
`.venv\Scripts\Activate.ps1` in PowerShell), then run:

```bash
python -m pip install -r requirements.txt
python -m scripts.simulate \
  --edges examples/demo/edges.in \
  --mutants examples/demo/mutants.in \
  --simulations 1000
python -m scripts.solve_exact \
  --edges examples/demo/edges.in \
  --mutants examples/demo/mutants.in
```

Both input file paths are required. See the [installation guide](docs/installation.md)
for setup details, the [user guide](docs/user-guide.md) for commands and input
formats, and the [development guide](docs/development.md) for implementation
and testing information.

The documented commands and tests were checked on Linux with Python 3.14.8.
Other operating systems and Python versions have not yet been verified.
