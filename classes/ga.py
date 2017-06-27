from classes.knapsacksharing import KnapsackSharing

import random


class GeneticAlgorithm:
    def __init__(self, seed):
        self.SIZE_POPULATION = 10
        self.seed = seed
        self.problemInstance = KnapsackSharing()
        self.population = None

    def generateFirstPopulation(self):

        # POPULATION DATA STRUCT: List (chromosomes) of lists (groups) of lists (items) of numbers 0|1
        self.population = [[] for _ in range(self.problemInstance.numGroups)]

        # Inicializing population struct
        for i in range(self.SIZE_POPULATION):
            for j in range(self.problemInstance.numGroups):
                self.population[i].append([])

        groupIndex = 0

        for chromosome in range(self.SIZE_POPULATION):  # Creating SIZE_POPULATION chromosomes
            for numItems in self.problemInstance.numItemsByGroups:  # Passing by each group
                for j in range(int(numItems)):  # Passing by each item of group
                    self.population[chromosome][groupIndex].append(
                        random.randint(0, 1))  # Is the item in the bag? Randomly decides
                groupIndex += 1
            groupIndex = 0

    def chromosomeFitness(self, chromosome):

        groupIndex = 0
        volume = 0
        groupsBenefits = [0 for _ in range(self.problemInstance.numGroups)]

        for numItems in self.problemInstance.numItemsByGroups:  # Passing by each group
            for j in range(int(numItems)):  # Passing by each item of group
                if chromosome[groupIndex][j] == 1:  # If the item is in the bag
                    volume += self.problemInstance.items[groupIndex][j][0]
                    groupsBenefits[groupIndex] += self.problemInstance.items[groupIndex][j][1]
            groupIndex += 1

        # If the volume of items in the chromosome > bag capacity
        # Remove items from the groups with the max benefits
        if volume > self.problemInstance.capacity:
            fitInTheBag = 0
            while (fitInTheBag == 0):
                maxBenefitGroupIndex = groupsBenefits.index(
                    max(groupsBenefits))  # Index of the group with the max benefit
                randomItemIndex = random.randint(0,
                                                 int(self.problemInstance.numItemsByGroups[maxBenefitGroupIndex]) - 1)
                if (chromosome[maxBenefitGroupIndex][randomItemIndex] == 1):
                    chromosome[maxBenefitGroupIndex][randomItemIndex] = 0
                    volume -= self.problemInstance.items[maxBenefitGroupIndex][randomItemIndex][0]
                    groupsBenefits[maxBenefitGroupIndex] -= self.problemInstance.items[maxBenefitGroupIndex][randomItemIndex][1]
                    if volume <= self.problemInstance.capacity:
                        fitInTheBag = 1

        return min(groupsBenefits)  # Returns the benefit of the group with the min benefit

    def calculating(self, file):
        self.problemInstance.readingfile(file)
        self.generateFirstPopulation()

        for chromosome in range(self.SIZE_POPULATION):
            print(self.chromosomeFitness(self.population[chromosome]))
