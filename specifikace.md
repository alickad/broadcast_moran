# Broadcasting Moran process
## Description of the problem
Let's imagine a graph with unoriented edges. There are two types of vertices - mutants and residents.
In one step, we choose a random vertex of the graph. The probability of choosing each mutant is $p$ times the probability
of choosing each resident. After a vertex is selected, it propagates its type to each of its neighbours.
If we chose a resident, it will turn all its neighbouring vertices into residents and vice versa.

- What is the probability, that all vertices end up as mutants (fixation probability)?
- What is the average number of steps it takes for that to happen (fixation time)?
- What is the average number of steps it takes for all the vertices to have the same type (absorption time)?

## Goal of the project
I will answer these questions for various types of graphs. For that, I will
use both simulations and calculate it numerically. I will also create a visualisation of the simulations 
to gain some insight into the process. I will implement at least 3 out these 5 things:

- simulation-based solver for calculating fixation probability, fixation time and absorption time for a given graph and starting vertex
- numerical solver for a general (small) graph 
- go through all the small graphs and find those with interesting properties (long fixation/absortion time, ...)
- dedicated numerical solver for [caterpillar](https://en.wikipedia.org/wiki/Caterpillar_tree) graphs
- vizualization of the process and result



## The software
I will mainly use Python, it has some very nice libraries to work on similar simulations. I am going to use:
- ```networkx``` for graph representation
- ```random``` for the simulations
- ```matplotlib``` for visualizing graphs and creating graphs from data