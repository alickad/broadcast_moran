def fix_prob_complete(N, mutant_fitness):
    return (mutant_fitness**2) / (mutant_fitness**2 + mutant_fitness + N - 2)

def fix_prob_star_from_center(N, mutant_fitness):
    return (mutant_fitness) / (mutant_fitness + N - 1)

def fix_prob_star_from_leaf(N, mutant_fitness):
    return mutant_fitness**2 / (mutant_fitness**2 + mutant_fitness + N - 2)

def fix_prob_cycle(N, mutant_fitness):
    r = mutant_fitness

    if r == 1:
        return 1/N

    return 1 / ( 1 + 2/r + (2/(r**2 * (r+1))) * ( (r-r**(7-N))/(r-1) + r**(5-N) * (r+1) + r**(4-N) * (r+1) / 2 )  )