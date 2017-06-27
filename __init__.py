from sys import argv
from classes.ga import GeneticAlgorithm

if __name__ == '__main__':

    if len(argv) == 3:
        # Instantiating
        heuristic = GeneticAlgorithm(argv[2])
        heuristic.calculating(argv[1])
    else:
        print("Ops, this is the right format: python __init__.py <input file> <seed>")
        exit()
