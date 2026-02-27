#!/bin/bash

dir=$1
[[ "$dir" != */ ]] && dir="$dir/"

for edges_path in ${dir}edges*.in; do
    # 1. Extract just the filename to avoid digits in the directory path
    filename=$(basename "$edges_path")
    
    # 2. Extract the number correctly
    num=$(echo "$filename" | sed 's/[^0-9]//g')
    
    # 3. Define the other filenames
    mutants="${dir}mutants${num}.in"
    out="${dir}result${num}.out"
    
    # 4. Run the simulation
    # Using "$edges_path" directly since it already includes the directory
    python3 simple_simulation.py --edges="$edges_path" --mutants="$mutants" -s=1000 -r=1 >> "$out"
    
    echo "Done with index: $num"
done