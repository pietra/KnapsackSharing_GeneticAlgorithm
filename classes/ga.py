from classes.knapsacksharing import KnapsackSharing
from collections import Counter
import random


class GeneticAlgorithm:
    def __init__(self, seed):
        self.SIZE_POPULATION = 60
        self.MAX_GENERATION = 10000
        self.SAME_FITNESS_GENERATIONS = 0
        self.NUM_CHROMOSOMES_TOURNAMENT_SELECTION = 20
        self.MUTATION_TAX = 1  # 0.001 %
        self.NUM_CLONED_CHROMOSOMES = 1
        self.seed = seed
        self.problemInstance = KnapsackSharing()
        self.population = None
        self.currentGeneration = 0

    def generateChromosome(self):

        # Initializing chromosome struct
        chromosome = [[] for _ in range(self.problemInstance.numGroups)]

        groupIndex = 0

        for numItems in self.problemInstance.numItemsByGroups:  # Passing by each group
            for j in range(int(numItems)):  # Passing by each item of group
                random.seed(self.problemInstance.seed)
                p = (random.randint(0, 100))  # Generates a random probability of the item be in the bag
                if random.randint(0, 100) < p:
                    chromosome[groupIndex].append(1)  # Is the item in the bag? Randomly decides
                else:
                    chromosome[groupIndex].append(0)
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

    def crossover(self, chromosome1, chromosome2):

        if self.chromosomeFitness(chromosome1) > self.chromosomeFitness(chromosome2):
            higherFitnessChromosome = chromosome1
            lowerFitnessChromosome = chromosome2
        else:
            higherFitnessChromosome = chromosome2
            lowerFitnessChromosome = chromosome1

        chromosomeSon = [[] for _ in range(self.problemInstance.numGroups)]

        groupIndex = 0

        for numItems in self.problemInstance.numItemsByGroups:
            for item in range(int(numItems)):  # Passing by each item of group
                prob = random.randint(1, 100)
                if prob <= 75:
                    chromosomeSon[groupIndex].append(higherFitnessChromosome[groupIndex][item])
                else:
                    chromosomeSon[groupIndex].append(lowerFitnessChromosome[groupIndex][item])
                # Probability of mutation = 0.001%
                random.seed(self.seed)
                probMutation = random.randint(self.MUTATION_TAX, 1000)
                # If mutation, flip bit
                if probMutation <= self.MUTATION_TAX:
                    if chromosomeSon[groupIndex][item] == 1:
                        chromosomeSon[groupIndex][item] = 0
                    else:
                        chromosomeSon[groupIndex][item] = 1
            groupIndex += 1

        return chromosomeSon

    def tournamentSelection(self):

        competitorsFitness = [0 for _ in range(self.NUM_CHROMOSOMES_TOURNAMENT_SELECTION)]
        competitorsIndex = [0 for _ in range(self.NUM_CHROMOSOMES_TOURNAMENT_SELECTION)]

        for j in range(self.NUM_CHROMOSOMES_TOURNAMENT_SELECTION):
            random.seed(self.problemInstance.seed)
            randomIndex = random.randint(0, len(self.population) - 1)
            competitorsIndex[j] = randomIndex
            competitorsFitness[j] = self.chromosomeFitness(self.population[randomIndex])

        winnerChromosome = self.population[competitorsIndex[competitorsFitness.index(max(competitorsFitness))]]

        return winnerChromosome

    def groupSelection(self):
        # Sorts the population by fitness. 75% of chance to pick a chromosome from the first half of the population
        populationFitness = []
        chromosomeIndexes = []

        # Calculates the fitness for all population
        for i in range(len(self.population)):
            populationFitness.append(self.chromosomeFitness(self.population[i]))

        # Sorts population by fitness
        for i in range(len(self.population)):
            indexBestFitness = populationFitness.index(max(populationFitness))
            chromosomeIndexes.append(indexBestFitness)
            populationFitness[indexBestFitness] = 0  # The best fitness is not the best fitness anymore

        random.seed(self.problemInstance.seed)
        prob = random.randint(1, 100)

        # 75% of chance to be one chromosome from the first half of the population
        if prob <= 60:
            random.seed(self.problemInstance.seed)
            indexFromFirstPart = random.randint(0, self.SIZE_POPULATION // 2)
            chromosomeWinnerIndex = chromosomeIndexes[indexFromFirstPart]
            return self.population[chromosomeIndexes[chromosomeWinnerIndex]]
        else:
            random.seed(self.problemInstance.seed)
            indexFromSecondPart = random.randint(self.SIZE_POPULATION // 2 + 1, self.SIZE_POPULATION - 1)
            chromosomeWinnerIndex = chromosomeIndexes[indexFromSecondPart]
            return self.population[chromosomeIndexes[chromosomeWinnerIndex]]

    def rouletteSelection(self):

        sumFitness = 0

        for i in range(self.SIZE_POPULATION):
            sumFitness += self.chromosomeFitness(self.population[i])

        random.seed(self.seed)
        randomProb = random.randint(0, sumFitness)
        t = 0

        for i in range(self.SIZE_POPULATION):
            t += self.chromosomeFitness(self.population[i])
            if t >= randomProb:
                return self.population[i]

    def generatingNewPopulation(self, bestFromPreviousPopulation):

        # POPULATION DATA STRUCT: List (chromosomes) of lists (groups) of lists (items) of numbers 0|1
        newPopulation = [[] for _ in range(self.SIZE_POPULATION)]

        # Initializing population data struct
        for i in range(self.SIZE_POPULATION):
            for j in range(self.problemInstance.numGroups):
                newPopulation[i].append([])

        chromosomeIndex = 0

        # ~50% of the population come from crossover
        for i in range(self.SIZE_POPULATION // 2):
            newPopulation[i] = self.crossover(self.rouletteSelection(), self.rouletteSelection())
            chromosomeIndex = i

        # And ~50% come from new chromosomes
        for i in range(chromosomeIndex + 1, self.SIZE_POPULATION - self.NUM_CLONED_CHROMOSOMES + 1):
            newPopulation[i] = self.generateChromosome()
            chromosomeIndex = i

        # But NUM_CLONED_CHROMOSOMES come from the best of the previous generation
        newPopulation[self.SIZE_POPULATION - 1] = bestFromPreviousPopulation

        self.currentGeneration += 1
        self.population = newPopulation

    def feasibleSolution(self, chromosome):
        # NOT USED ANYMORE
        groupIndex = 0
        volume = 0

        # Sum volumes and benefits of chromosome
        for numItems in self.problemInstance.numItemsByGroups:  # Passing by each group
            for j in range(int(numItems)):  # Passing by each item of group
                if chromosome[groupIndex][j] == 1:  # If the item is in the bag
                    volume += self.problemInstance.items[groupIndex][j][0]
            groupIndex += 1

        # If the volume of items in the chromosome > bag capacity
        # Fitness is decreased proportionally
        if volume > self.problemInstance.capacity:
            return 0
        else:
            return 1

    def calculating(self, file):

        self.problemInstance.readingfile(file)
        self.problemInstance.generatingGlpkData()
        self.generateFirstPopulation()

        while 1:

            print("GENERATION NUMBER ", self.currentGeneration)
            populationFitness = []

            # Calculate fitness for all the chromosomes
            for i in range(len(self.population)):
                populationFitness.append(self.chromosomeFitness(self.population[i]))

            # Chromosome with best fitness
            bestChromosome = self.population[populationFitness.index(max(populationFitness))]

            print("FITNESS: ", max(populationFitness))
            self.generatingNewPopulation(bestChromosome)
