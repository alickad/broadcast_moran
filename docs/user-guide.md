# User guide

## What the program does

The program works with an undirected graph whose vertices are either mutants or
residents. At each step, one vertex is selected with weight equal to its type's
fitness: a mutant has weight `mutant_fitness`, and a resident has weight `1`.
The selected vertex changes all its neighbors to its own type. The process ends
when all vertices have the same type.

The simulation estimates the results by repeating the process. The exact solver
constructs the reachable state space and solves the corresponding transition
system; it is intended for graphs with a small state space. The state space can
grow exponentially with the number of vertices.

## Input files

Both programs require an edge file and a mutant file.

### Edge file

Each non-empty line contains exactly two integer vertex IDs, separated by
whitespace. The edge is undirected. IDs may be negative.

```text
-4 -1
-1 8
```

The graph must be connected and non-empty. Every vertex must appear in at least
one edge; isolated vertices cannot be represented by this format.
Blank lines are not valid edge records.

The exact solver internally remaps vertex IDs to `0, 1, 2, ...`. This does not
change the IDs shown in the simulation visualization.

### Mutant file

Each line contains one integer vertex ID that is initially mutant. IDs must
occur in the edge file and must not be repeated. An empty file means there are
no initial mutants. Do not use blank lines in a non-empty mutant file.

Example:

```text
-4
```

The loader rejects malformed edges, invalid IDs, duplicate or unknown mutants,
an empty edge file, and disconnected graphs.

## Simulation

Run from the repository root:

```bash
python -m scripts.simulate \
  --edges examples/demo/edges.in \
  --mutants examples/demo/mutants.in \
  --mutant_fitness 1 \
  --simulations 1000
```

Options:

| Option | Required | Default | Description |
|---|---:|---:|---|
| `-e`, `--edges` | Yes | — | Path to the edge file |
| `-m`, `--mutants` | Yes | — | Path to the initial mutant file |
| `-r`, `--mutant_fitness` | No | `1` | Positive finite mutant fitness |
| `-s`, `--simulations` | No | `1` | Number of independent runs; must be at least `1` |
| `--visualize` | No | Off | Animate each simulation in a Matplotlib window |

The simulation prints fixation probability, absorption time, conditional
fixation time, and execution time. Results are Monte Carlo estimates and may
vary between runs. The command-line interface does not currently expose a
random seed.

To enable visualization, add `--visualize`. Mutants are shown in red and
residents in blue. Visualization slows the simulation because the display is
updated after each step.

## Exact solver

Run:

```bash
python -m scripts.solve_exact \
  --edges examples/demo/edges.in \
  --mutants examples/demo/mutants.in \
  --mutant_fitness 1
```

The exact solver accepts the same required paths and fitness option as the
simulation. It prints fixation probability, conditional fixation time,
absorption time, and execution time. It normalizes vertex IDs internally, so
input IDs do not need to start at zero.

The exact method can become impractical as graph size increases. Use the
simulation for larger graphs.

## Interpreting the results

- **Fixation probability**: probability that mutants eventually occupy every
  vertex, starting from the supplied initial state.
- **Conditional fixation time**: expected number of update steps to fixation,
  conditioned on fixation occurring. The simulation reports `0` if no
  simulated run reaches fixation.
- **Absorption time**: expected number of update steps until all vertices have
  the same type, whether mutants fix or go extinct.
- **Execution time**: wall-clock duration of that command, in seconds.

## Running tests

From the repository root:

```bash
python -m unittest discover -s tests -v
```
