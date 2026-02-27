def generate_paths():
    for num_of_nodes in [3, 4, 5, 6, 8, 10, 15, 20, 50, 100, 150]:     # we will see which of these sizes we want
        with open('./examples/paths/edges' + str(num_of_nodes) + '.in', 'w') as f:
            for i in range(num_of_nodes - 1):
                f.write(f"{i} {i + 1}\n")
        with open('./examples/paths/mutants' + str(num_of_nodes) + '.in', 'w') as f:
            f.write("0\n")    # based on mutants we want

def generate_cycles():
    for num_of_nodes in [3, 4, 5, 6, 8, 10, 15, 20, 50, 100, 150]:     # we will see which of these sizes we want
        with open('./examples/cycles/edges' + str(num_of_nodes) + '.in', 'w') as f:
            for i in range(num_of_nodes):
                f.write(f"{i} {(i + 1) % num_of_nodes}\n")
        with open('./examples/cycles/mutants' + str(num_of_nodes) + '.in', 'w') as f:
            f.write("0\n")    # based on mutants we want

def generate_paths_with_leaf():
    for num_of_nodes in [3, 4, 5, 6, 8, 10, 15, 20, 50, 100, 150]:     # we will see which of these sizes we want
        with open('./examples/paths_with_leaves/one_leaf_everywhere/edges' + str(num_of_nodes) + '.in', 'w') as f:
            for i in range(num_of_nodes - 1):
                f.write(f"{i} {i + 1}\n")
                f.write(f"{i} {num_of_nodes + i}\n")  # adding a leaf to each node in the path
            f.write(f"{num_of_nodes - 1} {2 * num_of_nodes - 1}\n")  # adding a leaf to the last node in the path
        with open('./examples/paths_with_leaves/one_leaf_everywhere/mutants' + str(num_of_nodes) + '.in', 'w') as f:
            f.write("0\n")    # based on mutants we want

generate_paths_with_leaf()