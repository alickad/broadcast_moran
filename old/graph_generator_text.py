def generate_paths():
    for num_of_nodes in [3, 4, 5, 6, 8, 10, 15, 20, 25, 30, 40, 50]:     # we will see which of these sizes we want
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


def generate_path_with_n_leaves(n):
    for num_of_nodes in [3, 4, 5, 6, 8, 10, 12, 14, 17, 20, 25, 30, 50]:     # we will see which of these sizes we want
        with open('./examples/paths_with_leaves/' + str(n) + '_leaves/edges' + str(num_of_nodes) + '.in', 'w') as f:
            for i in range(num_of_nodes - 1):
                f.write(f"{i} {i + 1}\n")
                for j in range(n):
                    f.write(f"{i} {num_of_nodes + i * n + j}\n")  # adding n leaves to each node in the path
            for j in range(n):
                f.write(f"{num_of_nodes - 1} {num_of_nodes + (num_of_nodes - 1) * n + j}\n")  # adding n leaves to the last node in the path
        with open('./examples/paths_with_leaves/' + str(n) + '_leaves/mutants' + str(num_of_nodes) + '.in', 'w') as f:
            f.write("0\n")    # based on mutants we want

def generate_paths_with_linear_leaves():
    for num_of_nodes in [3, 4, 5, 6, 8, 10, 12, 14, 17, 20, 25, 30, 50]:     # we will see which of these sizes we want
        with open('./examples/paths_with_leaves/paths_with_linear_leaves/edges' + str(num_of_nodes) + '.in', 'w') as f:
            for i in range(num_of_nodes - 1):
                f.write(f"{i} {i + 1}\n")
            leaf_index = num_of_nodes
            for num_leaves in range((num_of_nodes) // 2):
                l1 = (num_of_nodes)//2 - num_leaves
                l2 = (num_of_nodes)//2 + num_leaves
                for j in range(num_leaves):
                    f.write(f"{l1} {leaf_index}\n")
                    leaf_index += 1
                    f.write(f"{l2} {leaf_index}\n")
                    leaf_index += 1
            if num_of_nodes % 2 == 1:  # if odd, add one more leaf to the middle node
                for j in range((num_of_nodes + 1) // 2):
                    f.write(f"{num_of_nodes - 1} {leaf_index}\n")
                    leaf_index += 1
        with open('./examples/paths_with_leaves/paths_with_linear_leaves/mutants' + str(num_of_nodes) + '.in', 'w') as f:
            f.write("0\n")    # based on mutants we want

#generate_paths_with_leaf()
generate_paths_with_linear_leaves()