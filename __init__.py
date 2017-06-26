# Reading argv's

# FILE FORMAT:
# nro itens (n)
# nro grupos (g)
# capacidade da mochila (C)
# nro de itens do grupo 1 ... nro de itens do grupo (g)
# item 1 (peso & lucro do item)
# ...
# item n (peso & lucro do item)

from sys import argv
from classes.ga import GeneticAlgorithm

if __name__ == '__main__':

    #Instantiating
    heuristic = GeneticAlgorithm()

    if len(argv) == 2:
        heuristic.calculating(argv[1])
    else:
        print("Ops, this is the right format: python __init__.py <arquivo de entrada>")
        exit()
