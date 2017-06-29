from classes.knapsacksharing import KnapsackSharing
from collections import Counter
import random


class GeneticAlgorithm:
    def __init__(self, seed):
        self.SIZE_POPULATION = 16
        self.SAME_FITNESS_VALUE_PERCENT = 0.9
        self.MAX_GENERATION = 1000
        self.NUM_CHROMOSOMES_TOURNAMENT_SELECTION = 5
        self.seed = seed
        self.problemInstance = KnapsackSharing()
        self.population = None
        self.currentGeneration = 1

    def generateChromosome(self):

        # Inicializing chromosome struct
        chromosome = [[] for _ in range(self.problemInstance.numGroups)]

        groupIndex = 0

        for numItems in self.problemInstance.numItemsByGroups:  # Passing by each group
            for j in range(int(numItems)):  # Passing by each item of group
                chromosome[groupIndex].append(random.randint(0, 1))  # Is the item in the bag? Randomly decides
            groupIndex += 1

        return chromosome

    def generateFirstPopulation(self):

        # POPULATION DATA STRUCT: List (chromosomes) of lists (groups) of lists (items) of numbers 0|1
        self.population = [[] for _ in range(self.SIZE_POPULATION)]

        # Populating randomly
        for chromosome in range(self.SIZE_POPULATION):  # Creating SIZE_POPULATION chromosomes
            self.population[chromosome] = self.generateChromosome()

    def chromosomeFitness(self, chromosome):

        groupIndex = 0
        volume = 0
        groupsBenefits = [0 for _ in range(self.problemInstance.numGroups)]

        # Sum volumes and benefits of chromosome
        for numItems in self.problemInstance.numItemsByGroups:  # Passing by each group
            for j in range(int(numItems)):  # Passing by each item of group
                if chromosome[groupIndex][j] == 1:  # If the item is in the bag
                    volume += self.problemInstance.items[groupIndex][j][0]
                    groupsBenefits[groupIndex] += self.problemInstance.items[groupIndex][j][1]
            groupIndex += 1

        # If the volume of items in the chromosome > bag capacity
        # Remove items from the groups with the max benefits until volume <= bag capacity
        # Why correct infeasible solutions here? Because this way we avoid another loop n^2
        if volume > self.problemInstance.capacity:
            fitInTheBag = 0
            while (fitInTheBag == 0):
                maxBenefitGroupIndex = groupsBenefits.index(
                    max(groupsBenefits))  # Index of the group with the max benefit
                randomItemIndex = random.randint(0,  # Index of a random item
                                                 int(self.problemInstance.numItemsByGroups[maxBenefitGroupIndex]) - 1)
                if chromosome[maxBenefitGroupIndex][randomItemIndex] == 1:  # If the item is in the bag, remove it
                    chromosome[maxBenefitGroupIndex][randomItemIndex] = 0
                    volume -= self.problemInstance.items[maxBenefitGroupIndex][randomItemIndex][0]
                    groupsBenefits[maxBenefitGroupIndex] -= \
                        self.problemInstance.items[maxBenefitGroupIndex][randomItemIndex][1]
                    if volume <= self.problemInstance.capacity:
                        fitInTheBag = 1

        return min(groupsBenefits)  # Returns the benefit of the group with the min benefit

    def checkPercentual(self, array):

        mostCommonElement = Counter(array).most_common(1)

        # If more than PERCENT_SAME_FITNESS_VALUE fitness values are equal
        if mostCommonElement[1] >= (self.SAME_FITNESS_VALUE_PERCENT * len(array)):
            # If the generation passed the limit
            if self.currentGeneration >= self.MAX_GENERATION:
                return mostCommonElement[0]
            else:
                return -1
        else:
            return -1

    def crossover(self, chromosome1, chromosome2):

        chromosome3 = [[] for _ in range(self.problemInstance.numGroups)]
        chromosome4 = [[] for _ in range(self.problemInstance.numGroups)]

        index = 0
        groupIndex = 0

        for numItems in self.problemInstance.numItemsByGroups:
            for item in range((int(numItems) // 2) - 1):  # Passing by each item of group
                chromosome3[groupIndex].append(chromosome1[groupIndex][item])
                chromosome4[groupIndex].append(chromosome2[groupIndex][item])
                index += 1
            for item in range(index, int(numItems)):  # Passing by each item of group
                chromosome3[groupIndex].append(chromosome2[groupIndex][item])
                chromosome4[groupIndex].append(chromosome1[groupIndex][item])
                index += 1
            groupIndex += 1
            index = 0

        return chromosome3, chromosome4

    def tournamentSelection(self):

        competitorsFitness = [0 for _ in range(self.NUM_CHROMOSOMES_TOURNAMENT_SELECTION)]
        competitorsIndex = [0 for _ in range(self.NUM_CHROMOSOMES_TOURNAMENT_SELECTION)]

        for j in range(self.NUM_CHROMOSOMES_TOURNAMENT_SELECTION):
            randomIndex = random.randint(0, len(self.population) - 1)
            competitorsIndex[j] = randomIndex
            competitorsFitness[j] = self.chromosomeFitness(self.population[randomIndex])
        winnerChromosome = self.population[competitorsIndex[competitorsFitness.index(max(competitorsFitness))]]

        return winnerChromosome

    def generatingNewPopulation(self):

        # POPULATION DATA STRUCT: List (chromosomes) of lists (groups) of lists (items) of numbers 0|1
        newPopulation = [[] for _ in range(self.SIZE_POPULATION)]

        # Inicializing population struct
        for i in range(self.SIZE_POPULATION):
            for j in range(self.problemInstance.numGroups):
                newPopulation[i].append([])

        chromosomeIndex = 0

        # 3/4 of the population come from previous populations, 1/4 come from new chromosomes
        for i in range((len(self.population) // 4) * 3):
            crossoverResult = self.crossover(self.tournamentSelection(), self.tournamentSelection())
            newPopulation[i] = crossoverResult[0]
            newPopulation[i + 1] = crossoverResult[1]
            i += 2
            chromosomeIndex = i

        for i in range(chromosomeIndex, (len(self.population))):
            newPopulation[i] = self.generateChromosome()

        self.currentGeneration += 1
        self.population = newPopulation

    def calculating(self, file):

        self.problemInstance.readingfile(file)
        self.generateFirstPopulation()

        while self.currentGeneration < self.MAX_GENERATION:
            self.generatingNewPopulation()
            print("NEW GENERATION")
            populationFitness = []
            for i in range(len(self.population)):
                populationFitness.append(self.chromosomeFitness(self.population[i]))
            print(max(populationFitness))