# Development guide

## Project structure

- `moran/graph_utils.py` loads edge and mutant files, validates the graph, and
  assigns each vertex its initial state.
- `moran/simulation.py` implements one broadcast update and repeated
  Monte Carlo runs.
- `moran/exact_solver.py` enumerates reachable configurations and computes
  absorption quantities using sparse linear systems.
- `moran/visualization.py` draws and updates the graph using Matplotlib.
- `moran/graph_generators.py` provides programmatic path, cycle, and
  path-with-leaves generators.
- `scripts/simulate.py` and `scripts/solve_exact.py` are the command-line
  entry points intended for users.
- `tests/` contains the `unittest` suite.

## Model and implementation

For a graph with `N` vertices, a mutant is selected with weight `r` and a
resident with weight `1`, where `r` is the mutant fitness. The selected
vertex's type is copied to all adjacent vertices in one update. Therefore a
single update may change more than one vertex. Updates continue until the graph
is all-mutant or all-resident.

The simulation copies the initial graph for every run. It estimates fixation
probability as the fraction of runs ending all-mutant, absorption time as the
mean number of updates over all runs, and conditional fixation time as the mean
number of updates among runs ending all-mutant. Random choices use Python's
`random` module; the CLI currently has no seed option.

The exact solver represents a configuration as an integer bit mask, where bit
`i` indicates whether vertex `i` is mutant. It discovers reachable
configurations, builds transient (`Q`) and absorbing (`R`) transition matrices,
and solves sparse linear systems for absorption probabilities and expected
times. Its state-space size may be exponential in the number of vertices, so it
is intended for small graphs.

The exact solver's bit-mask representation expects vertex IDs `0` through
`N - 1`. The `solve_exact` command normalizes arbitrary integer labels before
calling the solver; direct callers of `moran.exact_solver.main` should provide
consecutive non-negative IDs.

## Build, run, and test

There is no separate build step or packaging configuration at present. Create
and activate a virtual environment, install `requirements.txt`, and run the
entry points as modules from the repository root:

```bash
python -m scripts.simulate --edges examples/demo/edges.in --mutants examples/demo/mutants.in
python -m scripts.solve_exact --edges examples/demo/edges.in --mutants examples/demo/mutants.in
python -m unittest discover -s tests -v
```

When modifying the model or result calculations, add focused tests to `tests/`
and compare simulation estimates with exact results on small graphs when
possible.

## Important constraints

- Input graphs must be non-empty, connected, and undirected.
- The edge-list format cannot represent isolated vertices.
- Fitness must be positive and finite; simulation count must be a positive
  integer.
- The exact solver is suitable only for graphs whose reachable state space
  fits available memory and runtime.
- The included test suite and CLI examples have been checked on Linux with
  Python 3.14.8; other operating systems and Python versions still need
  verification.
