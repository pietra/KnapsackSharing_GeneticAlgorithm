# Genetic Algorithm

# Inicialize first population

# Calculate the fitness and volume of all chromosomes

# Check what percentage of the chromosomes in the population has the same fitness value
# More than 90% ?
# Yes:
# 90% has the same fit value and the number of generations is greater than the limit?
# Yes:
# STOP
# No:
# Back to: "Calculate the fitness and volume of all chromosomes"
# No:
# Randomly select 2 chromosomes from the population
# Perform crossover on the 2 chromosomes selected
# Perform mutation on the chromosomes obtained

class GeneticAlgorithm:
    # DATA STRUCT: List (groups) of lists (items) of tuples (weight|value)

    def __init__(self):
        self.numItems = None
        self.numGroups = None
        self.capacity = None
        self.numItemsByGroups = None
        self.items = None

    def readingfile(self, file):
        f = open(file, 'r')
        self.numItems = int(f.readline())
        self.numGroups = int(f.readline())
        self.capacity = int(f.readline())
        self.numItemsByGroups = (f.readline()).split()
        self.items = []

        groupIndex = 0

        for i in range(self.numGroups):
            self.items.append([])

        for numItems in self.numItemsByGroups:
            for i in range(int(numItems)):
                item = (f.readline()).split()
                self.items[groupIndex].append((int(item[0]), int(item[1])))
            groupIndex += 1

        # Printing to test
        #for i in range(self.numGroups):
            #print(self.items[i])
            #print("\n", len(self.items[i]))
            #print('\n')

    def calculating(self, file):
        self.readingfile(file)
