from argparse import ArgumentParser
import matplotlib.pyplot as plt
import os



def main(input_directory):
    numOfVertices = []
    fixationProbabilities = []
    avgSteps = []
    avgFixationTimes = []
    
    for file in os.listdir(input_directory):
        if file.endswith(".out"):
            numOfVertices.append(int(file.split("result")[1].split(".out")[0]))
            with open(os.path.join(input_directory, file), 'r') as f:
                lines = f.readlines()
                fixation_probability = float(lines[0].split(":")[1].strip())
                avg_steps = float(lines[1].split(":")[1].strip())
                avg_fixation_time = float(lines[2].split(":")[1].strip())
                fixationProbabilities.append(fixation_probability)
                avgSteps.append(avg_steps)
                avgFixationTimes.append(avg_fixation_time)

    numOfVertices, fixationProbabilities, avgSteps, avgFixationTimes = zip(*sorted(zip(numOfVertices, fixationProbabilities, avgSteps, avgFixationTimes)))

    plt.plot(numOfVertices, fixationProbabilities, marker='o', label='Fixation Probability')
    plt.xlabel('Number of Vertices')
    plt.ylabel('Values')
    plt.title('Fixation Probability vs Number of Vertices')
    plt.legend()
    plt.show()       

    plt.plot(numOfVertices, avgSteps, label='Average Steps to Absorption', marker='o')
    plt.xlabel('Number of Vertices')
    plt.ylabel('Values')
    plt.title('Average number of steps vs Number of Vertices')
    plt.legend()
    plt.show()  

    plt.plot(numOfVertices, avgFixationTimes, marker='o', label='Average Fixation Time')
    plt.xlabel('Number of Vertices')
    plt.ylabel('Values')
    plt.title('Fixation time vs Number of Vertices')
    plt.legend()
    plt.show()  




if __name__ == "__main__":   

    parser = ArgumentParser(description="Create plots from given data.")

    parser.add_argument(
        "-i",
        "-in",
        "-dir",
        "--input_directory",
        default="examples",
        type=str,
        help=(
            "The folder with simulation outputs."
        ),
    )

    input_args = parser.parse_args()

    main(input_directory=input_args.input_directory)


