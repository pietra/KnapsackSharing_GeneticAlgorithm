# Reading argv's

# FILE FORMAT:
# nro itens (n)
# nro grupos (g)
# capacidade da mochila (C)
# nro de itens do grupo 1 ... nro de itens do grupo (g)
# item 1 (peso & lucro do item)
# ...
# item n (peso & lucro do item)

from classes.ga import GeneticAlgorithm

if __name__ == '__main__':

    # Instantiating
    heuristic = GeneticAlgorithm(None)

    heuristic.calculating()